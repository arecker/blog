import jinja2
import os
import shutil
import json
import binascii

"""
This is a place for miscellaneous utility methods
"""

class PathGetter:
    """
    Returns paths needed in the project
    """
    @staticmethod
    def get_project_src():
        return os.path.abspath(os.path.dirname(__file__))


    @staticmethod
    def get_posts_directory():
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'posts'))


    @staticmethod
    def get_public_directory():
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'public'))


    @staticmethod
    def get_content_path():
        return os.path.abspath(os.path.join(os.path.dirname(__file__), 'pages.json'))


    @staticmethod
    def get_abs_path_of_post_file(file):
        return os.path.abspath(os.path.join(PathGetter.get_posts_directory(), file))


    @staticmethod
    def get_abs_post_file_list():
        posts = []
        for item in sorted(os.listdir(PathGetter.get_posts_directory())):
            posts.append(PathGetter.get_abs_path_of_post_file(item))
        return posts


    @staticmethod
    def get_templates_directory():
        return os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))


    @staticmethod
    def get_test_docs_directory():
        return os.path.abspath(os.path.join(os.path.dirname(__file__), 'test_docs'))


def write_through_template(output_path, template_name, data, filename, templates_path=None):
    output = get_html_from_template(template_name=template_name, data=data, templates_path=templates_path)
    with open(os.path.join(output_path, filename), 'wb') as file:
        file.write(output.encode('utf-8'))


def get_html_from_template(template_name, data, templates_path=None):
    if not templates_path:
        templates_path = PathGetter.get_templates_directory()
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_path))
    j_template = env.get_template(template_name)
    return j_template.render(data = data)


def write_route(route_name, data, template_name, filename="index.html", public_root=None):
    if not public_root:
        public_root = PathGetter.get_public_directory()
    target_dir = os.path.join(public_root, route_name)
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    os.makedirs(target_dir)
    write_through_template(output_path=target_dir, template_name=template_name, data=data, filename=filename)


class KeyManager:
    """
    Retrieves keys from .keys.json
    """
    @staticmethod
    def get_key_data(path_to_key_file):
        if not path_to_key_file:
            path_to_key_file = os.path.join(PathGetter.get_project_src(), '.keys.json')
        try:
            with open(path_to_key_file, 'r') as file:
                data = json.load(file)
            return data
        except:
            raise Exception("No key file found")


    @staticmethod
    def get_admin_key(path_to_key_file=None):
        return KeyManager.get_key_data(path_to_key_file)["admin"]


    @staticmethod
    def get_app_key(path_to_key_file=None):
        return KeyManager.get_key_data(path_to_key_file)["app"]


    @staticmethod
    def get_email(path_to_key_file=None):
        return KeyManager.get_key_data(path_to_key_file)["email"]


    @staticmethod
    def get_email_password(path_to_key_file=None):
        return KeyManager.get_key_data(path_to_key_file)["email_password"]


def get_string_from_hex(hex):
    hex = hex.encode('ascii', 'strict')
    return binascii.unhexlify(hex.replace(' ', '').replace('\n', ''))