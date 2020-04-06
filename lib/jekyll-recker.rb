# frozen_string_literal: true

require 'jekyll'

module Jekyll
  # Recker
  module Recker
    require 'jekyll_recker/logger.rb'
    require 'jekyll_recker/mixins.rb'

    require 'jekyll_recker/commands.rb'
    require 'jekyll_recker/configuration.rb'
    require 'jekyll_recker/error.rb'
    require 'jekyll_recker/generators.rb'
    require 'jekyll_recker/shell.rb'
    require 'jekyll_recker/slack.rb'
    require 'jekyll_recker/tags.rb'
    require 'jekyll_recker/twitter.rb'
    require 'jekyll_recker/version.rb'
    require 'jekyll_recker/words.rb'
  end
end
