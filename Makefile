.PHONY: all
all: git jsonnet secrets test build

.PHONY: clean
clean:
	rm -rf secrets/*.json
	rm -rf data/*.json
	rm -rf www/*.html
	rm -rf www/*.xml

JSONNET_SOURCES := $(wildcard jsonnet/*.jsonnet)
JSONNET_TARGETS := $(patsubst jsonnet/%.jsonnet, data/%.json, $(JSONNET_SOURCES))
jsonnet: $(JSONNET_TARGETS)
data/%.json: jsonnet/%.jsonnet $(JSONNET_SOURCES)
	jsonnet $< > $@ && touch $@

SECRETS := twitter netlify slack
SECRET_TARGETS := $(patsubst %,secrets/%.json, $(SECRETS))
secrets: $(SECRET_TARGETS)
secrets/%.json:
	pass blog/$* > $@

PYTHON_CMD := python -m src \
--dir-data ./data \
--dir-entries ./entries \
--dir-secrets ./secrets \
--dir-www ./www

git: .git/hooks/pre-commit
.git/hooks/pre-commit:
	echo '$(PYTHON_CMD) --hook' > $@ && chmod +x $@

.PHONY: build
build:
	$(PYTHON_CMD)

COMMANDS := deploy share slack tweet help fixup
.PHONY: $(COMMANDS)
$(COMMANDS):
	$(PYTHON_CMD) --$@

.PHONY: test
test:
	python -m unittest
