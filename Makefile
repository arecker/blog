JSONNET_SOURCES = $(wildcard jsonnet/*.jsonnet)
JSONNET_TARGETS := $(patsubst jsonnet/%.jsonnet, data/%.json, $(JSONNET_SOURCES))

PYTHON_CMD := python -m src \
  --dir-data ./data \
  --dir-entries ./entries \
  --dir-secrets ./secrets \
  --dir-www ./www

SECRETS := twitter netlify slack
SECRET_TARGETS := $(patsubst %,secrets/%.json, $(SECRETS))

all: test build .git/hooks/pre-commit $(JSONNET_TARGETS) $(SECRET_TARGETS)

secrets/%.json:
	pass blog/$* > $@

data/%.json: jsonnet/%.jsonnet $(JSONNET_SOURCES)
	jsonnet $< > $@ && touch $@

.git/hooks/pre-commit:
	echo "$(PYTHON_CMD) --hook" > $@
	chmod +x $@

.PHONY: build
build: clean $(JSONNET_TARGETS) $(SECRET_TARGETS)
	$(PYTHON_CMD)

.PHONY: test
test:
	python -m unittest

.PHONY: publish
publish:
	python -m src.publish --dir-entries ./entries

ONE_OFFS := slack tweet help deploy fixup
.PHONY: $(ONE_OFFS)
$(ONE_OFFS):
	$(PYTHON_CMD) --$@ --dry

.PHONY: clean
clean:
	rm -rf secrets/*.json
	rm -rf data/*.json
	rm -rf www/*.html
	rm -rf www/*.xml

.PHONY: morning
morning: publish deploy slack tweet
