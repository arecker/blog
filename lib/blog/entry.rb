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

    def tags
      @tags ||= @headline.tags
    end

    def date
      @date ||= Date.strptime(@headline.headline_text, '%Y-%m-%d %A')
    end

    def date_slug
      date.strftime('%Y-%m-%d')
    end

    def public?
      !@headline.tags.include? 'private'
    end

    def filename
      "#{date_slug}-#{date_slug}.html.html"
    end

    def body_text
      @headline.body_lines.drop(1).collect(&:output_text).join("\n").strip
    end

    def body_html
      Orgmode::Parser.new(body_text).to_html
    end

    def to_html
      <<~HTML
        ---
        title: #{title}
        tags: [#{tags.join(',')}]
        excerpt: #{tags.to_and_list}
        ---
        #{body_html}
      HTML
    end
  end
end
