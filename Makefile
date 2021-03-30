COMMANDS = serve
STATIC_SOURCES = $(shell scripts/static-sources)
STATIC_TARGETS = $(addprefix www/, $(STATIC_SOURCES))

.PHONY: all
all: static

.PHONY: static
static: $(STATIC_TARGETS)
$(STATIC_TARGETS): $(STATIC_SOURCES)
	rm -rf $@ && cp -r $(notdir $@) $@

.PHONY: clean
clean:
	rm -rf $(STATIC_TARGETS)

.PHONY: $(COMMANDS)
$(COMMANDS):
	scripts/$@
