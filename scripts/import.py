import os
import markdown
import time
import codecs
import datetime
from Blog.apps.Blogging.models import Post
BLOG_PATH = '/home/alex/Documents/Posts'


def parse_post_from_path(path):
    file = codecs.open(path, encoding="utf-8", mode="r")
    contents = file.read()
    file.close()

    md = markdown.Markdown(extensions = ['extra', 'meta'])
    html = md.convert(contents)
    meta = md.Meta

    data = Post()
    data.body = strip_meta(contents)
    data.title = meta["title"][0]
    data.description = meta["description"][0]
    timestamp = time.strptime(meta["date"][0], "%m-%d-%Y")
    data.date = datetime.datetime.fromtimestamp(time.mktime(timestamp))

    try:
        data.image_url = meta["image"][0]
    except KeyError:
        data.image_url = None

    return data


def strip_meta(body):
    return body


for file in os.listdir(BLOG_PATH):
    full_path = os.path.join(BLOG_PATH, file)
    if not os.path.isdir(full_path):
        post = parse_post_from_path(full_path)
        existing_posts = Post.objects.filter(title=post.title, date=post.date).count()
        if existing_posts < 1:
            post.save()