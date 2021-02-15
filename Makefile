.PHONY: all
all: pages entries images data

.PHONY: entries
ENTRY_SOURCES := $(wildcard _posts/*.md)
ENTRY_TARGETS := $(patsubst _posts/%-entry.md, www/%.html, $(ENTRY_SOURCES))
entries: $(ENTRY_TARGETS)

PAGE_SOURCES = $(wildcard pages/*.md)
PAGE_TARGETS = $(addprefix www/, $(addsuffix .html, $(basename $(notdir $(PAGE_SOURCES)))))
PAGE_TEMPLATES = $(patsubst www/%, pandoc/%, $(PAGE_TARGETS))
PAGE_DATA_FILES = $(patsubst www/%.html, data/page-%.json, $(PAGE_TARGETS))
pages: $(PAGE_TARGETS)

DATA_FILES = $(subst generate-, , $(notdir $(wildcard scripts/generate-*)))
DATA_FILE_TARGETS = $(addsuffix .json, $(addprefix data/, $(DATA_FILES)))
DATA_FILE_FLAGS = $(addprefix --metadata-file , $(DATA_FILE_TARGETS))
data: $(DATA_FILE_TARGETS) $(PAGE_DATA_FILES)
data/%.json : scripts/generate-% $(ENTRY_SOURCES) $(PAGE_SOURCES) .git
	scripts/generate-$* > data/$*.json

$(PAGE_DATA_FILES): $(PAGE_SOURCES) scripts/parse-page-data
	scripts/parse-page-data $(patsubst data/page-%.json, pages/%.md, $@) > $@

$(PAGE_TEMPLATES): $(PAGE_SOURCES) scripts/page-temp-template
	scripts/page-temp-template $@ > $@

$(PAGE_TARGETS): $(DATA_FILE_TARGETS) $(PAGE_SOURCES) $(PAGE_TEMPLATES) $(PAGE_DATA_FILES)
	pandoc $(DATA_FILE_FLAGS) \
	-f markdown_strict \
	--metadata-file $(patsubst www/%.html, data/page-%.json, $@) \
	--template $(@:www/%=pandoc/%) \
	-V filename=$(@:www/%=%) \
	-o $@ \
	$(patsubst www/%.html, pages/%.md, $@)

PANDOC_FILES = pandoc/template.html pandoc/entry.lua
PANDOC_FLAGS = --lua-filter pandoc/entry.lua --template pandoc/template.html
www/%.html: _posts/%-entry.md $(PANDOC_FILES) $(DATA_FILE_TARGETS)
	pandoc $(PANDOC_FLAGS) $(DATA_FILE_FLAGS) -V filename=$*.html -o www/$*.html _posts/$*-entry.md

.PHONY: debug
debug: $(PAGE_TEMPLATES)

.PHONY: clean
clean:
	rm -rf www/*.html
	rm -rf data/*.json

.PHONY: images
images:
	cp -R images www/

SERVE_COMMANDS = up down
.PHONY: $(SERVE_COMMANDS)
$(SERVE_COMMANDS):
	scripts/serve $@
