#!/usr/bin/env ruby

# frozen_string_literal: true

$LOAD_PATH.unshift File.dirname(__FILE__)

require 'yaml'

autoload :Build, 'lib/build'
autoload :Entry, 'lib/entry'
autoload :Files, 'lib/files'
autoload :Git, 'lib/git'
autoload :Info, 'lib/info'
autoload :Markdown, 'lib/markdown'
autoload :Nav, 'lib/nav'
autoload :Page, 'lib/page'
autoload :Projects, 'lib/projects'
autoload :Run, 'lib/run'
autoload :Shell, 'lib/shell'
autoload :Stats, 'lib/stats'
autoload :Template, 'lib/template'

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
    # Run.pages
  end

  Run.section('build report') do
    log "total time: #{time.round(2)}s"
  end
end

main if __FILE__ == $PROGRAM_NAME
