DATA_SOURCES := $(wildcard jsonnet/*.jsonnet)
DATA_TARGETS := $(patsubst jsonnet/%.jsonnet, data/%.json, $(DATA_SOURCES))

.PHONY: all
all: $(DATA_TARGETS)

data/%.json: jsonnet/%.jsonnet
	jsonnet $< > $@ && touch $@

.PHONY: test
test:
	python -m unittest

.PHONY: install
install:
	pip install --editable .
