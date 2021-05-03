.PHONY: all

all: bin/stats

bin/stats: $(wildcard src/*.go) go.mod
	go build -o $@ ./...

.PHONY: run
run: bin/stats
	@./bin/stats

.PHONY: clean
clean:
	rm -rf bin/stats
