# frozen_string_literal: true

module Jekyll
  module Recker
    module Mixins
      # Descendants
      module Descendants
        def self.included(base)
          base.extend(self)
        end

        def descendants
          ObjectSpace.each_object(Class).select { |klass| klass < self }
        end
      end

      # Logging
      module Logging
        def self.included(base)
          base.extend(self)
        end

        def logger
          Jekyll::Recker.logger
        end
      end
    end
  end
end
