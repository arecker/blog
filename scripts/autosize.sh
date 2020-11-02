#!/usr/bin/env bash
set -e

log() {
    echo "autosize.sh $1" 1>&2;
}

list_images() {
    find ./images -type f
}

needs_resize() {
    [[ "$(identify -format %h $1)" -gt "800" || "$(identify -format %w $1)" -gt "800" ]]
}

resize() {
    convert "$1" -resize "800x800" "$1"
}

for img in $(list_images); do
    if needs_resize "$img"; then
	log "resizing $img ($(identify -format %hx%w $img))"
	resize "$img"
    fi
done
