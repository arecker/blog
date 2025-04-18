PYTHON_DETECTED = "$(shell python --version)"
PYTHON_DESIRED = "Python $(shell cat .tool-versions | grep python | awk '{ print $$2 }')"
ifneq ($(PYTHON_DETECTED), $(PYTHON_DESIRED))
$(error wanted $(PYTHON_DESIRED), detected $(PYTHON_DETECTED))
endif

ARGS := \
  --site-title "Hey Reader!" \
  --site-description "personal online journal of Alex Recker" \
  --site-domain "www.alexrecker.com" \
  --site-author "Alex Recker" \
  --site-email "alex@reckerfamily.com"

.PHONY: all
all: lint data test build

.PHONY: data
data:
	@echo "==> rendering data"
	jsonnet -m data data.jsonnet

.PHONY: build
build: venv/bin/python
	@echo "==> building website"
	./venv/bin/python -m src $(ARGS)

.PHONY: test
test: venv/bin/python
	@echo "==> running tests"
	./venv/bin/coverage run -m unittest discover -q
	./venv/bin/coverage html -d www/coverage -q

venv/bin/python: requirements.txt
	@echo "==> setting up python environment"
	rm -rf ./venv
	python -m venv --copies ./venv
	./venv/bin/pip install --upgrade --quiet pip
	./venv/bin/pip install --quiet -r requirements.txt

.PHONY: clean
clean:
	rm -rf ./www/*.xml
	rm -rf ./www/*.txt
	rm -rf ./www/*.html
	rm -rf ./venv

.PHONY: lint
lint: venv/bin/python
	@echo "==> linting code"
	./venv/bin/flake8 --doctests --color never --ignore=E501 --extend-exclude "venv/*" .

PUBLISH_TAG := entry-$(shell date '+%Y-%m-%d')
.PHONY: publish
publish:
	git add -A
	git commit -m "publish new entry: $(PUBLISH_TAG)"
	git tag "$(PUBLISH_TAG)"
	git push origin --tags
	git push origin "master:master"
