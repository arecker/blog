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

    def tokens
      content.split
    end
  end
end
