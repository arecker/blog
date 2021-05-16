package main

import (
	"fmt"
	"os"
	"path/filepath"
)

func fileSize(b int64) string {
	const unit = 1000
	if b < unit {
		return fmt.Sprintf("%d B", b)
	}
	div, exp := int64(unit), 0
	for n := b / unit; n >= unit; n /= unit {
		div *= unit
		exp++
	}
	return fmt.Sprintf("%.1f %cB",
		float64(b)/float64(div), "kMGTPE"[exp])
}

func Files(root string) ([]string, string, error) {
	var files []string
	var size int64
	err := filepath.Walk(root,
		func(path string, info os.FileInfo, err error) error {
			if err != nil {
				return err
			}
			if !info.IsDir() {
				files = append(files, path)
				size += int64(info.Size())
			}
			return nil
		})

	if err != nil {
		return files, "", err
	}

	return files, fileSize(size), err
}
