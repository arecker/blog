# frozen_string_literal: true

require 'logger'

module Blog
  # A module for concisely accessing the Blog logger.  You can call
  # directly or inherit as a mixin.
  module Logging
    # For accessing the Blog logger.
    def logger
      Logging.logger
    end

    # The Blog logger.
    def self.logger
      @logger ||= Logger.new($stdout)
    end
  end
end
