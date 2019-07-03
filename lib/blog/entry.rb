require 'date'
require 'org-ruby'

module Blog
  # A Journal Entry
  class Entry
    def self.last_five_from_file(file)
      journal = Orgmode::Parser.load(file)
      headlines = journal.headlines.reverse
      last_five = headlines.select { |h| h.tags.include? 'public' }.take(5)
      last_five.map do |h|
        Entry.new(
          h.output_text,
          h.body_lines.drop(1).collect(&:output_text).join(' ')
        )
      end
    end

    def initialize(datestamp, text)
      @datestamp = datestamp
      @text = text
    end

    def date
      Date.strptime(@datestamp, '%Y-%m-%d %A').strftime('%A, %B %-e %Y')
    end

    def body
      Orgmode::Parser.new(@text).to_html
    end
  end
end
