# frozen_literal_string: true

require 'date'
require 'json'

module Blog
  # Stats
  module Stats
    def self.write_stats!(journal, path)
      Blog.logger.info 'gathering stats'
      stats = gather_stats(journal)

      Blog.logger.info "writing stats to #{path.pretty_path}"
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
        @logger = Blog.logger
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

      def private_entries
        journal.private_entries
      end

      def public_entries
        journal.public_entries
      end

      def all_entries
        journal.all_entries
      end
    end

    # PostCountCruncher
    class PostCountCruncher < BaseCruncher
      def stats_key
        'posts'
      end

      def crunch
        @logger.debug 'calculating post count'
        {
          public: public_entries.count.pretty,
          private: private_entries.count.pretty,
          all: all_entries.count.pretty
        }
      end
    end

    # WordCountCruncher
    class WordCountCruncher < BaseCruncher
      def stats_key
        'words'
      end

      def crunch
        @logger.debug 'calculating word count'
        {
          public: {
            average: average(public_wordcounts).pretty,
            total: total(public_wordcounts).pretty
          },
          private: {
            average: average(private_wordcounts).pretty,
            total: total(private_wordcounts).pretty
          },
          all: {
            average: average(total_wordcounts).pretty,
            total: total(total_wordcounts).pretty
          }
        }
      end

      private

      def total_wordcounts(entries = nil)
        entries ||= all_entries
        entries.collect(&:body_text).map(&:word_count)
      end

      def private_wordcounts
        total_wordcounts(private_entries)
      end

      def public_wordcounts
        total_wordcounts(public_entries)
      end
    end

    # StreakCruncher
    class StreakCruncher < BaseCruncher
      def stats_key
        'days'
      end

      def crunch
        @logger.debug 'calculating streaks'
        {
          current: current_streak,
          streaks: longest_streaks,
          draughts: longest_draughts
        }
      end

      private

      def longest_streaks
        streaks.sort_by { |d| d[0] }.reverse.take(3).map do |count, dates|
          {
            days: count.pretty,
            start: dates[0],
            end: dates[1]
          }
        end
      end

      def current_streak
        streaks.take(1).map do |count, dates|
          {
            days: count.pretty,
            start: dates[0],
            end: dates[1]
          }
        end.first
      end

      def longest_draughts
        draughts.take(3).map do |count, dates|
          {
            days: count.pretty,
            start: dates[0],
            end: dates[1]
          }
        end
      end

      def draughts
        _draughts = []
        entry_dates.each_cons(2).each do |curr, nxt|
          next if nxt.nil? || curr == nxt.next_day
          _draughts << [(curr - nxt).to_i, [nxt, curr]]
        end
        _draughts.sort_by { |d| d[0] }.reverse
      end

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
        all_entries.collect(&:date).reverse
      end
    end

    # TagsCruncher
    class TagsCruncher < BaseCruncher
      def stats_key
        'tags'
      end

      def crunch
        @logger.debug 'calculating tags'
        {
          top: top_three
        }
      end

      private

      def top_three
        tags_by_count.take(3)
      end

      def tags_by_count
        tags = Hash.new([])
        public_entries.each do |entry|
          entry.tags.each do |t|
            tags[t] = tags[t] + [entry.date]
          end
        end
        tags.sort_by { |_t, dates| dates.count }.reverse
      end
    end
  end
end
