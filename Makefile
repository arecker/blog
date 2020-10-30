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
www/%.html: entries/%.md
	cd www && pandoc -o $(notdir $@) ../$<


.PHONY: clean
clean:
	rm -rf www/images
	rm -rf www/*.html
