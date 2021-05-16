MAKEFLAGS += --no-builtin-rules -j10

SCRIPTS := thumbnails

.PHONY: all
all: site

.PHONY: site
site: _site
_site: sitemap.xml feed.xml data $(wildcard _posts/*) $(wildcard _pages/*) _layouts/default.html
	bundle exec jekyll build

.PHONY: data
data: _data/git.yml _data/nav.yml _data/stats.yml _data/projects.yml

sitemap.xml: scripts/genxml $(wildcard _posts/*) $(wildcard _pages/*)
	scripts/genxml sitemap > $@

feed.xml: scripts/genxml $(wildcard _posts/*)
	scripts/genxml feed > $@

_data/git.yml: scripts/gengit .git
	scripts/gengit > $@

_data/nav.yml: scripts/gennav $(wildcard _pages/*)
	scripts/gennav > $@

_data/stats.yml: scripts/genstats $(wildcard _posts/*)
	scripts/genstats > $@

_data/projects.yml: scripts/genprojects $(wildcard _posts/*)
	scripts/genprojects > $@

bin/blog: $(wildcard src/*.go)
	go build -o $@ ./...

.PHONY: $(SCRIPTS)
$(SCRIPTS):
	@scripts/$@

.PHONY: clean
clean:
	rm -rf _data/*
	rm -rf feed.xml sitemap.xml
	rm -rf _site
	rm -rf bin/blog

.PHONY: serve
serve: site
	bundle exec jekyll serve

.PHONY: info
info: bin/blog
	@bin/blog -info -version

.PHONY: patch
patch:
	@bin/blog-bump patch
