log() {
    echo "test.sh: $@" 1>&2;
}

VERSION="$(cat VERSION)"

cd www

for file in ../entries/*.md; do
    target=$(echo $file | sed 's|.md|.html|' | sed 's|../entries/||')
    log "$file -> $target"
    pandoc --standalone \
	   --metadata revision="$VERSION" \
	   --lua-filter ../pandoc/filter.lua \
	   --template ../pandoc/layout.html \
	   -o "$target" \
	   "$file"
done
