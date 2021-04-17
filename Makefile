MAKEFLAGS += --no-builtin-rules

.PHONY: all
all:

.PHONY: clean
clean:
	rm -rf www/*

SCRIPTS := $(notdir $(wildcard scripts/*))
.PHONY: $(SCRIPTS)
$(SCRIPTS):
	@scripts/$@
