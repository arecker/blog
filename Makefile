.PHONY: all
all: entries images data

.PHONY: entries
ENTRY_SOURCES := $(wildcard _posts/*.md)
ENTRY_TARGETS := $(patsubst _posts/%-entry.md, www/%.html, $(ENTRY_SOURCES))
entries: $(ENTRY_TARGETS)

www/%.html: _posts/%-entry.md scripts/pandoc-entry pandoc/template.html pandoc/entry.lua
	scripts/pandoc-entry $*

PAGE_SOURCES = $(wildcard _pages/*.html)

DATA_FILES = $(subst generate-, , $(notdir $(wildcard scripts/generate-*)))
DATA_FILE_TARGETS = $(addsuffix .json, $(addprefix data/, $(DATA_FILES)))
DATA_FILE_FLAGS = $(addprefix --metadata-file , $(DATA_FILE_TARGETS))
data: $(DATA_FILE_TARGETS)
data/%.json : scripts/generate-% $(ENTRY_SOURCES) $(PAGE_SOURCES) .git
	scripts/generate-$* > data/$*.json

.PHONY: debug
debug:
	@echo $(DATA_FILE_FLAGS)

.PHONY: clean
clean:
	rm -rf www/*.html
	rm -rf $(DATA_FILE_TARGETS)

.PHONY: images
images:
	cp -R images www/

SERVE_COMMANDS = up down
.PHONY: $(SERVE_COMMANDS)
$(SERVE_COMMANDS):
	scripts/serve $@
