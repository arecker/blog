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

	log.Printf("Hello!  I'm blog, v%s.  Let's get started.", VERSION)
	entries, err := Entries()
	if err != nil {
		log.Fatal(err)
	}

	pages, err := Pages()
	if err != nil {
		log.Fatal(err)
	}

	log.Printf(`First, some info.  This website has %d entries and %d pages`, len(entries), len(pages))

	navList := Nav(pages)
	log.Printf(`The pages in the navbar are as follows: %s`, strings.Join(navList, ", "))
}
