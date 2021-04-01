# frozen_string_literal: true

$LOAD_PATH.unshift File.dirname(__FILE__)

# The official source code library of _alex-recker-dot-com_!
module Blog
  autoload :Files, 'blog/files.rb'
  autoload :Logging, 'blog/logging.rb'
end
