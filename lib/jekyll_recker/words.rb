# frozen_string_literal: true

module Jekyll
  module Recker
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

      def self.and_list_to_array(str)
        str = str.gsub(' and ', ', ')
        str.split(',').map(&:strip).reject(&:empty?)
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

      def self.to_weighted_list(arr)
        arr.uniq.map do |word|
          [word, arr.count(word)]
        end
      end
    end
  end
end

# Array extensions
class Array
  def to_and_list
    Jekyll::Recker::Words.array_to_and_list(self)
  end

  def to_weighted_list
    Jekyll::Recker::Words.to_weighted_list(self)
  end
end

# Integer extensions
class Integer
  def pretty
    Jekyll::Recker::Words.prettify_number(self)
  end
end

# String extensions
class String
  def words
    Jekyll::Recker::Words.to_word_list(self)
  end

  def word_count
    Jekyll::Recker::Words.to_word_list(self).count
  end

  def pretty_path(home = nil)
    Jekyll::Recker::Words.prettify_path(self, home)
  end

  def to_and_array
    Jekyll::Recker::Words.and_list_to_array(self)
  end
end
