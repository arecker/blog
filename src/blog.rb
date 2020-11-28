# frozen_string_literal: true

# Blog
module Blog
  autoload :Files, 'blog/files'
  autoload :Git, 'blog/git'
  autoload :Logging, 'blog/logging'
  autoload :Math, 'blog/math'
  autoload :Shell, 'blog/shell'
  autoload :Time, 'blog/time'

  # Eager Loads
  require 'blog/generators'
end
