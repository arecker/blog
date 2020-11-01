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

    rev.sh ARG

    show: print version and exit
    <major|minor|patch>: increment version
EOF
}

render_version() {
    echo "$(cat ./revision/major).$(cat ./revision/minor).$(cat ./revision/patch)"
}

branch_is_master() {
    [[ "$(git rev-parse --abbrev-ref HEAD)" == "master" ]]
}

case "$1" in
    show)
	echo "v$(render_version)"
	exit
	;;
    major|minor|patch)
	log "incrementing $1 version"
	;;
    *)
	print_help
	exit
	;;
esac

VERSION_FILE="./revision/$1"

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

case "$1" in
    major)
	log "resetting minor"
	echo "0" > revision/minor
	log "resetting patch"
	echo "0" > revision/patch
	;;
    minor)
	log "resetting patch"
	echo "0" > revision/patch
	;;
esac

log "amending results to last commit"
git add -A && git commit --amend -C HEAD

NEWTAG="v$(render_version)"
log "creating tag $NEWTAG"
git tag "$NEWTAG"

log "pushing tags"
git push --tags

log "pushing commit history"
git push origin master:master
