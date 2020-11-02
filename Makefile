all: metadata images assets entries pages

REVISION := $(shell scripts/rev.sh show)
.PHONY: publish edit patch
revision_files := revision/major revision/minor revision/patch
publish:; scripts/rev.sh major
edit:; scripts/rev.sh minor
patch:; scripts/rev.sh patch

.PHONY: metadata
metadata: www/revision.txt
www/revision.txt: $(revision_files)
	echo "$(REVISION)" > www/revision.txt

.PHONY: images resize
image_files := $(shell find images -type f)
images: $(addprefix www/,$(image_files))
resize:
	scripts/autosize.sh
www/images/%: images/%
	mkdir -p $(@D)
	cp $< $@

.PHONY: assets
assets: $(addprefix www/,$(notdir $(shell find assets -type f)))
www/%: assets/%
	mkdir -p $(@D)
	cp $< $@

pandoc := pandoc -s --metadata revision="$(REVISION)" --template ../pandoc/template.html

.PHONY: entries
entry_files := $(wildcard entries/*.md)
entry_outputs := $(patsubst %.md,%.html,$(subst entries/,www/,$(entry_files)))
pandoc_entry := $(pandoc) -L ../pandoc/entry.lua
entries: $(entry_outputs)
www/%.html: entries/%.md pandoc/entry.lua pandoc/template.html $(revision_files)
	cd www && $(pandoc_entry) -o $(notdir $@) ../$<

.PHONY: pages
page_files := $(wildcard pages/*.html)
pandoc_page := $(pandoc) -L ../pandoc/page.lua
pages: $(subst pages/,www/,$(page_files))
www/%.html: pages/%.html pages/%.yml pandoc/template.html $(revision_files)
	cd www && $(pandoc_page) --metadata-file="../$(patsubst %.html,%.yml,$<)" -o $(notdir $@) ../$<

.PHONY: clean
clean:
	rm -rf www/*

.PHONY: serve
serve: all
	python -m http.server -d www -b 0.0.0.0 4000
