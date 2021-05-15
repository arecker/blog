package main

import "io/ioutil"

func Entries() ([]Entry, error) {
	var entries []Entry

	files, err := ioutil.ReadDir(EntriesDir)
	if err != nil {
		return entries, err
	}

	for _, file := range files {
		if !file.IsDir() {
			entries = append(entries, NewEntry(file))
		}
	}

	return entries, nil
}
