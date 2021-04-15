# frozen_string_literal: true

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
      "#{File.basename(source, '.*')}.html"
    end

    def content
      @content ||= File.read(source)
    end

    def frontmatter
      YAML.safe_load(content)
    end

    def nav?
      frontmatter.key?('nav')
    end

    def entry?
      Blog.join(source).start_with?(Blog.join('_posts'))
    end
  end
end
