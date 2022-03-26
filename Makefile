DATA_SOURCES := $(wildcard jsonnet/*.jsonnet)
DATA_TARGETS := $(patsubst jsonnet/%.jsonnet, data/%.json, $(DATA_SOURCES))

.PHONY: all
all: .git/hooks/pre-commit $(DATA_TARGETS)

.git/hooks/pre-commit:
	ln scripts/pre-commit $@

data/%.json: jsonnet/%.jsonnet
	jsonnet $< > $@ && touch $@

.PHONY: test
test:
	python -m unittest

.PHONY: images
images:
	@./scripts/images

.PHONY: clean
clean:
	rm -rf .git/hooks/pre-commit
