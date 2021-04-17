MAKEFLAGS += --no-builtin-rules -j10

.PHONY: all
all: entries

entries: $(patsubst _posts/%-entry.md, www/%.html, $(wildcard _posts/*))
www/%.html: _posts/%-entry.md
	scripts/strip-frontmatter "$^" | txt2html --outfile "$@"

SCRIPTS := thumbnails serve
.PHONY: $(SCRIPTS)
$(SCRIPTS):
	@scripts/$@

.PHONY: clean
clean:
	rm -rf www/*
