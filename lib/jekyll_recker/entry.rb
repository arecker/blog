# frozen_string_literal: true

module JekyllRecker
  # Entry
  class Entry
    include Date

    def initialize(doc)
      @doc = doc
    end

    def content
      @doc.content
    end

    def date
      @date ||= time_to_date(@doc.date)
    end

    def words
      content.split.map do |token|
        token.gsub!(/[^0-9a-z ]/i, '')
        token.downcase
      end
    end

    def word_count
      @word_count ||= words.size
    end
  end
end
