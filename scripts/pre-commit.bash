#!/usr/bin/env bash

log() {
    echo "resize.sh: $@" 1>&2;
}

new_files() {
    git status --short | grep -v '^ D' | awk '{ print $2 }'
}

new_images() {
    new_files | grep -i -E "\.(jpg|jpeg|bmp|png|svg)$"
}

available() {
    command -v "$1" &> /dev/null
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

if available "identify" && available "convert"; then
    for image in $(new_images); do
	if is_too_big "$image"; then
	    log "resizing $image"
	    convert "$image" -resize "800x800" "$image"
	    git add "$image"
	fi
    done
else
    log "imagemagick commands not available, skipping image resize..."
fi
