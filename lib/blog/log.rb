# frozen_string_literal: true

require 'logger'

module Blog
  # Log
  module Log
    def self.logger
      @logger ||= default_logger
    end

    def self.default_logger
      logger = Logger.new(STDOUT)
      logger.level = Logger::INFO
      logger.formatter = proc do |severity, _datetime, _progname, msg|
        "#{severity.ljust(5)}: #{msg}\n"
      end
      logger
    end
  end
end
