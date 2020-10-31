#!/usr/bin/env bash
set -e

log() {
    echo "rev.sh $1" 1>&2;
}

prompt() {
    local RESPONSE=""
    
    while true; do
	log "$1 [Yy/Nn]"
	read RESPONSE
	if [[ "$RESPONSE" =~ ^[YyNn]$ ]]; then break; fi
    done

    [[ "$RESPONSE" =~ ^[Yy]$ ]]
}

print_help() {
    cat << EOF

rev.sh - revision manager

Usage:

    rev.sh <major|minor|patch>

    First, increments the number in the corresponding file

        major: ./revision/major
        minor: ./revision/minor
        patch: ./revision/patch

    Creates a tag, 
EOF
}

render_version() {
    echo "$(cat ./revision/major).$(cat ./revision/minor).$(cat ./revision/patch)"
}

git_is_dirty() {
    [[ $(git diff --stat) != '' ]]
}

branch_is_master() {
    [[ "$(git rev-parse --abbrev-ref HEAD)" == "master" ]]
}

case "$1" in
    major|minor|patch)
	log "incrementing $1 version"
	;;
    *)
	print_help
	exit
	;;
esac

VERSION_FILE="./revision/$1"

if git_is_dirty; then
    log "git is dirty... clean it up, you slob!"
    exit 1
fi

if ! branch_is_master; then
    log "not on master branch"
    log "what are you, some kind of careless child?"
    exit 1
fi

if ! prompt "Are you sure?"; then
    log "aborting"
    exit 1
fi

BEFORE="$(cat $VERSION_FILE)"
AFTER="$((BEFORE + 1))"
log "incrementing $VERSION_FILE ($BEFORE -> $AFTER)"
echo "$AFTER" > "$VERSION_FILE"

log "committing results"
git add -A && git commit -m "rev.sh: $VERSION_FILE ($BEFORE -> $AFTER)"

NEWTAG="v$(render_version)"
log "creating tag $NEWTAG"
git tag "$NEWTAG"

log "pushing tags"
git push --tags

log "pushing commit history"
git push origin master:master
