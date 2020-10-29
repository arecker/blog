entries_sources := $(wildcard entries/*.md)
entry_outputs := $(addprefix www/, $(notdir $(addsuffix .html, $(basename $(entries_sources)))))
pages_sources := $(wildcard pages/*.html)
pages_outputs := $(addprefix www/, $(notdir $(pages_sources)))

build: www/images www/site.css $(entry_outputs) $(pages_outputs)

www/images:
	mkdir -p www
	cp -r images $@

www/site.css:
	mkdir -p www
	cp assets/site.css $@

$(entry_outputs):
	mkdir -p www
	cd www && pandoc \
-s \
--template=../templates/entry.html \
--lua-filter=../scripts/entry_filter.lua \
-o $(notdir $@) ../entries/$(addsuffix .md, $(notdir $(basename $@)))

$(pages_outputs):
	mkdir -p www
	cd www && pandoc \
-s \
--template=../templates/page.html \
--metadata-file=../pages/$(addsuffix .metadata.yml, $(basename $(notdir $@))) \
-o $(notdir $@) ../pages/$(notdir $@)

.PHONY: clean
clean:
	rm -rf www

.PHONY: serve
serve: build
	# python -m http.server --directory "www" --bind "127.0.0.1" 4000
	python -m http.server --directory "www" --bind "0.0.0.0" 4000
