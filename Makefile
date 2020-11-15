#############
# RESOURCES #
#############

all: hooks images assets entries pages

.PHONY: hooks
hooks: .git/hooks/pre-commit
.git/hooks/pre-commit: scripts/pre-commit.bash
	cp -R $< $@

.PHONY: images
images: www/images
www/images: images/
	cp -R $< $@

.PHONY: assets
assets: $(addprefix www/,$(notdir $(shell find assets -type f)))
www/%: assets/%
	cp $< $@

revision := $(shell cat VERSION)
pandoc := pandoc -s --metadata revision="$(revision)"

.PHONY: entries
entry_files := $(wildcard entries/*.md)
entry_outputs := $(patsubst %.md,%.html,$(subst entries/,www/,$(entry_files)))
pandoc_entry := $(pandoc) --template ../pandoc/entry.html -L ../pandoc/entry.lua
entries: $(entry_outputs)
www/%.html: entries/%.md pandoc/entry.lua pandoc/entry.html VERSION
	cd www && $(pandoc_entry) -o $(notdir $@) ../$<

############
# COMMANDS #
############

.PHONY: publish edit patch
REVISION := ./scripts/revision.bash
publish:; $(REVISION) major
edit:; $(REVISION) minor
patch:; $(REVISION) patch

.PHONY: resize
resize:; scripts/resize.bash

.PHONY: clean
clean:
	rm -rf www/*

.PHONY: test
test:
	python -m unittest

.PHONY: serve
serve: all
	rm -rf www/ga.js
	python -m http.server -d www -b 0.0.0.0 4000
