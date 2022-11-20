.PHONY: all
all: test build

PYTHON_CMD := python -m src

.PHONY: build
build:
	$(PYTHON_CMD) --verbose

COMMANDS := help
.PHONY: $(COMMANDS)
$(COMMANDS):
	$(PYTHON_CMD) --$@

.PHONY: test
test:
	python -m unittest

PUBLISH_TAG := entry-$(shell date '+%Y-%m-%d')
.PHONY: publish
publish:
	git add -A
	git commit -m "publish new entry: $(PUBLISH_TAG)"
	git tag "$(PUBLISH_TAG)"
	git push origin --tags
	git push origin "master:master"
