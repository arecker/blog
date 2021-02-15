#!/usr/bin/env bash

set -e

log() {
    echo "pandoc-build.bash: $@" 1>&2;
}

get_pages() {
    local output="$(ls _posts/ | grep -C 1 "$1-entry.md")"
    local lines="$(echo "$output" | wc -l)"
    local current="${1}.html"
    local last="$(echo "$output" | tail -1 | sed 's|-entry.md|.html|1')"
    local first="$(echo "$output" | head -1 | sed 's|-entry.md|.html|1')"
    if [ "$lines" == "3" ]; then
        echo "$first
$last"
    else
        if [ "$last" == "$current" ]; then
            echo "$fist
"
        elif [ "$first" == "$current" ]; then
            echo "
$last"
        fi
    fi
}

for slug in "2019-07-02" "2021-02-05" "2021-02-13"; do
    PAGES="$(get_pages $slug)"
    echo "previous: $(echo $PAGES | head -1)"
    echo "next: $(echo $PAGES | tail -1)"
    echo "---"
done

# pandoc \
#     -V filename="$1.html" \
#     -V git_head="$(git rev-parse HEAD)" \
#     -V git_short_head="$(git rev-parse --short HEAD)" \
#     -V git_summary="$(git log -1 --pretty=format:\"%s\" HEAD)" \
#     -V timestamp="$(date)" \
#     -V year="$(date +%Y)" \
#     -V paginate="true" \
#     -V next="$(get_next $1)" \
#     -V previous="$(get_previous $1)" \
#     --lua-filter pandoc/entry.lua \
#     --template pandoc/template.html \
#     -o www/${1}.html \
#     _posts/${1}-entry.md
