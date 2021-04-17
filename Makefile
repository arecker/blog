MAKEFLAGS += --no-builtin-rules

.PHONY: all
all: entries

entries: www/2020-01-02.html
www/%.html: _posts/%-entry.md
	txt2html --infile "$^" --outfile "$@"

.PHONY: clean
clean:
	rm -rf www/*

SCRIPTS := $(notdir $(wildcard scripts/*))
.PHONY: $(SCRIPTS)
$(SCRIPTS):
	@scripts/$@
