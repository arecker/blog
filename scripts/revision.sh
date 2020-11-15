#!/usr/bin/env bash

set -e

log() {
    echo "revision.sh: $@" 1>&2;
}

here() {
    cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd
}

print_help() {
    cat <<EOF
revision.sh - the quick & nifty revision manager

Usage: revision.sh <major|minor|patch>
EOF
}

version_path() {
    echo "$(here)/../VERSION"
}

current_version() {
    cat "$(version_path)"
}

latest_tag() {
    git tag --sort version:refname | tail -1
}

annotation() {
    local changelog="$(git shortlog $(latest_tag)..HEAD)"
    cat <<EOF
revision.sh increment $1 version

${changelog}
EOF
}

increment_version() {
    if [[ "$(current_version)" =~ ^v([0-9]+)\.([0-9]+)\.([0-9]+) ]]; then
	local major="${BASH_REMATCH[1]}"
	local minor="${BASH_REMATCH[2]}"
	local patch="${BASH_REMATCH[3]}"
	case "$1" in
	    "major")
		major="$((major + 1))"
		minor="0"
		patch="0"
		;;
	    "minor")
		minor="$((minor + 1))"
		patch="0"
		;;
	    "patch")
		patch="$((patch + 1))"
		;;
	esac
	local new_version="v${major}.${minor}.${patch}"
	log "incrementing $(current_version) -> ${new_version}"
	echo "${new_version}" > "$(version_path)"
	git add "$(version_path)" && git commit --amend
	git tag -a "${new_version}" -m "$(annotation $1)"
	git push origin "${new_version}"
	log "${new_version} successfully published"
	exit 0
    else
	log "\"$(current_version) \"is an invalid version tag!"
	exit 1
    fi
}

case "$1" in
    "major"|"minor"|"patch")
	increment_version "$1"
	exit 0
	;;
    *)
	print_help
	exit 1
	;;
esac
