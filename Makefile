.PHONY: all
all: entries

.PHONY: entries
ENTRY_SOURCES := $(wildcard _posts/*.md)
ENTRY_TARGETS := $(patsubst _posts/%-entry.md, www/%.html, $(ENTRY_SOURCES))
entries: $(ENTRY_TARGETS)

www/%.html : _posts/%-entry.md
	@echo $@

.PHONY: images
images:
	cp -R images www/
