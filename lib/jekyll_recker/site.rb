# frozen_string_literal: true

module JekyllRecker
  # Site
  class Site
    def initialize(site)
      @site = site
    end

    def entries
      @entries ||= build_entries
    end

    def production?
      ENV['JEKYLL_ENV'] == 'production'
    end

    private

    def build_entries
      @site.posts.docs.select(&:published?).sort_by(&:date).reverse.map { |p| Entry.new(p) }
    end
  end
end
