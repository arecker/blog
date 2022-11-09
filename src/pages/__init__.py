from . import audio
from . import four_oh_four
from . import images
from . import index
from . import napkins
from . import quotes
from . import swears
from . import videos

from ..lib.pages import register_entry_listing


@register_entry_listing(filename='entries.html', title='Entries', description='complete archive of journal entries')
def all_entries(entries=[]):
    return entries
