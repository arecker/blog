# frozen_string_literal: true

module JekyllRecker
  # Entry
  class Entry
    def initialize(doc)
      @doc = doc
    end

    def content
      @doc.content
    end

    def date
      @date ||= Date.parse(@doc.date.strftime('%Y-%m-%d'))
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
