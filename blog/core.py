import os
import shutil
import time
import datetime
import codecs
import markdown
import slugify
import bs4
import json
import jinja2
import PyRSS2Gen
import smtplib


class Data:
    """
    Empty placeholder class
    """
    pass


class Config:
    def __init__(self):
        config_target = os.path.join(os.path.expanduser("~"), ".blog.json")
        with open(config_target) as stream:
            data = json.load(stream)
            self.posts = data["posts"]
            self.templates = data["templates"]
            self.public = data["public"]
            self.static = data["static"]

        if not os.path.exists(self.public):
            os.makedirs(self.public)


class CacheWriter:
    @staticmethod
    def render_html_from_template(template, data):
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(Config().templates))
        j_template = env.get_template(template)
        return j_template.render(data = data)


    @staticmethod
    def write_page(template, data, name, path=Config().public):
        output = CacheWriter.render_html_from_template(template=template, data=data)
        with open(os.path.join(path, name), 'wb') as file:
            output = bs4.BeautifulSoup(output).prettify()
            file.write(output.encode('utf-8'))


    @staticmethod
    def write_route(template, data, route, root=Config().public, test=False, file_override="index.html"):
        path = os.path.join(root, route)
        os.makedirs(path)
        CacheWriter.write_page(template=template, data=data, name=file_override, path=path)


    @staticmethod
    def rebuild_static():
        c = Config()
        target = os.path.join(c.public, 'static')
        if os.path.exists(target):
            shutil.rmtree(target)
        shutil.copytree(c.static, target)


    @staticmethod
    def create_feed_route(root=Config().public):
        path = os.path.join(root, 'feed')
        os.makedirs(path)


    @staticmethod
    def drop_public(root=Config().public):
        """
        Completely purge public folder
        """
        for thing in os.listdir(root):
            try:
                shutil.rmtree(os.path.join(root, thing))
            except:
                os.remove(os.path.join(root, thing))


    @staticmethod
    def refresh_public():
        CacheWriter.drop_public()
        CacheWriter.rebuild_static()

        packets = []

        # Home and other static pages
        home_data = Data()
        posts = Post.get_all_posts()
        home_data.posts = posts
        home_data.latest = posts[0]
        packets.append(("home.html", home_data, None, "index.html"),)
        packets.append(("404.html", None, "404", None),)
        packets.append(("sitemap.xml", posts, None, "sitemap.xml"),)

        # Post data
        for post in posts:
            packets.append(
                ("post.html", post, post.link, 'index.html')
            )

        # Write all the packets
        for template, data, route, name in packets:
            if route:
                CacheWriter.write_route(template=template, data=data, route=route)
            else:
                CacheWriter.write_page(template=template, data=data, name=name)


        # RSS Feed
        CacheWriter.create_feed_route()
        feed = RSSFeed(posts)
        feed.write()



class Post:
    """
    Post Class
    Defines post objects.  Constructed with path to markdown file
    """
    def __init__(self, path):
        data = self.parse_post_from_file(path)
        self.title = data.title
        self.date = data.date
        self.date_pretty = time.strftime("%B %d, %Y", self.date)
        self.body = data.body
        self.link = data.link
        self.description = data.description
        self.image = data.image


    def __unicode__(self):
        return self.title


    @classmethod
    def parse_post_from_file(cls, path):
        file = codecs.open(path, encoding="utf-8", mode="r")
        contents = file.read()
        file.close()

        md = markdown.Markdown(extensions = ['extra', 'meta'])
        html = md.convert(contents)
        meta = md.Meta

        data = Data()
        data.body = Post.convert_alts_to_captions(html)
        data.title = meta["title"][0]
        data.link = slugify.slugify(data.title)
        data.description = meta["description"][0]
        data.date = time.strptime(meta["date"][0], "%m-%d-%Y")

        try:
            data.image = meta["image"][0]
        except KeyError:
            data.image = None

        return data


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


    @staticmethod
    def get_all_posts():
        """
        returns all post objects in order of date desc
        """
        posts = []
        c = Config()
        files = os.listdir(c.posts)
        for file in files:
            file = os.path.join(c.posts, file)
            if os.path.isfile(file) and os.path.splitext(file)[1] == '.md':
                posts.append(Post(os.path.abspath(file)))

        return sorted(posts, key=lambda x: x.date, reverse=True)


class RSSFeed:
    def __init__(self, posts):
        items = []
        for post in posts:
            items.append(PyRSS2Gen.RSSItem(
                title = post.title,
                link = "http://alexrecker.com/" + post.link,
                description = post.description,
                guid = PyRSS2Gen.Guid("http://alexrecker.com/" + post.link),
                pubDate = datetime.datetime.fromtimestamp(time.mktime(post.date)),
                author = "alex@reckerfamily.com"
            ))

        self.feed = PyRSS2Gen.RSS2(
            title = "Blog by Alex Recker",
            link = "http://alexrecker.com",
            description = "Hey - my name is Alex Recker.  I like to write words.",
            image = PyRSS2Gen.Image(url='http://media.alexrecker.com/images/portrait.jpg', title='Blog by Alex Recker', link='alexrecker.com'),
            items = items
        )


    def write(self):
        self.feed.write_xml(open(os.path.join(Config().public, 'feed', "index.xml"), "w"))


class Email:
    def __init__(self, data):
        self.sender = 'Alex Recker'
        self.recipient = data.email
        self.subject = data.post.title
        self.post = data.post
        self.unsubscribe_key = data.unsubscribe_key
        self.full_text = data.full_text

        self.headers = "\r\n".join(["from: " + self.sender,
        "subject: " + self.subject,
        "to: " + self.recipient,
        "mime-version: 1.0",
        "content-type: text/html"])


    def send(self, test=False):
        c = Config()
        self.body = CacheWriter.render_html_from_template(template="email.html", data=self)
        self.content = self.headers + "\r\n\r\n" + self.body
        self.content = self.content.encode('ascii', 'ignore')

        if not test:
            session = smtplib.SMTP('smtp.gmail.com', 587)
            session.ehlo()
            session.starttls()
            session.login(c.EMAIL, c.EMAIL_PASS)
            session.sendmail(c.EMAIL, self.recipient, self.content)
            session.close()
        else:
            CacheWriter.write_page(template="email.html", data=self, name=self.recipient + '.html', path=os.getcwd())