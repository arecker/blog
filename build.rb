#!/usr/bin/env ruby
# frozen_string_literal: true

require 'date'
require 'erb'
require 'logger'
require 'ostruct'

logger = Logger.new($stdout)
logger.level = Logger::INFO

# Blog - source code library
module Blog
  # Site - global website metadata
  class Site
    attr_reader :protocol, :domain, :author, :year, :title, :subtitle

    def initialize(protocol:, domain:, author:, title:, subtitle:)
      @protocol = protocol
      @domain = domain
      @author = author
      @year = year
      @title = title
      @subtitle = subtitle

      now = Time.now
      @year = now.year
    end
  end

  # Page - blog page object
  class Page
    attr_reader :path

    def initialize(path)
      @path = path
    end

    def to_s
      "<Page #{filename}>"
    end

    def filename
      File.basename(path)
    end

    def slug
      File.basename(filename, '*.html')
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

    def title
      metadata.fetch('title')
    end

    def subtitle
      metadata.fetch('subtitle')
    end

    def banner
      metadata['banner']
    end

    def subindex
      metadata['subindex']
    end

    def next
      metadata['next']
    end

    def previous
      metadata['previous']
    end

    def render(*args, **kwargs)
      # setup context
      namespace = OpenStruct.new(*args, **kwargs)

      # render innder page
      template = ERB.new(content, trim_mode: '-')
      inner = template.result(namespace.instance_eval { binding })

      # indent
      inner.split("\n").map { |l| "      #{l}" }.join("\n").lstrip
    end
  end

  # Entry - journal entry object
  class Entry < Page
    attr_accessor :next, :previous

    def to_s
      "<Entry #{filename}>"
    end

    def date
      DateTime.strptime(slug, '%Y-%m-%d')
    end

    def title
      date.strftime('%A, %B %-d %Y')
    end

    def render(*_args, **_kwargs)
      # child page is not a template, so just read it
      content.split("\n").map { |l| "      #{l}" }.join("\n").lstrip
    end

    def subtitle
      metadata.fetch('title')
    end

    def subindex
      'entries'
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
    entries = entries.map { |p| Entry.new p }.reverse
    paginate_entries(entries)
  end

  def self.paginate_entries(entries)
    entries.each_with_index do |e, i|
      e.previous = entries[i - 1].filename if i.positive?
      e.next = entries[i + 1].filename unless i == (entries.length - 1)
    end
    entries
  end

  def self.load_pages(pages_dir)
    pages_dir += '/' unless pages_dir.end_with?('/')
    pages = Dir["#{pages_dir}*.html"]
    pages.map { |p| Page.new p }.keep_if { |p| !p.filename.start_with?('_') }
  end

  def self.render_page(layout:, page:, site:, entries:, pages:)
    context = { page: page, site: site, entries: entries, pages: pages }
    context[:content] = page.render(**context)
    template = ERB.new(layout, trim_mode: '-')
    namespace = OpenStruct.new(**context)
    template.result(namespace.instance_eval { binding })
  end

  def self.render_feed(site: nil, entries: nil)
    context = { site: site, entries: entries }
    layout = File.read('./pages/_feed.xml')
    template = ERB.new(layout, trim_mode: '-')
    namespace = OpenStruct.new(**context)
    template.result(namespace.instance_eval { binding })
  end
end

www_dir = './www'
logger.info "removed #{Blog.clean_webroot(www_dir)} old target(s)"

entries = Blog.load_entries('./entries')
logger.info "loaded #{entries.length} entries"

pages = Blog.load_pages('./pages')
logger.info "loaded #{pages.length} page(s)"

www_dir += '/' unless www_dir.end_with? '/'
total_entries = entries.length
layout = File.read('./pages/_layout.html')
site = Blog::Site.new(
  title: 'alexrecker.com',
  subtitle: 'a personal website',
  protocol: 'https',
  domain: 'www.alexrecker.com',
  author: 'Alex Recker'
)
total_pages = pages.length
pages.each_with_index do |p, i|
  content = Blog.render_page(page: p, layout: layout, site: site, entries: entries, pages: pages)
  File.open("./#{www_dir}#{p.filename}", 'w') { |f| f.write(content) }
  logger.info "wrote #{p} (#{i + 1}/#{total_pages})"
end

entries.each_with_index do |e, i|
  content = Blog.render_page(page: e, layout: layout, site: site, entries: entries, pages: pages)
  File.open("./#{www_dir}#{e.filename}", 'w') { |f| f.write(content) }
  logger.debug "wrote #{e}"
  logger.info "wrote #{i + 1}/#{total_entries} entries" if ((i + 1) % 100).zero? || i == total_entries - 1
end

File.open("./#{www_dir}/feed.xml", 'w') do |f|
  content = Blog.render_feed(site: site, entries: entries)
  f.write(content)
end
logger.info 'wrote feed.xml'
