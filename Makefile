.PHONY: all
all: entries images

.PHONY: entries
ENTRY_SOURCES := $(wildcard _posts/*.md)
ENTRY_TARGETS := $(patsubst _posts/%-entry.md, www/%.html, $(ENTRY_SOURCES))
entries: $(ENTRY_TARGETS)

www/%.html: _posts/%-entry.md scripts/pandoc-build.bash pandoc/template.html pandoc/entry.lua
	scripts/pandoc-build.bash $*

.PHONY: clean
clean:
	rm -rf www/*.html

.PHONY: images
images:
	cp -R images www/

SERVE_COMMANDS = up down
.PHONY: $(SERVE_COMMANDS)
$(SERVE_COMMANDS):
	scripts/serve.bash $@
