# frozen_string_literal: true

require 'logger'

module JekyllRecker
  # Logging
  module Logging
    def self.included(base)
      base.extend(self)
    end

    def info(msg)
      Jekyll.logger.info 'jekyll-recker:', msg
    end

    def logger
      ::Jekyll.logger
    end
  end
end
