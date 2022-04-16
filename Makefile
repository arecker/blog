.PHONY: all
all: test

.PHONY: test
test:
	python -m unittest

.PHONY: install
install:
	pip install --editable .
