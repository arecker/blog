from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone
import markdown
import bs4


class PostManager(models.Manager):
    def published(self):
        return super(models.Manager, self).filter(published=True)

    def latest_published(self):
        """
        will return a one item list
        becuase the API is expecting something iterable
        """
        published = self.published()
        if published.count() < 1:
            return []
        return [published.latest()]


class Post(models.Model):
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    date = models.DateField(default=timezone.now)
    published = models.BooleanField(default=False)
    description = models.TextField(max_length=200, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    image_url = models.URLField(
        verbose_name='Image URL',
        blank=True,
        null=True
    )

    objects = PostManager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('view_blog_post', args=[str(self.slug)])

    @property
    def body_html(self):
        return self.convert_alts_to_captions(
            markdown.Markdown().convert(self.body)
        )

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

    class Meta:
        ordering = ('-date',)
        get_latest_by = 'date'
