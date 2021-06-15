package main

import (
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path"
	"runtime"
)

var (
	VERSION    string
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
	allFlag := flag.Bool("all", false, "Run everything.")
	versionFlag := flag.Bool("version", false, "Print version information.")
	infoFlag := flag.Bool("info", false, "Print website information.")
	dataFlag := flag.Bool("data", false, "Generate website data.")

	setupLogging()
	setupConfig()

	flag.Parse()

	if !(*allFlag || *versionFlag || *infoFlag || *dataFlag) {
		log.Printf("no commands were specified, try 'blog -help'")
		os.Exit(1)
	}

	if *versionFlag || *allFlag {
		log.Printf("running v%s (%s)", VERSION, runtime.Version())
	}

	if *infoFlag || *allFlag {
		printDirectoryInfo("entries", EntriesDir)
		printDirectoryInfo("pages", PagesDir)
		printDirectoryInfo("images", ImagesDir)
		printDirectoryInfo("vids", VideosDir)
		printDirectoryInfo("audios", AudiosDir)
	}

	if *dataFlag || *allFlag {
		pages, err := Pages()
		if err != nil {
			log.Fatal(err)
		}
		log.Printf("generating data - nav.json")
		navPages := Nav(pages)
		if err := writeData("nav.json", navPages); err != nil {
			log.Fatal(err)
		}

		log.Printf("generating data - git.json")
		gitData, err := Git()
		if err != nil {
			log.Fatal(err)
		}
		if err := writeData("git.json", gitData); err != nil {
			log.Fatal(err)
		}
	}
}

func writeData(filename string, data interface{}) error {
	content, err := JSON(data)
	if err != nil {
		return err
	}

	target := path.Join(DataDir, filename)
	err = ioutil.WriteFile(target, content, 0644)
	return err
}

func printDirectoryInfo(name string, path string) {
	files, size, err := Files(path)
	if err != nil {
		log.Fatal(err)
	}

	log.Printf(`%d %s (%s)`, len(files), name, size)
}
