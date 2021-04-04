COMMANDS = serve
PAGE_TARGETS = www/2019-07-02.html
STATIC_SOURCES = $(shell scripts/static-sources)
STATIC_TARGETS = $(addprefix www/, $(STATIC_SOURCES))

.PHONY: all
all: static $(PAGE_TARGETS)

.PHONY: static
static: $(STATIC_TARGETS)
$(STATIC_TARGETS): $(STATIC_SOURCES)
	rm -rf $@ && cp -r $(notdir $@) $@

$(PAGE_TARGETS): _posts/2019-07-02-entry.md
	scripts/render --from $^ --to $@

.PHONY: clean
clean:
	rm -rf $(STATIC_TARGETS)
	rm -rf $(PAGE_TARGETS)

.PHONY: $(COMMANDS)
$(COMMANDS):
	scripts/$@
