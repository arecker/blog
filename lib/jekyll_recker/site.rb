# frozen_string_literal: true

module JekyllRecker
  # Site
  class Site
    def initialize(site)
      @site = site
    end

    def entries
      @site.posts.docs.select(&:published?).sort_by(&:date).reverse
    end

    def production?
      ENV['JEKYLL_ENV'] == 'production'
    end
  end
end
