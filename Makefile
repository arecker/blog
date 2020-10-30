all: images

.PHONY: images
image_files := $(shell find images -type f)
images: $(addprefix www/,$(image_files))
www/images/%: images/%
	mkdir -p $(@D)
	cp $< $@

.PHONY: clean
clean:
	rm -rf www/images
	rm -rf www/*.html
