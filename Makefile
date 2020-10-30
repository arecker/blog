entries_sources := $(wildcard entries/*.md)
entry_outputs := $(addprefix www/, $(notdir $(addsuffix .html, $(basename $(entries_sources)))))
pages_sources := $(wildcard pages/*.md)
pages_metadatas := $(addsuffix .metadata.yml, $(basename $(pages_sources)))
pages_outputs := $(addprefix www/, $(notdir $(addsuffix .html, $(basename $(pages_sources)))))
partials := $(wildcard templates/_*.html)

build: www/images www/site.css $(entry_outputs) $(pages_outputs)

www/images:
	mkdir -p www
	cp -r images $@

www/site.css:
	mkdir -p www
	cp assets/site.css $@

templates/page.html templates/entry.html $(partials) $(pages_metadatas) $(entries_sources):
	touch $@

$(entry_outputs): templates/entry.html $(partials) scripts/entry_filter.lua
	mkdir -p www
	cd www && pandoc \
-s \
-t html \
--template=../templates/entry.html \
--lua-filter=../scripts/entry_filter.lua \
../entries/$(addsuffix .md, $(notdir $(basename $@))) | tidy -iq -o $(notdir $@)

pages: $(pages_outputs)

entries: $(entries_outputs)

$(pages_outputs): templates/page.html $(partials) $(pages_sources)
	mkdir -p www
	cd www && pandoc \
-s \
-t html \
--template=../templates/page.html \
../pages/$(addsuffix .md, $(notdir $(basename $@))) | tidy -iq -o $(notdir $@)

.PHONY: clean
clean:
	rm -rf www

.PHONY: serve
serve: build
	python -m http.server --directory "www" --bind "0.0.0.0" 4000
