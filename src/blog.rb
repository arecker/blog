#!/usr/bin/env ruby

# frozen_string_literal: true

$LOAD_PATH.unshift File.dirname(__FILE__)

require 'yaml'

autoload :Context, 'lib/context'
autoload :Entry, 'lib/entry'
autoload :Feeds, 'lib/feeds'
autoload :Files, 'lib/files'
autoload :Git, 'lib/git'
autoload :Info, 'lib/info'
autoload :Lists, 'lib/lists'
autoload :Markdown, 'lib/markdown'
autoload :Nav, 'lib/nav'
autoload :Page, 'lib/page'
autoload :Projects, 'lib/projects'
autoload :Run, 'lib/run'
autoload :Serve, 'lib/serve'
autoload :Shell, 'lib/shell'
autoload :Stats, 'lib/stats'
autoload :Template, 'lib/template'

# 3rd party libraries
autoload :Kramdown, 'lib/kramdown'
autoload :Parallel, 'lib/parallel'

# Logs a message for the user.
def log(msg)
  puts "blog :: #{msg}"
end

# Returns the blog version string.
def version
  @version ||= IO.read(Files.join('src/VERSION')).chomp
end

# Runs the main blog routine.
def main
  Run.greeting

  time = Run.time_it do
    Run.data
    Run.feeds
    Run.pages
    Run.entries
  end

  Run.section('build report') do
    log "total time: #{time.round(2)}s"
  end
end

main if __FILE__ == $PROGRAM_NAME
