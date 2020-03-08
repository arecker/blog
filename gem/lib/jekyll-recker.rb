module Jekyll
  module Recker
    require 'jekyll_recker/commands.rb'

    autoload :Twitter, 'jekyll_recker/twitter.rb'
    autoload :VERSION, 'jekyll_recker/version.rb'
  end
end
