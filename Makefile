MAKEFLAGS += --no-builtin-rules -j10

.PHONY: all
all: bin/blog

bin/blog: go.mod $(wildcard src/*.go)
	go build -ldflags="-X 'main.VERSION=$(shell cat VERSION)'" -o $@ src/*.go

.PHONY: xml
XML_TARGETS := sitemap.xml feed.xml
xml: $(XML_TARGETS)
%.xml:
	scripts/genxml $* > $@

.PHONY: data
data: _data/stats.yml _data/projects.yml _data/git.json
_data/%.yml:
	scripts/gen$* > $@
_data/%.json:
	scripts/gen$* > $@

.PHONY: binaries
BINARY_TARGETS := $(addprefix bin/blog-, darwin linux freebsd)
binaries: $(BINARY_TARGETS)
bin/blog-%: $(wildcard src/*.go)
	GOOS=$* go build -ldflags="-X 'main.VERSION=$(shell cat VERSION)'" -o $@ src/*.go

BUMP_COMMANDS := major minor patch
.PHONY: $(BUMP_COMMANDS)
$(BUMP_COMMANDS):
	@bin/blog-bump $@

.PHONY: test
test: bin/blog
	go test ./...

.PHONY: thumbnails
thumbnails:
	@scripts/thumbnails

.PHONY: clean
clean:
	rm -rf _site
	rm -rf $(XML_TARGETS) _data/*
	rm -rf bin/blog $(BINARY_TARGETS)
