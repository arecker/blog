# frozen_string_literal: true

# Functions for building and parsing site navigation
module Nav
  # Returns a sorted list of pages that should appear in site
  # navigation.
  def self.pages
    Files.pages.map do |p|
      [p.permalink, p.frontmatter['nav']]
    end.select(&:all?).sort_by(&:last).collect(&:first)
  end
end
