# frozen_string_literal: true

module Jekyll
  module Recker
    module Generators
      # StatsGenerator
      class StatsGenerator < Jekyll::Generator
        include Jekyll::Recker::LoggingMixin

        def generate(site)
          logger.info 'generating site statistics'
          site.data['stats'] = Stats.crunch(site)
        end
      end
    end
  end
end
