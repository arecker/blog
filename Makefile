all: test build .git/hooks/pre-commit

.git/hooks/pre-commit:
	@echo "==> installing pre-commit hook"
	echo "python -m blog.hook" > $@
	chmod +x $@

.PHONY: build
build: clean
	@echo "==> build"
	python -m blog.build --dir-www ./www --dir-entries ./entries --dir-data ./data

.PHONY: test
test:
	@echo "==> test"
	python -m unittest

.PHONY: publish
publish:
	@echo "==> publish"
	git add -A
	git commit -m "publish: $$(date '+%Y-%m-%d')"
	git tag "entry-$$(date '+%Y-%m-%d')"
	git push origin "entry-$$(date '+%Y-%m-%d')"
	git push origin master:master

.PHONY: images
images:
	@echo "==> images"
	python -m blog.images --dir-www ./www

.PHONY: clean
clean:
	@echo "==> clean"
	rm -rf www/*.html
	rm -rf www/*.xml
