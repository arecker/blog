import dataclasses
import datetime


@dataclasses.dataclass
class Page:
    filename: str
    title: str
    description: str
    contents: str

    banner: str = None
    date: datetime.datetime = None
