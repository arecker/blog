# frozen_literal_string: true

require 'date'
require 'json'

module Blog
  # Stats
  module Stats
    def self.logger
      @logger ||= Blog::Log.logger
    end

    def self.write_stats!(journal, path)
      logger.info 'gathering stats'
      stats = gather_stats(journal)

      logger.info "writing stats to #{path.pretty_path}"
      File.open(path, 'w+') do |f|
        f.write(JSON.pretty_generate(stats))
      end
    end

    def self.gather_stats(journal)
      stats = {}
      BaseCruncher.descendants.each do |cruncher_class|
        cruncher = cruncher_class.new(journal)
        stats[cruncher.stats_key] = cruncher.crunch
      end
      stats
    end

    # Base Cruncher
    class BaseCruncher
      def self.descendants
        ObjectSpace.each_object(Class).select { |klass| klass < self }
      end

      def initialize(journal)
        @journal = journal
        @logger = Blog::Log.logger
      end

      private

      attr_reader :journal

      def average(numlist)
        calc = numlist.inject { |sum, el| sum + el }.to_f / numlist.size
        calc.round
      end

      def total(numlist)
        numlist.inject(0) { |sum, x| sum + x }
      end

      def public_entries
        journal.public_entries
      end
    end

    # PostCountCruncher
    class PostCountCruncher < BaseCruncher
      def stats_key
        'posts'
      end

      def crunch
        @logger.debug 'calculating post count'
        public_entries.count.pretty
      end
    end

    # WordCountCruncher
    class WordCountCruncher < BaseCruncher
      def stats_key
        'words'
      end

      def crunch
        @logger.debug 'calculating word count'
        total_counts = public_entries.collect(&:body_text).map(&:word_count)
        {
          average: average(total_counts).pretty,
          total: total(total_counts).pretty
        }
      end
    end

    # Streak Cruncher
    class StreakCruncher < BaseCruncher
      def stats_key
        'days'
      end

      def crunch
        @logger.debug 'calculating streaks'
        streaks.take(1).map do |count, dates|
          {
            days: count.pretty,
            start: dates[0],
            end: dates[1]
          }
        end.first
      end

      private

      def streaks
        _streaks = []
        entry_dates.slice_when do |prev, curr|
          curr != prev - 1
        end.each do |dates|
          first, last = dates.min, dates.max
          _streaks << [(last - first).to_i, [first, last]]
        end
        _streaks
      end

      def entry_dates
        public_entries.collect(&:date)
      end
    end
  end
end
