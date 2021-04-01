# frozen_string_literal: true

$LOAD_PATH.unshift File.dirname(__FILE__)

# The official source code library of alex-recker-dot-com!
module Blog
  autoload :Files, 'blog/files.rb'
  autoload :Logging, 'blog/logging.rb'
end
