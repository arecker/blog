package main

import (
	"bytes"
	"os/exec"
	"strings"
)

type GitData struct {
	Head        string `json:"git_head"`
	Summary     string `json:"git_head_summary"`
	ShortHead   string `json:"git_short_head"`
	CommitCount string `json:"git_commit_count"`
}

func Git() (GitData, error) {
	var data GitData
	var err error

	data.Head, err = runGitCommand(`rev-parse HEAD`)
	if err != nil {
		return data, err
	}

	data.Summary, err = runGitCommand(`log -1 --pretty=format:%s HEAD`)
	if err != nil {
		return data, err
	}

	data.ShortHead, err = runGitCommand(`rev-parse --short HEAD`)
	if err != nil {
		return data, err
	}

	data.CommitCount, err = runGitCommand(`rev-list --count master`)
	if err != nil {
		return data, err
	}

	return data, err
}

func runGitCommand(command string) (string, error) {
	var out bytes.Buffer
	cmd := exec.Command("git", strings.Split(command, " ")...)
	cmd.Stdout = &out
	err := cmd.Run()
	output := strings.TrimSuffix(out.String(), "\n")
	return output, err
}
