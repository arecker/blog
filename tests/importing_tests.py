from django.test import TestCase
import importlib


class TestImports(TestCase):
    def run_import(self, name):
        success = True
        try:
            importlib.import_module(name)
        except:
            success = False
        self.assertTrue(success)


    def test_Blog(self): self.run_import("Blog")
    def test_Blog_wsgi(self): self.run_import("Blog.wsgi")
    def test_Blog_settings(self): self.run_import("Blog.settings")
    def test_Blog_apps(self): self.run_import("Blog.apps")
    def test_Blog_apps_Blogging(self): self.run_import("Blog.apps.Blogging")
    def test_Blog_apps_Blogging_migrations(self): self.run_import("Blog.apps.Blogging.migrations")
    def test_Blog_apps_Subscribing(self): self.run_import("Blog.apps.Subscribing")
    def test_Blog_apps_Subscribing_migrations(self): self.run_import("Blog.apps.Subscribing.migrations")
