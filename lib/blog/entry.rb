# frozen_string_literal: true

require 'date'
require 'org-ruby'

module Blog
  # A Journal Entry
  class Entry
    def self.last_five_from_file(file)
      journal = Orgmode::Parser.load(file)
      headlines = journal.headlines.reverse
      last_five = headlines.reject { |h| h.tags.include? 'private' }.take(5)
      last_five.map do |h|
        Entry.new(
          h.output_text,
          h.body_lines.drop(1).collect(&:output_text).join(' '),
          tags: h.tags
        )
      end
    end

    attr_reader :tags

    def initialize(datestamp, text, tags: [])
      @datestamp = datestamp
      @text = text
      @tags = tags
    end

    def title
      date.strftime('%A, %B %-e %Y')
    end

    def slug
      date.strftime('%Y-%m-%d')
    end

    def date
      Date.strptime(@datestamp, '%Y-%m-%d %A')
    end

    def description
      case tags.size
      when 0
        nil
      else
        tags.join(', ')
      end
    end

    def tags?
      @tags.any?
    end

    def body
      Orgmode::Parser.new(@text).to_html
    end
  end
end
