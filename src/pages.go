package main

import "io/ioutil"

func Pages() ([]Page, error) {
	var pages []Page

	files, err := ioutil.ReadDir(PagesDir)
	if err != nil {
		return pages, err
	}

	for _, file := range files {
		if !file.IsDir() {
			pages = append(pages, NewPage(file))
		}
	}

	return pages, nil
}
