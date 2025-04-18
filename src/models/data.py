import collections
import json
import pathlib
import datetime
import dataclasses

from . import Image


def load_data(name, data_dir: str | pathlib.Path):
    data_dir = pathlib.Path(data_dir)
    data_file = data_dir / f'{name}.json'
    with data_file.open('r') as f:
        return json.load(f)


@dataclasses.dataclass
class Game:
    """A Game"""
    slug: str
    """A slugified version of the name to act as an ID"""

    description: str
    """A short description of the game"""

    image: Image
    """The game's image (an `Image`)"""

    url: str
    """A url link to the game download"""

    @property
    def title(self) -> str:
        """A title cased version of the slug for display."""
        return self.slug.title()


@dataclasses.dataclass
class Spider:
    """A Spider"""
    personal: str
    """The spider's personal name (e.g. *Spidey*)"""

    common: str
    """The spider's species common name (e.g. *Mexican Rose Grey*)"""

    scientific: str
    """The spider's species scientific name (e.g. *Tlitiocatl verdezi*)"""

    image: Image
    """The spider's picture (an `Image`)"""

    acquired: datetime.datetime
    """The day the spider was acquired"""

    deceased: datetime.datetime
    """The day the spider died"""

    endemic: str
    """The spider's natural endemic region (e.g. *Mexico - Southern Guerrero and eastern Oaxaca*)"""


def load_games(data_dir: str | pathlib.Path, images=[]) -> list[Game]:
    """Load games from the `data_dir`

    Games are defined in `data/games.json` in this format:

    ```json
    [
     {
      "description": "fight a bear",
      "image": "2025-04-16-bear-fight.png",
      "slug": "bear-fight",
      "url": "https://www.bear-fight-game.biz"
     },
    ]
    ```

    This function converts it into a list of `Game` objects.

    Pass in site a list of site `Image` objects so the game's image
    can be associated.

    ```python
    games = load_games('./data', images=[])
    ```
    """
    games = []

    for obj in load_data('games', data_dir):
        try:
            image = next((
                img for img in images if img.filename == obj['image']
            ))
        except StopIteration:
            raise ValueError(f'could not find game image \"{obj["image"]}\"')

        kwargs = obj
        kwargs['image'] = image
        game = Game(**kwargs)
        games.append(game)

    return games


def load_spiders(data_dir: str | pathlib.Path, images=[]) -> list[Spider]:
    """Load spiders from the `data_dir`.

    Spiders are defined in `data/spiders.json` in this format:

    ```json
    [
      {
        "acquired": [
           5,
           7,
           2021
        ],
        "common": "Mexican Rose Grey",
        "deceased": [
           26,
           7,
           2024
        ],
        "endemic": "Mexico - Southern Guerrero and eastern Oaxaca",
        "image": "2023-06-26-spidey.jpg",
        "personal": "Spidey",
        "scientific": "Tlitocatl verdezi"
      }
    ]
    ```
    This function reads the same data and converts it into a list of
    `Spider` objects in the order they were acquired.

    Pass in site a list of site `Image` objects so the spider's image
    can be associated.

    ```python
    spiders = load_spiders('./data')
    ```
    """
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
    """Generate stats from a list of `spiders`.

    Returns a `SpiderStats` containing some miscellaneous
    stats.

    ```python
    stats = load_spider_stats(spiders)
    ```
    """
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
