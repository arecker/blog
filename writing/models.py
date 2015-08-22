from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse

from uuid import uuid4
import markdown
import bs4


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(published=True)


class Post(models.Model):
    objects = PostQuerySet.as_manager()

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid4,
        unique=True,
        editable=False
    )
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    date = models.DateField(default=timezone.now)
    published = models.BooleanField(default=False)
    description = models.TextField(max_length=200, blank=True, null=True)
    body = models.TextField(blank=True, null=True)

    # Images
    cover_image_url = models.URLField(
        verbose_name='Cover Image URL',
        null=True,
        blank=True
    )
    cover_image_file = models.ImageField(
        verbose_name='Cover Image',
        upload_to='covers/',
        null=True,
        blank=True
    )
    meta_image_url = models.URLField(
        verbose_name='Meta Image URL',
        null=True,
        blank=True
    )
    meta_image_file = models.ImageField(
        verbose_name='Meta Image',
        upload_to='metas/',
        null=True,
        blank=True
    )

    # Helpers
    @property
    def meta_image(self):
        if self.meta_image_file:
            return self.meta_image_file.url
        return self.meta_image_url

    @property
    def cover_image(self):
        if self.cover_image_file:
            return self.cover_image_file.url
        return self.cover_image_url

    @classmethod
    def convert_alts_to_captions(cls, html):
        """
        Converts alt attributes to captions
        takes in one of these:
        <img src="src.jpg" alt="This is an image" />
        and returns one of these:
        <figure class="image">
            <img src="src.jpg" alt="This is an image" />
            <figcaption>This is an image</figcaption>
        </figure>
        """
        soup = bs4.BeautifulSoup(html)
        imgs = soup.find_all('img')
        for tag in imgs:
            try:
                alt = tag['alt']
            except KeyError:
                alt = None
            tag.wrap(soup.new_tag('figure', {'class': 'image'}))
            tag.parent['class'] = 'image'
            tag.insert_after(soup.new_tag('figcaption'))
            if alt:
                tag.next_sibling.string = alt
        return soup.prettify()

    @property
    def body_html(self):
        return self.convert_alts_to_captions(
            markdown.Markdown().convert(self.body)
        )

    # Representation
    def __unicode__(self):
        if self.published:
            return self.title
        return '{0} (draft)'.format(self.title)

    def get_absolute_url(self):
        return reverse(
            'post-detail',
            args=[str(self.slug)]
        )

    class Meta:
        ordering = ('-date',)
        get_latest_by = 'date'
