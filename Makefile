SCRIPTS = $(notdir $(basename $(wildcard scripts/*)))
STATIC_SOURCES = $(shell scripts/static sources)
STATIC_TARGETS = $(shell scripts/static targets)

.PHONY: all
all: static


.PHONY: static



.PHONY: clean
clean:
	rm -rf www/*

.PHONY: $(SCRIPTS)
$(SCRIPTS):
	scripts/$@
