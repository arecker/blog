package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
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
	dataFlag := flag.Bool("data", false, "Generate website data.")

	setupLogging()
	setupConfig()

	flag.Parse()

	if !(*versionFlag || *infoFlag || *dataFlag) {
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

	if *dataFlag {
		pages, err := Pages()
		if err != nil {
			log.Fatal(err)
		}
		log.Printf("generating data - nav.json")
		navPages := Nav(pages)
		if err := writeNav(navPages); err != nil {
			log.Fatal(err)
		}
	}
}

func writeNav(pageList []string) error {
	content, err := json.MarshalIndent(pageList, "", "  ")
	if err != nil {
		return err
	}

	navTarget := path.Join(DataDir, "nav.json")

	err = ioutil.WriteFile(navTarget, content, 0644)
	return err
}

func printDirectoryInfo(name string, path string) {
	files, size, err := Files(path)
	if err != nil {
		log.Fatal(err)
	}

	log.Printf(`%d %s (%s)`, len(files), name, size)
}
