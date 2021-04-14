STATIC_SOURCES := $(shell scripts/statics)
STATIC_TARGETS := $(addprefix www/,$(STATIC_SOURCES))
SCRIPTS := $(notdir $(wildcard scripts/*))

.PHONY: all
all: static partials

.PHONY: static
static: $(STATIC_TARGETS)
$(STATIC_TARGETS): $(STATIC_SOURCES)
	rm -rf $@ && cp -r $(notdir $@) $@

.PHONY: partials
partials: partials/nav.html
partials/nav.html:
	scripts/nav > $@

.PHONY: clean
clean:
	rm -rf www/*
	rm -rf partials/*

.PHONY: $(SCRIPTS)
$(SCRIPTS):
	@scripts/$@
