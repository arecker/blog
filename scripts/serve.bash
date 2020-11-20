#!/usr/bin/env bash

set -e

log() {
    echo "serve.bash: $@" 1>&2;
}

remove_ga() {
    local ga_file="./www/assets/ga.js"
    log "deleting $ga_file"
    rm -rf "$ga_file"
}

serve() {
    local addr="0.0.0.0"
    local port="4000"
    local path="./www"
    log "serving $path -> ${addr}:${port}"
    python -m http.server -d "$path" -b "$addr" "$port"
}

remove_ga && serve
