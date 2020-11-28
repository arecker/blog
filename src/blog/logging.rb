# frozen_string_literal: true

require 'jekyll'

module Blog
  # Logging
  module Logging
    def info(msg)
      Jekyll.logger.info 'blog:', msg
    end

    def debug(msg)
      Jekyll.logger.debug 'blog:', msg
    end

    def error(msg)
      Jekyll.logger.error 'blog:', msg
    end

    def warn(msg)
      Jekyll.logger.warn 'blog:', msg
    end
  end
end
