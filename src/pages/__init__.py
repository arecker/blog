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


@register_entry_listing(filename='antijournal.html', title='Anti-Journal', description='private journal entries re-published')
def antijournal_entries(entries=[]):
    return [e for e in entries if e.description.startswith('anti-journal')]


@register_entry_listing(filename='homework.html', title='From the Homework Vault', description='old homework assignments re-published')
def homework_entries(entries=[]):
    return [e for e in entries if e.description.startswith('from the homework vault')]


@register_entry_listing(filename='lookingback.html', title='Looking Back', description='special journal entries that look back in time')
def lookingback_entries(entries=[]):
    return [e for e in entries if e.description.startswith('looking back on')]


@register_entry_listing(filename='confessions.html', title='Confessions', description='juicy, embarassing secrets brought to light')
def confessions_entries(entries=[]):
    return [e for e in entries if e.description.startswith('confessions:')]


@register_entry_listing(filename='stories.html', title='Stories', description='miscellaneous stories about topics')
def specials_entries(entries=[]):
    def is_story(entry):
        desc = entry.description
        
        if desc.startswith('stories about') or desc.startswith('some stories about'):
            return True

    return list(filter(is_story, entries))
