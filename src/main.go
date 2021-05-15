package main

import (
	"fmt"
	"log"
	"path"
	"strings"
)

var RootDir string = `.`
var EntriesDir string = path.Join(RootDir, "_posts")
var PagesDir string = path.Join(RootDir, "_pages")
var DataDir string = path.Join(RootDir, "_data")

type logWriter struct{}

func (writer logWriter) Write(bytes []byte) (int, error) {
	return fmt.Printf("BLOG: %s", string(bytes))
}

func setupLogging() {
	log.SetFlags(0)
	log.SetOutput(new(logWriter))
}

func main() {
	setupLogging()

	log.Println("Hello!  Let's get started.")
	entries, err := Entries()
	if err != nil {
		log.Fatal(err)
	}

	pages, err := Pages()
	if err != nil {
		log.Fatal(err)
	}

	log.Printf("We have %d entries, %d pages", len(entries), len(pages))

	navList := Nav(pages)
	log.Printf("Here is the site navigation: %s", strings.Join(navList, ", "))
}
