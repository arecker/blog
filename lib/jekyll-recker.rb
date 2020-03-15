# frozen_string_literal: true

require 'jekyll'

module Jekyll
  # Recker
  module Recker
    require 'jekyll-recker/commands.rb'
    require 'jekyll-recker/configuration.rb'
    require 'jekyll-recker/error.rb'
    require 'jekyll-recker/generators.rb'
    require 'jekyll-recker/log.rb'
    require 'jekyll-recker/shell.rb'
    require 'jekyll-recker/slack.rb'
    require 'jekyll-recker/stats.rb'
    require 'jekyll-recker/tags.rb'
    require 'jekyll-recker/twitter.rb'
    require 'jekyll-recker/version.rb'
    require 'jekyll-recker/words.rb'
  end
end
