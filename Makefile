.PHONY: all
all: entries images

.PHONY: entries
ENTRY_SOURCES := $(wildcard _posts/*.md)
ENTRY_TARGETS := $(patsubst _posts/%-entry.md, www/%.html, $(ENTRY_SOURCES))
entries: $(ENTRY_TARGETS)

www/%.html : _posts/%-entry.md
	pandoc -s -o $@ $^

.PHONY: images
images:
	cp -R images www/

.PHONY: serve up down
SERVE := python3 -m http.server --directory www
serve:
	$(SERVE)
up:
	$(SERVE) > /dev/null &
down:
	kill -9 $$(ps ax | grep http.server | awk '{ print $$1 }' | head -1)
