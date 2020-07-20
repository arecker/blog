# frozen_string_literal: true

module JekyllRecker
  module Generators
    # Memory Size Generator
    class Memory < Jekyll::Generator
      include Stats

      KEY = 'memory'

      def crunch
        results = Hash.new(0)
        entries.each do |entry|
          results['chars'] += entry.content.size
          results['spaces'] += entry.content.count(' ')
          results['size'] += entry.content.bytes.to_a.length
        end
        results['size'] = bytes_to_megabytes(results['size'])
        results
      end

      private

      def bytes_to_megabytes(bytes)
        (bytes / (1024.0 * 1024.0)).to_f.round(4)
      end
    end
  end
end
