#!/usr/bin/env bash

log() {
    echo "pandoc-build.bash: $@" 1>&2;
}

pandoc \
    -V filename="$*.html" \
    -V git_head="$(git rev-parse HEAD)" \
    -V git_short_head="$(git rev-parse --short HEAD)" \
    -V git_summary="$(git log -1 --pretty=format:\"%s\" HEAD)" \
    -V timestamp="$(date)" \
    -V year="$(date +%Y)" \
    --lua-filter pandoc/entry.lua \
    --template pandoc/template.html \
    -o www/${1}.html \
    _posts/${1}-entry.md
