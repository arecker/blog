MAKEFLAGS += --no-builtin-rules

PAGE_SOURCES := $(wildcard _pages/*)
PAGE_TARGETS := $(addprefix www/,$(notdir $(PAGE_SOURCES)))
ENTRY_SOURCES := $(wildcard _posts/*)
ENTRY_TARGETS := $(addprefix www/,$(notdir $(patsubst %-entry.md,%.html, $(ENTRY_SOURCES))))
STATIC_SOURCES := $(shell scripts/static-sources)
STATIC_TARGETS := $(addprefix www/,$(STATIC_SOURCES))
SCRIPTS := $(notdir $(wildcard scripts/*))

.PHONY: all
all: static entries pages

.PHONY: static
static: $(STATIC_TARGETS)
$(STATIC_TARGETS): $(STATIC_SOURCES)
	rm -rf $@ && cp -r $(notdir $@) $@

.PHONY: entries
entries: $(ENTRY_TARGETS)
www/%.html: _posts/%-entry.md scripts/render
	scripts/render $^ > $@

.PHONY: pages
pages: $(PAGE_TARGETS)
www/%.html: _pages/%.html scripts/render
	scripts/render $^ > $@

.PHONY: clean
clean:
	rm -rf www/*

.PHONY: $(SCRIPTS)
$(SCRIPTS):
	@scripts/$@
