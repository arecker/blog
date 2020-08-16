def plural(n, singular, plural=None):
    plural = plural or singular + 's'

    if n == 1:
        return f'{n} {singular}'

    return f'{n} {plural}'
