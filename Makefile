all: hooks images assets entries pages

.PHONY: publish edit patch
REVISION := ./scripts/revision.bash
publish:; $(REVISION) major
edit:; $(REVISION) minor
patch:; $(REVISION) patch

.PHONY: resize
resize:; scripts/resize.bash

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
	mkdir -p $(@D)
	cp $< $@

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
