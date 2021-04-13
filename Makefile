STATIC_SOURCES := $(shell scripts/statics)
STATIC_TARGETS := $(addprefix www/,$(STATIC_SOURCES))
SCRIPTS := $(notdir $(wildcard scripts/*))

.PHONY: all
all: static
# all:
#	@echo $(STATIC_SOURCES)

.PHONY: static
static: $(STATIC_TARGETS)
$(STATIC_TARGETS): $(STATIC_SOURCES)
	rm -rf $@ && cp -r $(notdir $@) $@

.PHONY: clean
clean:
	rm -rf www/*

.PHONY: $(SCRIPTS)
$(SCRIPTS):
	@scripts/$@
