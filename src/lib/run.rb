# frozen_string_literal: true

module Blog
  # Functions for running pieces of the blog program.
  module Run
    # Returns the blog version string.
    def self.version
      @version ||= IO.read(Files.join('src/VERSION')).chomp
    end

    # Prints a program greeting.
    def self.greeting
      section('BLOG ##') do
        Log.info "version: v#{version}"
        Log.info "commit: #{Git.label}"
      end
    end

    # Builds site feeds.
    def self.feeds
      section('building site feeds') { Feeds.generate_all }
    end

    # Builds site pages.
    def self.pages
      section('building site pages') { Page.generate_all }
    end

    # Builds site entries.
    def self.entries
      section('building site entries') { Entry.generate_all }
    end

    # Decorates a section
    def self.section(name, &block)
      Log.info "## #{name} "
      yield block
      Log.info ''
    end

    # Run the block and return the execution time difference
    def self.time_it
      start = Time.now
      yield
      stop = Time.now
      stop - start
    end
  end
end
