ALL: assets images entries pages

.PHONY: assets
assets: $(addprefix www/, $(shell find assets -type "f"))
www/assets/%: assets/%
	mkdir -p $(@D)
	cp $< $@

.PHONY: images
images: $(addprefix www/, $(shell find images -type "f"))
www/images/%: images/%
	mkdir -p $(@D)
	cp $< $@

PANDOC := cd ./www && pandoc -s --metadata timestamp="$(shell date)"

.PHONY: entries
entry_sources := $(wildcard entries/*.md)
entry_targets := $(addprefix www/, $(patsubst %.md, %.html, $(notdir $(entry_sources))))
entries: $(entry_targets)
www/%.html: entries/%.md pandoc/page.html pandoc/entry.lua
	$(PANDOC) -o $*.html --template ../pandoc/page.html -L ../pandoc/entry.lua ../entries/$*.md

.PHONY: pages
page_sources := $(wildcard pages/*.html)
page_targets := $(subst pages/, www/, $(page_sources))
pages: $(page_targets)
www/%.html: pages/%.html
	@echo page: $*.html

.PHONY: publish edit patch
publish:; ./scripts/revision.bash major
edit:; ./scripts/revision.bash minor
patch:; ./scripts/revision.bash patch

scripts := serve
.PHONY: $(scripts)
$(scripts):
	./scripts/$@.bash

.PHONY: clean test
clean:
	rm -rf www/*
test:
	python -m unittest
