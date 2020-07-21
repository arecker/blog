# frozen_string_literal: true

require 'bundler'

module JekyllRecker
  module Generators
    module BaseGenerator
      include Mixins::Logging

      def production?
        ENV['JEKYLL_ENV'] == 'production'
      end

      def generate(site)
        @site = site
        logger.info "running #{self.class.name} generator"
      end
    end
    
    # Stats Module
    #
    # Functions for stats generators.
    # @abstract
    module Stats
      include BaseGenerator
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

      # Calculates the average of a list of numbers.
      #
      # @param [Array<Numeric>] numlist list of numbers to be averaged.
      # @return [Numeric] rounded, calculated average of numlist.
      def average(numlist)
        calc = numlist.inject { |sum, el| sum + el }.to_f / numlist.size
        calc.round
      end

      # Calculates the total of a list of numbers.
      #
      # @param [Array<Numeric>] numlist list of numbers to be totaled.
      # @return [Numeric] calculated total of numlist.
      def total(numlist)
        numlist.inject(0) { |sum, x| sum + x }
      end

      def entries
        @site.posts.docs.select(&:published?).sort_by(&:date).reverse
      end
    end

    # Graphs Module
    #
    # Functions for graph creation.
    # @abstract
    module Graphs
      include BaseGenerator

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
    require 'jekyll_recker/generators/memory.rb'
  end
end
