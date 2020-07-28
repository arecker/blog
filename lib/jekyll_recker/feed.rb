# frozen_string_literal: true

module JekyllRecker
  # Feed
  class Feed
    attr_reader :site

    def initialize(site)
      @site = site
    end

    def content
      <<~XML
        <?xml version="1.0" encoding="utf-8"?>
        <feed xmlns="http://www.w3.org/2005/Atom">
          <title>#{site.config.title}</title>
          <link href="#{site.url}"/>
          <updated>2003-12-13T18:30:02Z</updated>
          <author>#{author}</author>
          <id>#{feed_url}</id>
        </feed>
      XML
    end

    def author
      <<~XML
        <name>#{site.config.author}</name>
        <email>#{site.config.email}</email>
      XML
    end

    def feed_url
      File.join(site.url, 'feed.xml')
    end
  end
end
