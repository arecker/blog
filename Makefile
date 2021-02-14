.PHONY: all
all: entries images

.PHONY: entries
ENTRY_SOURCES := $(wildcard _posts/*.md)
ENTRY_TARGETS := $(patsubst _posts/%-entry.md, www/%.html, $(ENTRY_SOURCES))
entries: $(ENTRY_TARGETS)

www/%.html : %.md pandoc/template.html
	@echo $@ $^

.PHONY: images
images:
	cp -R images www/

SERVE_COMMANDS = up down
.PHONY: $(SERVE_COMMANDS)
$(SERVE_COMMANDS):
	scripts/serve.bash $@
