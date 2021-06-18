#!/usr/bin/env ruby

# frozen_string_literal: true

$LOAD_PATH.unshift File.dirname(__FILE__)

require 'yaml'

autoload :Build, 'lib/build'
autoload :Entry, 'lib/entry'
autoload :Files, 'lib/files'
autoload :Git, 'lib/git'
autoload :Nav, 'lib/nav'
autoload :Projects, 'lib/projects'
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

# Decorates a section
def section(name, &block)
  log "## #{name} "
  yield block
  log ''
end

# Run the block and return the execution time difference
def time_it
  start = Time.now
  yield
  stop = Time.now
  stop - start
end

# Runs the main blog routine.
def main
  section('starting BLOG') do
    log "current version:  v#{version}"
    log "current last commit: #{Git.label}"
  end

  time = time_it do
    section('generating site data') do
      Build.info
      Build.nav
      Build.stats
      Build.projects
    end

    section('building site pages') do
      Build.sitemap
      Build.feed
    end
  end

  section('report') do
    log "total build time: #{time.round(4)}s"
  end
end

main if __FILE__ == $PROGRAM_NAME
