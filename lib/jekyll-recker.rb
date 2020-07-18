# frozen_string_literal: true

require 'jekyll'

# jekyll-recker
#
# The greatest jekyll plugin in the world
module JekyllRecker
  autoload :Mixins, 'jekyll_recker/mixins.rb'
  autoload :Shell, 'jekyll_recker/shell.rb'
  autoload :Social, 'jekyll_recker/social.rb'
  autoload :VERSION, 'jekyll_recker/version.rb'

  # Eager loads!
  require 'jekyll_recker/commands.rb'
  require 'jekyll_recker/filters.rb'
  require 'jekyll_recker/generators.rb'
  require 'jekyll_recker/tags.rb'
end
