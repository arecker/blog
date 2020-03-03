# frozen_string_literal: true

require 'date'
require 'org-ruby'

module Blog
  # Entry
  class Entry
    def initialize(headline)
      @headline = headline
    end

    def title
      date.strftime('%A, %B %-e %Y')
    end

    def subtitle
      @subtitle ||= @headline.headline_text.split(' ').drop(2).join(' ')
    end

    alias excerpt subtitle

    def tags
      @tags ||= @headline.tags
    end

    def date
      @date ||= Date.strptime(
        @headline.headline_text.split(' ').take(2).join(' '),
        '%Y-%m-%d %A'
      )
    end

    def date_slug
      date.strftime('%Y-%m-%d')
    end

    def public?
      !tags.include? 'private'
    end

    def filename
      "#{date_slug}-#{date_slug}.html.html"
    end

    def permalink
      "https://www.alexrecker.com/#{date_slug}.html"
    end

    def body_text
      @headline.body_lines.drop(1).collect(&:output_text).join(' ')
    end

    def body_html
      Orgmode::Parser.new(body_text).to_html
    end

    def to_html
      <<~HTML
        ---
        title: #{title}
        excerpt: #{excerpt}
        ---
        #{body_html}
      HTML
    end
  end
end
