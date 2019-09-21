# frozen_string_literal: true

module Blog
  # Words
  module Words
    def self.array_to_and_list(array)
      case array.length
      when 0
        ''
      when 1
        array.first
      when 2
        "#{array.first} and #{array.last}"
      else
        array[0...-1].join(', ') + ", and #{array.last}"
      end
    end

    def self.prettify_number(number)
      number.to_s.reverse.gsub(/(\d{3})(?=\d)/, '\\1,').reverse
    end

    def self.word_count_from_string(str)
      str.gsub(/[^-a-zA-Z]/, ' ').split.size
    end
  end
end

# Array extensions
class Array
  def to_and_list
    Blog::Words.array_to_and_list(self)
  end
end

# Integer extensions
class Integer
  def pretty
    Blog::Words.prettify_number(self)
  end
end

# String extensions
class String
  def word_count
    Blog::Words.word_count_from_string(self)
  end
end
