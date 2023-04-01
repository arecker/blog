#!/usr/bin/env ruby
# frozen_string_literal: true

require 'date'
require 'erb'
require 'logger'
require 'ostruct'

logger = Logger.new($stdout)
logger.level = Logger::INFO

module Blog
  class Site
    attr_reader :protocol, :domain

    def initialize(protocol, domain)
      @protocol = protocol
      @domain = domain
    end
  end

  class Entry
    attr_reader :path

    def initialize(path)
      @path = path
    end

    def filename
      File.basename(path)
    end

    def to_s
      "Entry <#{filename}>"
    end

    def slug
      File.basename(filename, '*.html')
    end

    def date
      DateTime.strptime(slug, '%Y-%m-%d')
    end

    def title
      date.strftime('%A, %B %-d %Y')
    end

    def content
      @content ||= File.read(path)
    end

    def metadata
      @metadata ||= parse_metadata(content)
    end

    def parse_metadata(content)
      pattern = /^\s?<!--\s?meta:(?<key>[A-za-z]+)\s?(?<value>.*)\s?-->$/
      Hash[content.scan(pattern)]
    end

    def subtitle
      metadata.fetch('title')
    end

    def banner
      metadata['banner']
    end
  end

  def self.clean_webroot(www_dir)
    www_dir += '/' unless www_dir.end_with?('/')
    targets = Dir["#{www_dir}*.html"] + Dir["#{www_dir}*.xml"]
    targets.each { |p| File.delete(p) }
    targets.length
  end

  def self.load_entries(entries_dir)
    entries_dir += '/' unless entries_dir.end_with?('/')
    entries = Dir["#{entries_dir}*.html"]
    entries.map { |p| Entry.new p }.reverse
  end

  def self.render_page(page, layout, site)
    template = ERB.new layout
    namespace = OpenStruct.new(page: page, site: site)
    template.result(namespace.instance_eval { binding })
  end
end

www_dir = './www'
logger.info "removed #{Blog.clean_webroot(www_dir)} old target(s)"

entries = Blog.load_entries('./entries')
logger.info "loaded #{entries.length} entries"

www_dir += '/' unless www_dir.end_with? '/'
total_entries = entries.length
layout = File.read('./pages/_layout.html')
site = Blog::Site.new(protocol='https', domain='www.alexrecker.com')
entries.each_with_index do |e, i|
  content = Blog.render_page(e, layout, site)
  File.open("./#{www_dir}#{e.filename}", 'w') { |f| f.write(content) }
  logger.debug "wrote #{e.filename}"
  logger.info "wrote #{i + 1}/#{total_entries} entries" if (i % 100).zero? || i == total_entries - 1
end
