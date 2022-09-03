import dataclasses
import datetime


@dataclasses.dataclass
class Page:
    filename: str
    title: str
    description: str

    banner: str = None
    date: datetime.datetime = None
