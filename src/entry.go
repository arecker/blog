package main

import (
	"io/fs"
	"path"
)

type Entry struct {
	Page
	DateSlug string
}

func NewEntry(fileInfo fs.FileInfo) Entry {
	var entry Entry

	entry.SourceFileName = fileInfo.Name()
	entry.SourcePath = path.Join(EntriesDir, entry.SourceFileName)
	entry.DateSlug = entry.SourceFileName[0:10]

	return entry
}
