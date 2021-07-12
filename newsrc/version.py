from newsrc import files


def version_string():
    with open(files.join('src/VERSION')) as f:
        return f.read().strip()
