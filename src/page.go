package main

import (
	"io/fs"
	"io/ioutil"
	"path"
	"regexp"
	"strconv"
)

type Page struct {
	SourceFileName string
	SourcePath     string
	TargetFileName string
}

func NewPage(fileInfo fs.FileInfo) Page {
	var page Page

	page.SourceFileName = fileInfo.Name()
	page.SourcePath = path.Join(PagesDir, page.SourceFileName)
	page.TargetFileName = regexp.MustCompile(`\.md$`).ReplaceAllString(page.SourceFileName, ".html")

	return page
}

func (page *Page) Content() (string, error) {
	bytes, err := ioutil.ReadFile(page.SourcePath)
	if err != nil {
		return "", err
	}
	return string(bytes), err
}

func (page *Page) NavIndex() (int, error) {
	content, err := page.Content()
	if err != nil {
		return 0, err
	}

	p := regexp.MustCompile(`(?s)^---.*?\nnav: (?P<index>\d)\n.*?---`)

	if !p.MatchString(content) {
		return 0, nil
	}

	match := p.FindStringSubmatch(content)[1]

	index, err := strconv.Atoi(match)
	if err != nil {
		return 0, err
	}

	return index, err

}
