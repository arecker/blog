import random

import jinja2


template_loader = jinja2.FileSystemLoader(searchpath='./templates')
template_env = jinja2.Environment(loader=template_loader)


def render_template(template_name: str, context={}):
    """
    Render a template into a string.
    """
    template = template_env.get_template(template_name)
    return template.render(**context)


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


template_env.globals['on_this_date'] = on_this_date


def find_random_napkin(images):
    try:
        return random.choice([i for i in images if 'napkin' in (i.slug or '')])
    except IndexError:
        return None


template_env.globals['find_random_napkin'] = find_random_napkin


def find_random_entry_with_banner(entries):
    return random.choice([e for e in entries if e.banner])


template_env.globals['find_random_entry_with_banner'] = \
    find_random_entry_with_banner


def find_napkins(images):
    def is_napkin(image):
        return 'napkin' in (image.slug or '')

    napkins = list(filter(is_napkin, images))
    group_by = 3
    return [napkins[i:i+group_by] for i in range(0, len(napkins), group_by)]


template_env.globals['find_napkins'] = find_napkins
