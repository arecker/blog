MAKEFLAGS += --no-builtin-rules -j10

SCRIPTS := thumbnails
GOOSES := darwin linux freebsd
BINARY_TARGETS := $(addprefix bin/blog-, $(GOOSES))

.PHONY: all
all: newsite site

.PHONY: newsite
newsite: ./bin/blog
	./bin/blog -info -data

.PHONY: site
site: _site
_site: sitemap.xml feed.xml data $(wildcard _posts/*) $(wildcard _pages/*) _layouts/default.html
	bundle exec jekyll build

.PHONY: data
data: _data/git.yml _data/stats.yml _data/projects.yml

sitemap.xml: scripts/genxml $(wildcard _posts/*) $(wildcard _pages/*)
	scripts/genxml sitemap > $@

feed.xml: scripts/genxml $(wildcard _posts/*)
	scripts/genxml feed > $@

_data/git.yml: scripts/gengit .git
	scripts/gengit > $@

_data/stats.yml: scripts/genstats $(wildcard _posts/*)
	scripts/genstats > $@

_data/projects.yml: scripts/genprojects $(wildcard _posts/*)
	scripts/genprojects > $@

bin/blog: download

.PHONY: $(SCRIPTS)
$(SCRIPTS):
	@scripts/$@

.PHONY: clean
clean:
	rm -rf _data/*
	rm -rf feed.xml sitemap.xml
	rm -rf _site
	rm -rf bin/blog
	rm -rf $(BINARY_TARGETS)

.PHONY: binaries
binaries: $(BINARY_TARGETS)
bin/blog-%: $(wildcard src/*.go)
	GOOS=$* go build -o $@ src/*.go

.PHONY: serve
serve: newsite site
	bundle exec jekyll serve

.PHONY: info
info: bin/blog
	@bin/blog -info -version

.PHONY: patch
patch:
	@bin/blog-bump patch

.PHONY: test
test: bin/blog
	go test ./...

.PHONY: download
download:
	@bin/blog-download
