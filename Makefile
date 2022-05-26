JSONNET_SOURCES = $(wildcard jsonnet/*.jsonnet)
JSONNET_TARGETS := $(patsubst jsonnet/%.jsonnet, data/%.json, $(JSONNET_SOURCES))

PYTHON_CMD := python -m src \
  --dir-entries ./entries \
  --dir-data ./data \
  --dir-www ./www

all: test build .git/hooks/pre-commit $(JSONNET_TARGETS)

data/%.json: jsonnet/%.jsonnet $(JSONNET_SOURCES)
	jsonnet $< > $@ && touch $@

.git/hooks/pre-commit:
	echo "python -m src.hook" > $@
	chmod +x $@

.PHONY: build
build: clean $(JSONNET_TARGETS)
	python -m src --dir-www ./www --dir-entries ./entries --dir-data ./data

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

TWITTER_SECRETS := --twitter-consumer-api-key "$$(pass twitter/reckerbot/consumer-api-key)" \
	           --twitter-consumer-api-secret-key "$$(pass twitter/reckerbot/consumer-api-secret-key)" \
	           --twitter-access-token "$$(pass twitter/reckerbot/access-token)" \
	           --twitter-access-token-secret "$$(pass twitter/reckerbot/access-token-secret)"
.PHONY: tweet
tweet:
	python -m src.tweet --dir-data ./data --dir-entries ./entries $(TWITTER_SECRETS)

.PHONY: share
share:
	python -m src.share --dir-data ./data --dir-entries ./entries $(SLACK_SECRETS) $(TWITTER_SECRETS)

.PHONY: clean
clean:
	rm -rf data/*.json
	rm -rf www/*.html
	rm -rf www/*.xml

NETLIFY_SECRETS := --netlify-token "$$(pass netlify/jenkins)"
.PHONY: deploy
deploy: test build
	python -m src.deploy --dir-data ./data --dir-www ./www $(NETLIFY_SECRETS)

.PHONY: morning
morning: publish deploy share

.PHONY: help
help:
	$(PYTHON_CMD) --help

.PHONY: fixup
fixup:
	$(PYTHON_CMD) --fixup
