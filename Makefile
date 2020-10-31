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

.PHONY: entries
entry_files := $(wildcard entries/*.md)
entry_outputs := $(patsubst %.md,%.html,$(subst entries/,www/,$(entry_files)))
pandoc_entry := pandoc -L ../pandoc/entry.lua --template ../pandoc/template.html
entries: $(entry_outputs)
www/%.html: entries/%.md pandoc/entry.lua pandoc/template.html
	cd www && $(pandoc_entry) -o $(notdir $@) ../$<

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
	python -m http.server -d www -b 127.0.0.1 4000
