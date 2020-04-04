# frozen_string_literal: true

module Jekyll
  module Recker
    # Descendants Mixin
    module DescendantsMixin
      def self.included(base)
        def base.descendants
          ObjectSpace.each_object(Class).select { |klass| klass < self }
        end
      end
    end

    # Logging Mixin
    module LoggingMixin
      def self.included(base)
        def base.logger
          Jekyll::Recker.logger
        end
      end

      def logger
        Jekyll::Recker.logger
      end
    end
  end
end
