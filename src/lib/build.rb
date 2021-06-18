# frozen_string_literal: true

# Functions for building portions of the site.
module Build
  # Build sitemap.
  def self.sitemap
    Files.generate(Files.target('sitemap.xml')) do
      context = { entries: Files.entries, pages: Files.pages }
      Template.render('sitemap.xml', context)
    end
  end

  # Build atom feed.
  def self.feed
    Files.generate(Files.target('feed.xml')) do
      context = { entries: Files.entries, pages: Files.pages }
      Template.render('feed.xml', context)
    end
  end

  # Build site info
  def self.info
    Files.generate(Files.join('_data/git.yml')) do
      Git.context.to_yaml
    end
  end

  # Build site projects
  def self.projects
    Files.generate(Files.join('_data/projects.yml')) do
      Projects.context.to_yaml
    end
  end

  # Build site navigation
  def self.nav
    Files.generate(Files.join('_data/nav.yml')) do
      Nav.pages.to_yaml
    end
  end

  # Build site statistics.
  def self.stats
    Files.generate(Files.join('_data/stats.yml')) do
      Stats.context.to_yaml
    end
  end
end
