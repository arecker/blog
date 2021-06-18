# frozen_string_literal: true

# Functions for running pieces of the blog program.
module Run
  # Prints a program greeting.
  def self.greeting
    section('BLOG ##') do
      log "version: v#{version}"
      log "commit: #{Git.label}"
    end
  end

  # Builds site data.
  def self.data
    section('building site data') do
      Build.info
      Build.nav
      Build.stats
      Build.projects
    end
  end

  # Builds site pages.
  def self.pages
    section('building site pages') do
      Build.sitemap
      Build.feed
    end
  end

  # Decorates a section
  def self.section(name, &block)
    log "## #{name} "
    yield block
    log ''
  end

  # Run the block and return the execution time difference
  def self.time_it
    start = Time.now
    yield
    stop = Time.now
    stop - start
  end
end
