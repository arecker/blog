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
entries: $(entry_outputs)
www/%.html: entries/%.md pandoc/entry.lua pandoc/template.html
	cd www && pandoc -L ../pandoc/entry.lua --template ../pandoc/template.html -o $(notdir $@) ../$<

.PHONY: clean
clean:
	rm -rf www/images
	rm -rf www/*.html

.PHONY: serve
serve: all
	python -m http.server -d www -b 127.0.0.1 4000
