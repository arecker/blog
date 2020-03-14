# frozen_string_literal: true

module Jekyll
  module Recker
    module Generators
      # StatsGenerator
      class StatsGenerator < Jekyll::Generator
        def generate(site)
          Recker.info 'generating site statistics'
          site.data['stats'] = Stats.crunch(site)
        end
      end
    end
  end
end
