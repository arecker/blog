.phony: all
all: test

.phony: test
test:
	python -m unittest discover
