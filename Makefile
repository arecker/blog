.PHONY: all
all: test build

PYTHON_CMD := python -m src

.PHONY: build
build:
	$(PYTHON_CMD) --verbose

.PHONY: test
test:
	python -m unittest

.PHONY: clean
clean:
	rm -rf ./www/*.xml
	rm -rf ./www/*.html

.PHONY: new
new:
	./build.rb

PUBLISH_TAG := entry-$(shell date '+%Y-%m-%d')
.PHONY: publish
publish:
	git add -A
	git commit -m "publish new entry: $(PUBLISH_TAG)"
	git tag "$(PUBLISH_TAG)"
	git push origin --tags
	git push origin "master:master"
