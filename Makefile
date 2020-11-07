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
