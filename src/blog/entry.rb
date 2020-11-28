# frozen_string_literal: true

module Blog
  # Entry
  class Entry
    include Blog::Time

    def initialize(doc)
      @doc = doc
    end

    def content
      @doc.content
    end

    def date
      @date ||= time_to_date(@doc.date)
    end

    def title
      to_uyd_date(date)
    end

    def subtitle
      @doc.data['title']
    end

    def url
      @doc.url
    end

    def words
      content.split.map do |token|
        token.gsub!(/[^0-9a-z ']/i, '')
        token.downcase
      end
    end

    def word_count
      @word_count ||= words.size
    end
  end
end
