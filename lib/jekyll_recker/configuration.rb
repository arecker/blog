# frozen_string_literal: true

module Jekyll
  module Recker
    # Configuration
    module Configuration
      def self.jekyll
        @jekyll ||= Jekyll.configuration
      end

      def self.recker
        jekyll.fetch('recker', {})
      end

      def self.twitter
        recker.fetch('twitter', {})
      end

      def self.slack
        recker.fetch('slack', {})
      end

      def self.site
        @site = Jekyll::Site.new(jekyll)
        @site.reset
        @site.read
        @site
      end

      def self.latest_post
        @latest_post ||= site.posts.docs.last
      end
    end
  end
end
