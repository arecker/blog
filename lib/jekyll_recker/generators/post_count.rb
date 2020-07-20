# frozen_string_literal: true

module JekyllRecker
  module Generators
    # Post Count Generator
    class PostCount < Jekyll::Generator
      include Stats

      KEY = 'posts'

      def crunch
        entries.count
      end
    end
  end
end
