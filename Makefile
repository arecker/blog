build: www/images www/site.css www/2020-10-27.html

www/images:
	cp -r images $@

www/site.css:
	mkdir -p www
	cp assets/site.css $@

www/2020-10-27.html:
	mkdir -p www
	cd www && pandoc \
-s \
--template=../templates/entry.html \
--lua-filter=../filters/entry.lua \
-o $(notdir $@) ../entries/2020-10-27.md

.PHONY: serve
serve: build
	python -m http.server --directory "www" --bind "127.0.0.1" 4000
