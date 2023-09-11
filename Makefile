ARGS := \
  --site-title "Hey Reader!" \
  --site-description "personal online journal of Alex Recker" \
  --site-domain "www.alexrecker.com" \
  --site-author "Alex Recker" \
  --site-email "alex@reckerfamily.com"

.PHONY: all
all: lint build

.PHONY: build
build: venv/bin/python
	./venv/bin/python -m src $(ARGS)

venv/bin/python: requirements/prod.txt .python-version
	rm -rf ./venv
	python -m venv --copies ./venv
	./venv/bin/pip install --upgrade --quiet pip
	./venv/bin/pip install --quiet -r requirements/prod.txt

.PHONY: clean
clean:
	rm -rf ./www/*.xml
	rm -rf ./www/*.txt
	rm -rf ./www/*.html
	rm -rf ./venv

.PHONY: lint
lint: venv/bin/python
	./venv/bin/flake8 --doctests --color never --extend-exclude "venv/*" .

PUBLISH_TAG := entry-$(shell date '+%Y-%m-%d')
.PHONY: publish
publish:
	git add -A
	git commit -m "publish new entry: $(PUBLISH_TAG)"
	git tag "$(PUBLISH_TAG)"
	git push origin --tags
	git push origin "master:master"
