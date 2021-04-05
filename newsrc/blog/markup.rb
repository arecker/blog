# frozen_string_literal: true

require 'yaml'

module Blog
  # For working with markdown and HTML.
  module Markup
    # For building HTML documents from pages.
    def self.strip_frontmatter(text)
      text.gsub(/^---\n(.*?)\n---\n/, '')
    end

    def self.markdown_to_html(text)
      formatter = RDoc::Markup::ToHtml.new(RDoc::Options.new, nil)
      RDoc::Markdown.parse(text).accept(formatter)
    end

    # Buld an HTML doc.
    class Document
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
        <<~HTML
          #{page.content}
          #{footer}
        HTML
      end

      def footer
        <<~HTML
          <hr/>
          <footer>
            <small>Last Updated: #{page.build_updated}</small>
            <small>Last Change:
              <span>#{page.build_summary} (<a href="https://github.com/arecker/blog/commit/#{page.build_head}">#{page.build_short_head}</a>)</span>
            </small>
            <small>&copy; Copyright #{page.build_year} Alex Recker</small>
          </footer>
        HTML
      end

      def to_html
        <<~HTML
          <!doctype html>
          <html lang="en">
          #{head}
          #{body}
          </html>
        HTML
      end
    end

    def self.render(from = '', to = '')
      page = Blog::Page.new(Blog::Files.join(from))
      document = Document.new(page)
      File.open(Blog::Files.join(to), 'w+') do |output|
        output.write document.to_html
      end
    end
  end
end
