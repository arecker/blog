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
}

func main() {
	versionFlag := flag.Bool("version", false, "Print version information.")

	setupLogging()
	setupConfig()

	flag.Parse()

	if *versionFlag {
		log.Printf("running v%s (%s)", VERSION, runtime.Version())
		os.Exit(0)
	}

	if !*versionFlag {
		log.Printf("no commands were specified, try 'blog -help'")
	}

	// entries, err := Entries()
	// if err != nil {
	//	log.Fatal(err)
	// }

	// pages, err := Pages()
	// if err != nil {
	//	log.Fatal(err)
	// }

	// navList := Nav(pages)
}
