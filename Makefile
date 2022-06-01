JSONNET_SOURCES = $(wildcard jsonnet/*.jsonnet)
JSONNET_TARGETS := $(patsubst jsonnet/%.jsonnet, data/%.json, $(JSONNET_SOURCES))

PYTHON_CMD := python -m src \
  --dir-data ./data \
  --dir-entries ./entries \
  --dir-secrets ./secrets \
  --dir-www ./www

SECRET_TARGETS := secrets/twitter.json secrets/netlify.json

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

SLACK_SECRETS := --slack-webhook-urls "$$(pass slack/reckers/webhook)"
.PHONY: slack
slack:
	python -m src.slack --dir-data ./data --dir-entries ./entries $(SLACK_SECRETS)

.PHONY: tweet
tweet:
	$(PYTHON_CMD) --tweet

.PHONY: clean
clean:
	rm -rf secrets/*.json
	rm -rf data/*.json
	rm -rf www/*.html
	rm -rf www/*.xml

.PHONY: deploy
deploy:
	$(PYTHON_CMD) --deploy

.PHONY: morning
morning: publish deploy slack tweet

.PHONY: help
help:
	$(PYTHON_CMD) --help

.PHONY: fixup
fixup:
	$(PYTHON_CMD) --fixup
