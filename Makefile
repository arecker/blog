entries_sources := $(wildcard entries/*.md)
entry_outputs := $(addprefix www/, $(notdir $(addsuffix .html, $(basename $(entries_sources)))))

build: www/images www/site.css $(entry_outputs)

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
-o $(notdir $@) ../entries/$(addsuffix ".md", $(notdir $(basename $@)))

.PHONY: clean
clean:
	rm -rf www

.PHONY: serve
serve: build
	python -m http.server --directory "www" --bind "127.0.0.1" 4000
