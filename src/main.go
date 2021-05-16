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

	entries, err := Entries()
	if err != nil {
		log.Fatal(err)
	}
	_, entriesSize, err := Files(EntriesDir)
	if err != nil {
		log.Fatal(err)
	}

	pages, err := Pages()
	if err != nil {
		log.Fatal(err)
	}
	_, pagesSize, err := Files(PagesDir)
	if err != nil {
		log.Fatal(err)
	}

	images, imagesSize, err := Files(ImagesDir)
	if err != nil {
		log.Fatal(err)
	}

	videos, videosSize, err := Files(VideosDir)
	if err != nil {
		log.Fatal(err)
	}

	audios, audiosSize, err := Files(AudiosDir)
	if err != nil {
		log.Fatal(err)
	}

	navPages := Nav(pages)

	if *infoFlag {
		log.Printf(`using "%s" as BLOG_PATH`, RootDir)
		log.Printf(`%d entries (%s)`, len(entries), entriesSize)
		log.Printf(`%d pages (%s)`, len(pages), pagesSize)
		log.Printf(`%d images (%s)`, len(images), imagesSize)
		log.Printf(`%d vids (%s)`, len(videos), videosSize)
		log.Printf(`%d audios (%s)`, len(audios), audiosSize)
		log.Printf(`nav - %s`, navPages)
	}
}
