.PHONY: all
all: test

.PHONY: test
test:
	python -m unittest

.PHONY: install
install:
	pip install --editable .

.PHONY: coverage
coverage:
	coverage run -m unittest discover
	coverage report -m
