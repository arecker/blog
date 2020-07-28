# frozen_string_literal: true

require 'jekyll'

# jekyll-recker
#
# The greatest jekyll plugin in the world
module JekyllRecker
  autoload :Date, 'jekyll_recker/date.rb'
  autoload :Entry, 'jekyll_recker/entry.rb'
  autoload :Feed, 'jekyll_recker/feed.rb'
  autoload :Graphs, 'jekyll_recker/graphs.rb'
  autoload :Logging, 'jekyll_recker/logging.rb'
  autoload :Math, 'jekyll_recker/math.rb'
  autoload :Shell, 'jekyll_recker/shell.rb'
  autoload :Site, 'jekyll_recker/site.rb'
  autoload :Social, 'jekyll_recker/social.rb'
  autoload :VERSION, 'jekyll_recker/version.rb'

  # Eager loads!
  require 'jekyll_recker/commands.rb'
  require 'jekyll_recker/filters.rb'
  require 'jekyll_recker/generators.rb'
  require 'jekyll_recker/tags.rb'
end
