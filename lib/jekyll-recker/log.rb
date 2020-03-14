# frozen_string_literal: true

module Jekyll
  module Recker
    def self.info(msg)
      Jekyll.logger.info("jekyll-recker: #{msg}")
    end

    def self.error(msg)
      Jekyll.logger.error("jekyll-recker: #{msg}")
    end

    def self.abort_with(msg)
      Jekyll.logger.abort_with("jekyll-recker: #{msg}")
    end
  end
end
