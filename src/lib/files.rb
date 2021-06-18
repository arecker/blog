# frozen_string_literal: true

require 'pathname'
require 'time'

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
    Dir.glob(Files.join('_posts/*.md')).sort.map { |f| Entry.new f }
  end

  # Returns a list of pages.
  def self.pages
    Dir.glob(Files.join('_pages/*.html'))
  end

  # Returns a list of ruby test files.
  def self.tests
    Dir.glob(Files.join('src/spec/test_*.rb'))
  end

  # Shorten a filepath relative to the root
  def self.shorten(path)
    path.delete_prefix("#{root}/")
  end

  # Writes a file (and reports the size of the file)
  def self.write(path, content)
    start = Time.now
    File.open(path, 'w') do |file|
      file.write(content)
    end
    stop = Time.now
    size = File.size(path)
    time = "#{(stop - start).round(2)} s"
    log "generated #{shorten(path)} (#{size} b) [#{time}]-> www/#{shorten(path)}"
  end

  # Joins a file path relative to the site root (www/ by default).
  def self.target(*args)
    join(*args)
  end
end
