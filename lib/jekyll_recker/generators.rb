# frozen_string_literal: true

module Jekyll
  module Recker
    module Generators
      # Base Stats Methods
      module BaseStatsGenerator
        include Mixins::Logging
        include Jekyll::Filters

        def key
          self.class.const_get(:KEY)
        end

        def generate(site)
          @site = site
          logger.info "crunching stats.#{key}"
          @site.data['stats'] ||= {}
          @site.data['stats'][key] = crunch
        end

        def crunch
          raise NotImplementedError, '#crunch not implemented!'
        end

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

      # Post Count Generator
      class PostCount < Jekyll::Generator
        include BaseStatsGenerator

        KEY = 'posts'

        def crunch
          entries.count.pretty
        end
      end

      # Word Count Generator
      class Words < Jekyll::Generator
        include BaseStatsGenerator

        KEY = 'words'

        def crunch
          total_counts = entries.collect(&:content).map { |c| number_of_words(c) }
          {
            'average' => average(total_counts).pretty,
            'total' => total(total_counts).pretty
          }
        end
      end

      # StatsGenerator
      class OldStats < Jekyll::Generator
        include Jekyll::Recker::Mixins::Logging

        def generate(site)
          logger.info 'generating site statistics'
          site.data['stats'].merge!(Jekyll::Recker::Stats.crunch(site))
        end
      end
    end
  end
end
