# frozen_string_literal: true

# Functions for building portions of the site.
module Build
  # Build sitemap.
  def self.sitemap
    context = { entries: Files.entries, pages: Files.pages }
    content = Template.render('sitemap.xml', context)
    target = Files.target('sitemap.xml')
    Files.write(target, content)
  end

  # Build atom feed.
  def self.feed
    context = { entries: Files.entries, pages: Files.pages }
    content = Template.render('feed.xml', context)
    target = Files.target('feed.xml')
    Files.write(target, content)
  end

  # Build site info
  def self.info
    context = {}.merge(Git.context)
    target = Files.join('_data/git.yml')
    Files.write(target, context.to_yaml)
  end

  # Build site projects
  def self.projects
    context = {}.merge(Projects.context)
    target = Files.join('_data/projects.yml')
    Files.write(target, context.to_yaml)
  end

  # Build site navigation
  def self.nav
    target = Files.join('_data/nav.yml')
    Files.write(target, Nav.pages.to_yaml)
  end

  # Build site statistics.
  def self.stats
    target = Files.join('_data/stats.yml')
    Files.write(target, Stats.context.to_yaml)
  end
end
