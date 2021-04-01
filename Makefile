COMMANDS = serve
STATIC_SOURCES = $(shell scripts/static-sources)
STATIC_TARGETS = $(addprefix www/, $(STATIC_SOURCES))

.PHONY: all
all: static www/2019-07-02.html

.PHONY: static
static: $(STATIC_TARGETS)
$(STATIC_TARGETS): $(STATIC_SOURCES)
	rm -rf $@ && cp -r $(notdir $@) $@

www/2019-07-02.html: _posts/2019-07-02-entry.md
	scripts/render --from $^ --to $@

.PHONY: clean
clean:
	rm -rf $(STATIC_TARGETS)

.PHONY: $(COMMANDS)
$(COMMANDS):
	scripts/$@
