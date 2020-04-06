# frozen_string_literal: true

require 'date'

module Jekyll
  module Recker
    # Stats
    module Stats
      include Jekyll::Recker::Mixins::Logging

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
        include Mixins::Descendants

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
            first, last = dates.minmax
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
