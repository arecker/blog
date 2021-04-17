MAKEFLAGS += --no-builtin-rules -j10

SCRIPTS := thumbnails

.PHONY: all
all: site

.PHONY: site
site: _site
_site: sitemap.xml feed.xml _data/git.yml _data/nav.yml $(wildcard _posts/*) $(wildcard _pages/*) _layouts/default.html
	bundle exec jekyll build

sitemap.xml: scripts/genxml $(wildcard _posts/*) $(wildcard _pages/*)
	scripts/genxml sitemap > $@

feed.xml: scripts/genxml $(wildcard _posts/*)
	scripts/genxml feed > $@

_data/git.yml: scripts/gengit .git
	scripts/gengit > $@

_data/nav.yml: scripts/gennav $(wildcard _pages/*)
	scripts/gennav > $@

.PHONY: $(SCRIPTS)
$(SCRIPTS):
	@scripts/$@

.PHONY: clean
clean:
	rm -rf _data/*
	rm -rf feed.xml sitemap.xml
	rm -rf _site

.PHONY: serve
serve: site
	bundle exec jekyll serve
