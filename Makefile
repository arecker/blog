ARGS := \
  --site-title "Hey Reader!" \
  --site-description "personal online journal of Alex Recker" \
  --site-domain www.alexrecker.com \
  --site-author "$(shell git config user.name)" \
  --site-email "$(shell git config user.email)"

.PHONY: all
all: test lint build

.PHONY: build
build: venv/bin/python
	@echo "==> building website"
	./venv/bin/python ./main.py $(ARGS)

venv/bin/python: requirements.txt
	@echo "==> generating local python"
	rm -rf ./venv
	python -m venv --copies ./venv
	./venv/bin/pip install --upgrade --quiet pip
	./venv/bin/pip install --quiet -r requirements.txt

.PHONY: clean
clean:
	@echo "==> cleaning old artifacts"
	rm -rf ./www/*.xml
	rm -rf ./www/*.html
	rm -rf ./venv

.PHONY: lint
lint: venv/bin/python
	@echo "==> checking code style"
	./venv/bin/flake8 --doctests --color never --extend-exclude "venv/*" .

.PHONY: test
test: venv/bin/python
	@echo "==> running unit tests"
	./venv/bin/python -m unittest discover -q

PUBLISH_TAG := entry-$(shell date '+%Y-%m-%d')
.PHONY: publish
publish:
	git add -A
	git commit -m "publish new entry: $(PUBLISH_TAG)"
	git tag "$(PUBLISH_TAG)"
	git push origin --tags
	git push origin "master:master"
