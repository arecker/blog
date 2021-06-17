# frozen_string_literal: true

require 'date'

# Functions for statistics.
module Stats
  SWEAR_WORDS = %w[
    ass
    asshole
    booger
    crap
    damn
    fart
    fuck
    hell
    jackass
    piss
    poop
    shit
  ].freeze

  # Extract the words from a string.
  def self.extract_words(content)
    content.sub!(/^---\n.*?---\n/m, '')
    words = content.split.map do |token|
      token.gsub!(/[^0-9a-z ']/i, '')
      token.downcase
    end
    words.reject(&:empty?)
  end

  # Returns a list of journal entry word.
  def self.entry_words
    @entry_words ||= entries.map { |f| extract_words(File.read(f)) }
  end

  # Returns the average number of words per entry.
  def self.entry_words_average
    entry_totals = entry_words.collect(&:size).sum
    entry_totals.to_f / entry_words.size
  end

  # Returns the total number of swear words used.
  def self.swear_count
    entry_words.flatten.select { |w| SWEAR_WORDS.include? w }.size
  end

  # Returns the journal entry dates, sliced by consecutive dates.
  def self.consecutive_dates
    dates.slice_when { |p, c| c != p - 1 && c != p + 1 }.to_a
  end

  # Return all the stats data for site.
  def self.context
    {
      'total_posts' => entries.size,
      'consecutive_posts' => consecutive_dates.last.size,
      'total_words' => entry_words.flatten.size,
      'average_words' => entry_words_average.truncate,
      'swear_count' => swear_count
    }
  end
end
