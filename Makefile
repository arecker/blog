.PHONY: all
all: test

.PHONY: test
test:
	python -m unittest discover

.PHONY: data
data:
	jsonnet -m . data.jsonnet
