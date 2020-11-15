#!/usr/bin/env bash
set -e

log() {
    echo "resize.sh: $@" 1>&2;
}

here() {
    cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd
}

check_installed() {
    if ! command -v "$1" &> /dev/null
    then
	log "$1 command not available!"
	exit 1
    fi
}

is_too_big() {
    local max="800"
    if [[ "$(identify -format %wx%h $1)" =~ ^([0-9]+)x([0-9]+) ]]; then
	local height="${BASH_REMATCH[1]}"
	local width="${BASH_REMATCH[2]}"
	[[ (( "$width" > "$max" )) || (("$heigth" > "$max")) ]]
    else
	log "error checking size of $1"
	exit 1
    fi
}

for cmd in convert identify; do
    check_installed "$cmd"
done

for image in $(find $(here)/../images -type f); do
    if is_too_big "$image"; then
	log "resizing $image"
	convert "$image" -resize "800x800" "$image"
    fi
done
