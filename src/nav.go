package main

import (
	"log"
	"sort"
)

func Nav(allPages []Page) []string {
	var navPages []Page
	var navList []string

	navMap := make(map[string]int)

	for _, page := range allPages {
		index, err := page.NavIndex()
		if err != nil {
			log.Printf("couldn't parse nav index for page %s, %s", page.SourceFileName, err)
		} else if index != 0 {
			navPages = append(navPages, page)
			navMap[page.SourceFileName] = index
		}
	}

	sort.SliceStable(navPages, func(i, j int) bool {
		return navMap[navPages[i].SourceFileName] < navMap[navPages[j].SourceFileName]
	})

	for _, page := range navPages {
		navList = append(navList, page.TargetFileName)
	}

	return navList
}
