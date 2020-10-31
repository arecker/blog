all: images assets entries

.PHONY: images
image_files := $(shell find images -type f)
images: $(addprefix www/,$(image_files))
www/images/%: images/%
	mkdir -p $(@D)
	cp $< $@

.PHONY: assets
assets: www/site.css
www/site.css: assets/site.css
	mkdir -p $(@D)
	cp $< $@

pandoc := pandoc -s -L ../pandoc/revision.lua --template ../pandoc/template.html

.PHONY: entries
entry_files := $(wildcard entries/*.md)
entry_outputs := $(patsubst %.md,%.html,$(subst entries/,www/,$(entry_files)))
pandoc_entry := $(pandoc) -L ../pandoc/entry.lua
entries: $(entry_outputs)
www/%.html: entries/%.md pandoc/entry.lua pandoc/template.html
	cd www && $(pandoc_entry) -o $(notdir $@) ../$<

.PHONY: pages
pandoc_page := $(pandoc) -L ../pandoc/page.lua --template ../pandoc/template.html
pages: www/index.html
www/index.html: pages/index.html
	cd www && $(pandoc_page) -o $(notdir $@) ../$<

.PHONY: publish edit patch
publish:; scripts/rev.sh major
edit:; scripts/rev.sh minor
patch:; scripts/rev.sh patch

.PHONY: clean
clean:
	rm -rf www/images
	rm -rf www/*.html

.PHONY: serve
serve: all
	python -m http.server -d www -b 0.0.0.0 4000
