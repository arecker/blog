.PHONY: all
all: test build

PYTHON_CMD := python -m src

.PHONY: build
build:
	$(PYTHON_CMD) --verbose

.PHONY: test
test:
	python -m unittest

.phony: clean
clean:
	rm -rf ./www/*.xml
	rm -rf ./www/*.html
	rm -rf ./venv

venv:
	$$(which python) -m venv ./venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install --upgrade jinja2

.phony: new
new: venv
	./build.py

PUBLISH_TAG := entry-$(shell date '+%Y-%m-%d')
.PHONY: publish
publish:
	git add -A
	git commit -m "publish new entry: $(PUBLISH_TAG)"
	git tag "$(PUBLISH_TAG)"
	git push origin --tags
	git push origin "master:master"
