# frozen_string_literal: true

require 'date'
require 'yaml'

module Blog
  class Page
    attr_reader :source

    def initialize(source, content: nil)
      @source = source
      @content = content unless content.nil?
    end

    def pathname
      "/#{filename}"
    end

    def filename
      if entry?
        "#{File.basename(source, '-entry.md')}.html"
      else
        "#{File.basename(source, '.*')}.html"
      end
    end

    def content
      @content ||= File.read(source)
    end

    def frontmatter
      YAML.safe_load(content)
    end

    def date
      return nil unless entry?

      Date.strptime(filename, '%Y-%m-%d.html')
    end

    def nav?
      frontmatter.key?('nav')
    end

    def entry?
      Blog.join(source).start_with?(Blog.join('_posts'))
    end
  end
end
