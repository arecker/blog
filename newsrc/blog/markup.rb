# frozen_string_literal: true

require 'yaml'

module Blog
  # For working with markdown and HTML.
  module Markup
    # Wrapper object for working with pages.
    class Page
      attr_reader :source

      def initialize(source='')
        @source = source
      end

      def markdown?
        ['.md', '.markdown'].include? File.extname(source)
      end

      def frontmatter
        YAML.load_file source
      end

      def content
        data = File.read(source)
        data unless markdown?

        formatter = RDoc::Markup::ToHtml.new(RDoc::Options.new, nil)
        RDoc::Markdown.parse(data).accept(formatter)
      end

      def render(target)
        File.open(target, 'w+') do |f|
          builder = DocBuilder.new(self)
          f.write builder.to_html
        end
      end
    end

    # For building HTML documents from pages.
    class DocBuilder
      attr_reader :page

      def initialize(page)
        @page = page
      end

      def head
        <<~HTML
          <head>
            <meta charset="UTF-8"/>
            <title>#{page.title} | #{page.description}}</title>
            <link rel="shortcut icon" type="image/x-icon" href="/favicon.ico"/>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <meta name="twitter:card" content="summary" />
            <meta name="twitter:site" content="@alex_recker" />
            <meta name="twitter:title" content="#{page.title}" />
            <meta name="twitter:description" content="#{page.description}" />
            <meta property="og:url" content="#{page.url}" />
            <meta property="og:type" content="article" />
            <meta property="og:title" content="#{page.title}"/>
            <meta property="og:description" content="#{page.description}" />
            <meta name="twitter:image" content="#{page.banner}"/>
            <meta property="og:image" content="#{page.banner}"/>
            <link href="/assets/site.css" rel="stylesheet"/>
          </head>
        HTML
      end

      def body
      end

      def to_html
        <<~HTML
<!doctype html>
<html lang="en">
#{head}
#{body}
#{footer}
        HTML
      end
    end

    def self.render(from = '', to = '')
      page = Page.new(Blog::Files.join(from))
      puts page.frontmatter
      # page.render(Blog::Files.join(to))
    end
  end
end
