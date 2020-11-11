all: metadata images assets entries pages

.PHONY: publish edit patch
publish:; python -m src.revision major
edit:; python -m src.revision  minor
patch:; python -m src.revision patch

.PHONY: metadata
metadata: www/VERSION
www/VERSION: VERSION
	cp $< $@

.PHONY: images
image_files := $(shell find images -type f)
images: $(addprefix www/,$(image_files))
www/images/%: images/%
	mkdir -p $(@D)
	cp $< $@

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
	python -m http.server -d www -b 0.0.0.0 4000
