import random

import jinja2


template_loader = jinja2.FileSystemLoader(searchpath='./templates')
template_env = jinja2.Environment(loader=template_loader)


def register(func):
    template_env.globals[func.__name__] = func


def render_template(template_name: str, context={}):
    """
    Render a template into a string.
    """
    template = template_env.get_template(template_name)
    return template.render(**context)


@register
def on_this_date(today, entries):
    def same_date(e):
        same_month = e.date.month == today.month
        same_day = e.date.day == today.day
        different_year = e.date.year != today.year
        return same_month and same_day and different_year

    matching = filter(same_date, entries)

    try:
        return random.choice(list(matching))
    except IndexError:
        return None


@register
def find_random_napkin(images):
    try:
        return random.choice([i for i in images if 'napkin' in (i.slug or '')])
    except IndexError:
        return None


@register
def find_random_entry_with_banner(entries):
    return random.choice([e for e in entries if e.banner])


@register
def find_napkins(images):
    def is_napkin(image):
        return 'napkin' in (image.slug or '')

    napkins = list(filter(is_napkin, images))
    group_by = 3
    return [napkins[i:i + group_by] for i in range(0, len(napkins), group_by)]


@register
def find_looking_back_entries(entries):
    return [e for e in entries if e.description.startswith('looking back on')]


@register
def find_homework(entries):
    def is_homework(e):
        return e.description.startswith('from the homework vault:')

    return list(filter(is_homework, entries))


@register
def find_anti_journals(entries):
    def is_anti(e):
        return e.description.startswith('anti-journal')

    return list(filter(is_anti, entries))
