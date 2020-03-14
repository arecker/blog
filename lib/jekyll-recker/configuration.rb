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
    end
  end
end
