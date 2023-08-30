from src.template import render_template


class Feed:
    """
    RSS feed object.

    `entries` should be a list of `Page` objects.

    `images` should be a list of `Image` objects.
    """
    def __init__(self, entries=[], images=[]):
        pass

    def render(self) -> str:
        """
        Render the body of feed.xml as a string
        """
        return render_template('feed.xml.j2')
