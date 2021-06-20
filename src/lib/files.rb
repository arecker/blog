# frozen_string_literal: true

require 'pathname'
require 'time'

module Blog
  # Functions for working with files
  module Files
    # Returns the root of the blog project.  Should be something like
    # ~/src/blog
    def self.root
      File.expand_path(File.join(File.dirname(__FILE__), '../..'))
    end

    # Like File.join, except relative to the blog root.  Returns the blog
    # root if called withour args.
    def self.join(*args)
      rel = File.join(root, *args)
      File.expand_path rel
    end

    # Returns a list of entries.
    def self.entries
      @entries ||= Entry.build_paginated_list
    end

    # Returns a list of pages.
    def self.pages
      Dir.glob(Files.join('pages/*.html')).map { |f| Page.new f }
    end

    # Returns a list of ruby test files.
    def self.tests
      Dir.glob(Files.join('src/spec/test_*.rb'))
    end

    # Shorten a filepath relative to the root
    def self.shorten(path)
      path.delete_prefix("#{root}/")
    end

    # Generates a file.  Expects a path and a block that returns a
    # string.  Will report execution time and size.
    def self.generate(path, &block)
      size = 0
      elapsed = Run.time_it do
        content = yield block
        size = content.bytesize
        File.open(path, 'w') do |file|
          file.write(content)
        end
      end
      time = "#{elapsed.round(2)}s"
      Log.info "generated #{shorten(path)} (#{size} b) [#{time}]-> #{shorten(path)}"
    end

    # Joins a file path relative to the site root (www/ by default).
    def self.target(*args)
      join('www/', *args)
    end
  end
end
