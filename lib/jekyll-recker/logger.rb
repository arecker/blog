# frozen_string_literal: true

require 'logger'

module Jekyll
  # Recker
  module Recker
    def self.logger
      @logger ||= make_logger
    end

    def self.make_logger
      logger = Logger.new(STDOUT)
      logger.formatter = proc do |_severity, _datetime, _progname, msg|
        "jekyll-recker: #{msg}\n"
      end
      logger
    end
  end
end
