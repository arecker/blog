from django.db import models
import datetime
import slugify
import markdown
import bs4


class PostManager(models.Manager):
    def all_archives(self):
        return Post.objects.values('title', 'slug').filter(published=True).order_by('-date')


    def all_feed_items(self):
        return Post.objects.values('title', 'slug', 'description', 'date').filter(published=True).order_by('-date')


    def latest(self):
        latest = Post.objects.filter(published=True).order_by('-date')
        if len(latest) > 0:
            return latest[0]
        else:
            return None


class Post(models.Model):
    title = models.CharField(verbose_name='Title', max_length=120)
    slug = models.SlugField(verbose_name='Slug', max_length=120, unique=True, blank=True)
    date = models.DateField(verbose_name='Date', db_index=True, default=datetime.datetime.now(), blank=True)
    published = models.BooleanField(verbose_name='Publish', default=False)
    description = models.TextField(max_length=200, verbose_name='Description', blank=True, null=True)
    body = models.TextField(verbose_name='Body', blank=True, null=True)
    image_url = models.CharField(verbose_name='Image URL', max_length=160, blank=True, null=True)

    objects = PostManager()


    def save(self, *args, **kwargs):
        # Extend save function to slugify title
        self.slug = slugify.slugify(self.title, to_lower=True)
        return super(Post, self).save(*args, **kwargs)


    def get_truncated_description(self, length=50, suffix='...'):
        if not self.description:
            return ''
        if len(self.description) <= length:
            return self.description
        else:
            return ' '.join(self.description[:length+1].split(' ')[0:-1]) + suffix
    get_truncated_description.short_description = 'Description'


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
            src = tag['src']
            try:
                alt = tag['alt']
            except KeyError:
                alt = None
            tag.wrap(soup.new_tag('figure', { 'class': 'image'}))
            tag.parent['class'] = 'image'
            tag.insert_after(soup.new_tag('figcaption'))
            if alt:
                tag.next_sibling.string = alt
        return soup.prettify()


    def render_html(self):
        md = markdown.Markdown()
        return self.convert_alts_to_captions(md.convert(self.body))


    def __unicode__(self):
        return self.title