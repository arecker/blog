# frozen_string_literal: true

require 'bundler'

module JekyllRecker
  # Generators Module
  module Generators
    # Base Generator Functions
    module Base
      include Logging
      include Math

      def production?
        ENV['JEKYLL_ENV'] == 'production'
      end

      def entries
        @site.posts.docs.select(&:published?).sort_by(&:date).reverse
      end

      def dates
        entries.collect(&:date).map { |t| Date.new(t.year, t.month, t.day) }
      end
    end

    # Stats Module
    #
    # Functions for stats generators.
    # @abstract
    module Stats
      include Base
      include Jekyll::Filters

      def key
        self.class.const_get(:KEY)
      end

      def generate(site)
        @site = site
        logger.info "running stats.#{key} generator"
        @site.data['stats'] ||= {}
        @site.data['stats'][key] = crunch
      end

      def crunch
        raise NotImplementedError, '#crunch not implemented!'
      end
    end

    # Graphs Module
    #
    # Functions for graph creation.
    # @abstract
    module Graphs
      include Base

      def new_line_graph
        g = Gruff::Line.new('800x600')
        g.theme = Gruff::Themes::PASTEL
        g.hide_legend = true
        g
      end

      def new_pie_graph
        g = Gruff::Pie.new('800x600')
        g.theme = Gruff::Themes::PASTEL
        g.hide_legend = false
        g
      end

      def graphs_join(path)
        recker = @site.config.fetch('recker', {})
        graphs_dir = recker.fetch('graphs', 'assets/images/graphs/')
        File.join Bundler.root, graphs_dir, path
      end
    end

    require 'jekyll_recker/generators/image_resize.rb'
    require 'jekyll_recker/generators/post_count.rb'
    require 'jekyll_recker/generators/word_count.rb'
    require 'jekyll_recker/generators/streaks.rb'
    require 'jekyll_recker/generators/swears.rb'
  end
end
