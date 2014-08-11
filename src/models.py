import markdown
import cgi
import time
import datetime
import email.utils
import json
import ntpath
import slugify
import utility


class Post:
    """
    Definition class for a post, constructed with
    a path to a markdown file.
    """
    def __init__(self, file_path, date_override=None):
        md = markdown.Markdown(extensions = ['meta'])
        with open(file_path, 'r') as file:
            try:
                html = md.convert(file.read().decode('utf-8'))
            except AttributeError: # Python 3.3
                html = md.convert(utility.get_string_from_hex(file.read()))
        meta = md.Meta

        if date_override:
            self.date = date_override
        else:
            self.date = ntpath.basename(file_path).split('.md')[0]
        self.title = meta["title"][0]
        self.link = slugify.slugify(self.title)
        self.description = meta["description"][0]
        try:
            self.image = meta["image"][0]
        except KeyError:
            self.image = None
        self.body = html


    def to_rss(self):
        """
        Fills in RSS attributes (only needed for one post)
        """
        self.rss_body = cgi.escape(self.body)
        self.rss_date = email.utils.formatdate(time.mktime(datetime.datetime.strptime(self.date, '%Y-%m-%d').timetuple())) # Never touching this again


class ContentItems:
    """
    Container for any item extracted out of pages.json
    """
    def __init__(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)

        self.friends = []
        self.projects = []

        for item in data["Friends"]:
            self.friends.append(Friend(item))

        for item in data["Projects"]:
            self.projects.append(Project(item))


class Friend:
    def __init__(self, content_item):
        self.title = content_item["title"]
        self.subtitle = content_item["subtitle"]
        self.image = content_item["image"]
        self.link = content_item["link"]


class Project:
    def __init__(self, content_item):
        self.title = content_item["title"]
        self.subtitle = content_item["subtitle"]
        self.image = content_item["image"]
        self.caption = content_item["caption"]
        self.link = content_item["link"]


class Email:
    """
    Definition class for an email.
    Constructs header and email body
    """
    def __init__(self, sender, recipient, subject, post, unsubscribe_key, full_text):
        self.sender = sender
        self.recipient = recipient
        self.subject = subject
        self.post = post
        self.unsubscribe_key = unsubscribe_key
        self.full_text = full_text

        self.headers = "\r\n".join(["from: " + self.sender,
                           "subject: " + self.subject,
                           "to: " + self.recipient,
                           "mime-version: 1.0",
                           "content-type: text/html"])

        self.body = utility.get_html_from_template(template_name="email.html", data=self)
        self.content = self.headers + "\r\n\r\n" + self.body