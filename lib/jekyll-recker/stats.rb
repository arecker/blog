# frozen_string_literal: true

require 'date'

module Jekyll
  module Recker
    # Stats
    module Stats
      include Jekyll::Recker::LoggingMixin

      def self.crunch(site)
        stats = {}
        BaseCruncher.descendants.each do |cruncher_class|
          cruncher = cruncher_class.new(site)
          logger.info "crunching stats.#{cruncher.stats_key}"
          stats[cruncher.stats_key] = cruncher.crunch
        end
        stats
      end

      # Base Cruncher
      class BaseCruncher
        include Jekyll::Filters
        include DescendantsMixin

        def initialize(site)
          @site = site
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

        def entries
          @site.posts.docs.select(&:published?)
        end
      end

      # PostCountCruncher
      class PostCountCruncher < BaseCruncher
        def stats_key
          'posts'
        end

        def crunch
          entries.count.pretty
        end
      end

      # WordCountCruncher
      class WordCountCruncher < BaseCruncher
        def stats_key
          'words'
        end

        def crunch
          total_counts = entries.collect(&:content).map { |c| number_of_words(c) }
          {
            'average' => average(total_counts).pretty,
            'total' => total(total_counts).pretty
          }
        end
      end

      # Streak Cruncher
      class StreakCruncher < BaseCruncher
        def stats_key
          'days'
        end

        def crunch
          streaks.take(1).map do |count, dates|
            {
              'days' => count.pretty,
              'start' => dates[0],
              'end' => dates[1]
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
          entries.collect(&:date).map { |t| Date.new(t.year, t.month, t.day) }.sort.reverse
        end
      end
    end
  end
end
