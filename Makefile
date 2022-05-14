all: test build .git/hooks/pre-commit

.git/hooks/pre-commit:
	@echo "==> installing pre-commit hook"
	echo "python -m src.hook" > $@
	chmod +x $@

.PHONY: build
build: clean
	@echo "==> build"
	python -m src.build --dir-www ./www --dir-entries ./entries --dir-data ./data

.PHONY: test
test:
	@echo "==> test"
	python -m unittest

.PHONY: publish
publish:
	python -m src.publish --dir-entries ./entries

.PHONY: images
images:
	@echo "==> images"
	python -m src.images --dir-www ./www

SLACK_SECRETS := --slack-webhook-urls "$$(pass slack/reckers/webhook)"
.PHONY: slack
slack:
	@echo "==> slack"
	python -m src.slack --dir-data ./data --dir-entries ./entries $(SLACK_SECRETS)

TWITTER_SECRETS := --twitter-consumer-api-key "$$(pass twitter/reckerbot/consumer-api-key)" \
	           --twitter-consumer-api-secret-key "$$(pass twitter/reckerbot/consumer-api-secret-key)" \
	           --twitter-access-token "$$(pass twitter/reckerbot/access-token)" \
	           --twitter-access-token-secret "$$(pass twitter/reckerbot/access-token-secret)"
.PHONY: tweet
tweet:
	@echo "==> tweet"
	python -m src.tweet --dir-data ./data --dir-entries ./entries $(TWITTER_SECRETS)

.PHONY: share
share:
	@echo "==> share"
	python -m src.share --dir-data ./data --dir-entries ./entries $(SLACK_SECRETS) $(TWITTER_SECRETS)

.PHONY: clean
clean:
	@echo "==> clean"
	rm -rf www/*.html
	rm -rf www/*.xml

NETLIFY_SECRETS := --netlify-token "$$(pass netlify/jenkins)"
.PHONY: deploy
deploy:
	python -m src.deploy --dir-data ./data --dir-www ./www $(NETLIFY_SECRETS)

.PHONY: jenkins
jenkins: test build deploy
