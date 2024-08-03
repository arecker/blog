import collections
import json
import pathlib
import datetime


def load_data(name, data_dir: str | pathlib.Path):
    data_dir = pathlib.Path(data_dir)
    data_file = data_dir / f'{name}.json'
    with data_file.open('r') as f:
        return json.load(f)


Spider = collections.namedtuple('Spider', [
    'personal',
    'common',
    'scientific',
    'image',
    'acquired',
    'deceased',
    'endemic',
])


def load_spiders(data_dir: str | pathlib.Path, images=[]) -> list[Spider]:
    spiders = []

    for obj in load_data('spiders', data_dir):
        try:
            image = next((
                img for img in images if img.filename == obj['image']
            ))
        except StopIteration:
            raise ValueError(f'could not find spider image \"{obj["image"]}\"')

        kwargs = obj
        kwargs['image'] = image
        day, month, year = kwargs['acquired']
        kwargs['acquired'] = datetime.datetime(year=year, month=month, day=day)
        if deceased := kwargs.get('deceased'):
            day, month, year = deceased
            kwargs['deceased'] = datetime.datetime(
                year=year, month=month, day=day)
        else:
            kwargs['deceased'] = None
        spider = Spider(**kwargs)
        spiders.append(spider)

    spiders.sort(key=lambda s: s.acquired)
    return spiders


SpiderStats = collections.namedtuple('SpiderStats', [
    'count_living',
    'count_deceased',
    'oldest_living',
    'youngest_living',
    'oldest_deceased',
    'youngest_deceased',
])


def load_spider_stats(spiders: list[Spider]) -> SpiderStats:
    stats = {}

    living = [s for s in spiders if not s.deceased]
    deceased = [s for s in spiders if s.deceased]

    stats['count_living'] = f'{len(living):,}'
    stats['count_deceased'] = f'{len(deceased):,}'

    today = datetime.datetime.now()
    living_by_age = list(sorted(living, key=lambda s: today - s.acquired, reverse=True))
    oldest_living = living_by_age[0]
    youngest_living = living_by_age[-1]
    stats['oldest_living'] = f'{oldest_living.personal} ({(today - oldest_living.acquired).days:,} days)'
    stats['youngest_living'] = f'{youngest_living.personal} ({(today - youngest_living.acquired).days:,} days)'

    deceased_by_age = list(sorted(deceased, key=lambda s: s.deceased - s.acquired, reverse=True))
    oldest_deceased = deceased_by_age[0]
    stats['oldest_deceased'] = f'{oldest_deceased.personal} ({(oldest_deceased.deceased - oldest_deceased.acquired).days:,} days)'
    youngest_deceased = deceased_by_age[-1]
    stats['youngest_deceased'] = f'{youngest_deceased.personal} ({(youngest_deceased.deceased - youngest_deceased.acquired).days:,} days)'
    return SpiderStats(**stats)
