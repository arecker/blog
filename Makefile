.PHONY: all
all: jsonnet test build

.PHONY: clean
clean:
	rm -rf data/*.json

JSONNET_SOURCES := $(wildcard jsonnet/*.jsonnet)
JSONNET_TARGETS := $(patsubst jsonnet/%.jsonnet, data/%.json, $(JSONNET_SOURCES))
jsonnet: $(JSONNET_TARGETS)
data/%.json: jsonnet/%.jsonnet $(JSONNET_SOURCES)
	jsonnet $< > $@ && touch $@

PYTHON_CMD := pipenv run python -m src \
--dir-data ./data \
--dir-entries ./entries \
--dir-www ./www

.PHONY: build
build:
	$(PYTHON_CMD) --verbose

COMMANDS := help
.PHONY: $(COMMANDS)
$(COMMANDS):
	$(PYTHON_CMD) --$@

.PHONY: test
test:
	pipenv run python -m unittest

PUBLISH_TAG := entry-$(shell date '+%Y-%m-%d')
.PHONY: publish
publish:
	git add -A
	git commit -m "publish new entry: $(PUBLISH_TAG)"
	git tag "$(PUBLISH_TAG)"
	git push origin --tags
	git push origin "master:master"
