all: metadata images assets entries pages

.PHONY: publish edit patch
REVISION := python -m src.revision
publish:; $(REVISION) major
edit:; $(REVISION) minor
patch:; $(REVISION) patch

.PHONY: metadata
metadata: www/VERSION
www/VERSION: VERSION
	cp $< $@

.PHONY: resize
resize:; python -m src.resize_images

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
	python -m http.server -d www -b 0.0.0.0 4000
