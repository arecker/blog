all: test build

.PHONY: build
build: clean
	@echo "==> build"
	python -m blog.build --dir-www ./www --dir-entries ./entries --dir-data ./data

.PHONY: test
test:
	@echo "==> test"
	python -m unittest

.PHONY: clean
clean:
	@echo "==> clean"
	rm -rf www/*.html
	rm -rf www/*.xml
