package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"path"
	"runtime"
)

var (
	RootDir    string
	EntriesDir string
	PagesDir   string
	DataDir    string
	ImagesDir  string
	VideosDir  string
	AudiosDir  string
	ScriptsDir string
)

type logWriter struct{}

func (writer logWriter) Write(bytes []byte) (int, error) {
	return fmt.Printf("BLOG: %s", string(bytes))
}

func setupLogging() {
	log.SetFlags(0)
	log.SetOutput(new(logWriter))
}

func setupConfig() {
	val, present := os.LookupEnv("BLOG_PATH")
	if present {
		RootDir = val
	} else {
		RootDir = "."
	}

	EntriesDir = path.Join(RootDir, "_posts")
	PagesDir = path.Join(RootDir, "_pages")
	DataDir = path.Join(RootDir, "_data")
	ImagesDir = path.Join(RootDir, "images")
	VideosDir = path.Join(RootDir, "vids")
	AudiosDir = path.Join(RootDir, "audio")
}

func main() {
	versionFlag := flag.Bool("version", false, "Print version information.")
	infoFlag := flag.Bool("info", false, "Print website information.")

	setupLogging()
	setupConfig()

	flag.Parse()

	if !(*versionFlag || *infoFlag) {
		log.Printf("no commands were specified, try 'blog -help'")
		os.Exit(1)
	}

	if *versionFlag {
		log.Printf("running v%s (%s)", VERSION, runtime.Version())
	}

	if *infoFlag {
		printDirectoryInfo("entries", EntriesDir)
		printDirectoryInfo("pages", PagesDir)
		printDirectoryInfo("images", ImagesDir)
		printDirectoryInfo("vids", VideosDir)
		printDirectoryInfo("audios", AudiosDir)
	}
}

func printDirectoryInfo(name string, path string) {
	files, size, err := Files(path)
	if err != nil {
		log.Fatal(err)
	}

	log.Printf(`%d %s (%s)`, len(files), name, size)
}
