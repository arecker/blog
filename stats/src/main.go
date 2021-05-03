package main

import (
	"io/ioutil"
	"log"
)

const EntriesDir string = `../_posts/`

func main() {
	for _, file := range listEntries() {
		log.Printf("processing %s", file)
	}
}

func listEntries() []string {
	var files []string
	results, err := ioutil.ReadDir(EntriesDir)
	if err != nil {
		log.Fatal(err)
	}
	for _, result := range results {
		if !result.IsDir() {
			files = append(files, result.Name())
		}
	}
	return files
}
