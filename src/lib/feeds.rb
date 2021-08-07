# frozen_string_literal: true

module Blog
  # Functions for working with feeds.
  module Feeds
    # Returns the context used to render feeds.
    def self.context
      @context ||= {
        entries: Files.entries,
        pages: Files.pages
      }
    end

    # Generates the feeds.
    def self.generate_all
      ['feed.xml', 'sitemap.xml'].each do |name|
        target = Files.target(name)
        Files.generate(target) { Template.render(name, context) }
      end
    end
  end
end
