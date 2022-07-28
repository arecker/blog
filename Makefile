.PHONY: all
all: git jsonnet test build

.PHONY: clean
clean:
	rm -rf data/*.json

JSONNET_SOURCES := $(wildcard jsonnet/*.jsonnet)
JSONNET_TARGETS := $(patsubst jsonnet/%.jsonnet, data/%.json, $(JSONNET_SOURCES))
jsonnet: $(JSONNET_TARGETS)
data/%.json: jsonnet/%.jsonnet $(JSONNET_SOURCES)
	jsonnet $< > $@ && touch $@

PYTHON_CMD := python -m src \
--dir-data ./data \
--dir-entries ./entries \
--dir-www ./www

git: .git/hooks/pre-commit
.git/hooks/pre-commit:
	echo '$(PYTHON_CMD) --hook' > $@ && chmod +x $@

.PHONY: build
build:
	$(PYTHON_CMD)

COMMANDS := deploy share slack help fixup
.PHONY: $(COMMANDS)
$(COMMANDS):
	$(PYTHON_CMD) --$@

.PHONY: test
test:
	python -m unittest

.PHONY: publish
publish:
	git add -A
	git commit -m 'publish new entry'
	git tag "entry-$$(date '+%Y-%m-%d')"
	git push origin --tags
	git push origin "master:master"
