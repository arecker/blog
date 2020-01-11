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

    def self.prettify_path(path, home = nil)
      home ||= File.expand_path('~/')
      path.sub(home, '~')
    end

    def self.to_word_list(str)
      str.split(' ')
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
  def words
    Blog::Words.to_word_list(self)
  end

  def word_count
    Blog::Words.to_word_list(self).count
  end

  def pretty_path(home = nil)
    Blog::Words.prettify_path(self, home)
  end
end
