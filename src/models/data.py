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

    return spiders
