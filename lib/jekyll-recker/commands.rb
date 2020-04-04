# frozen_string_literal: true

module Jekyll
  module Recker
    # Commands
    module Commands
      require 'jekyll-recker/commands/share.rb'
      require 'jekyll-recker/commands/slack.rb'
      require 'jekyll-recker/commands/tweet.rb'
    end
  end
end
