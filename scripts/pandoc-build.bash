#!/usr/bin/env bash

log() {
    echo "pandoc-build.bash: $@" 1>&2;
}

get_next() {
    ls _posts | sort | grep -C 1 "$1-entry.md" | tail -1 | sed 's|-entry.md|.html|1'
}

get_previous() {
    ls _posts | sort | grep -C 1 "$1-entry.md" | head -1 | sed 's|-entry.md|.html|1'
}

pandoc \
    -V filename="$1.html" \
    -V git_head="$(git rev-parse HEAD)" \
    -V git_short_head="$(git rev-parse --short HEAD)" \
    -V git_summary="$(git log -1 --pretty=format:\"%s\" HEAD)" \
    -V timestamp="$(date)" \
    -V year="$(date +%Y)" \
    -V paginate="true" \
    -V next="$(get_next $1)" \
    -V previous="$(get_previous $1)" \
    --lua-filter pandoc/entry.lua \
    --template pandoc/template.html \
    -o www/${1}.html \
    _posts/${1}-entry.md
