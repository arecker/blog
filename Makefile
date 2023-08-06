ARGS := \
  --site-domain www.alexrecker.com \
  --site-author "Alex Recker"

.PHONY: all
all: build

.PHONY: build
build: venv/bin/python
	@echo "==> building blog"
	./venv/bin/python -m src $(ARGS)

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

PUBLISH_TAG := entry-$(shell date '+%Y-%m-%d')
.PHONY: publish
publish:
	git add -A
	git commit -m "publish new entry: $(PUBLISH_TAG)"
	git tag "$(PUBLISH_TAG)"
	git push origin --tags
	git push origin "master:master"
