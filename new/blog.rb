#!/usr/bin/env ruby
# -*- mode: ruby -*-
# frozen_string_literal: true

require 'date'
require 'fileutils'
require 'html-proofer'
require 'liquid'
require 'logger'
require 'open3'
require 'optparse'
require 'pathname'
require 'rack'
require 'redcarpet'
require 'shellwords'
require 'singleton'
require 'thin'
require 'time'
require 'yaml'

begin
  require 'liquid/debug'
rescue LoadError # rubocop:disable Lint/SuppressedException
end

CONFIG = {
  'author' => 'Alex Recker',
  'email' => 'alex@reckerfamily.com',
  'facebook_handle' => 'alex.recker.581',
  'github_handle' => 'arecker',
  'linkedin_handle' => 'alex-recker-a0316481',
  'timezone' => 'CST',
  'twitter_handle' => '@alex_recker',
  'url' => 'https://www.alexrecker.com'
}.freeze

# Blog
#
# The greatest static site generator in the universe.
module Blog
  def self.logger
    @logger ||= Logger.new(
      STDOUT,
      formatter: proc { |_sev, _dt, _name, msg| "blog: #{msg}\n" },
      level: Logger::INFO
    )
  end

  # Dates
  module Dates
    def timezone
      CONFIG.fetch('timezone', 'UTC')
    end

    def to_uyd_date(date)
      date.strftime('%A, %B %-d %Y')
    end

    def today
      @today ||= Date.today.to_datetime.new_offset(offset).to_date
    end

    def offset
      Time.zone_offset(timezone)
    end
  end

  # Files
  module Files
    def files(path)
      Dir["#{path}/**/*"].select { |o| File.file?(o) }
    end

    def root
      File.dirname(__FILE__)
    end

    def path(*subpaths)
      File.join(root, *subpaths)
    end

    def relpath(root, path)
      Pathname.new(path).relative_path_from(Pathname.new(root)).to_s
    end

    def webext(filename)
      special_exts = { '.md' => '.html' }
      newext = special_exts[File.extname(filename)]
      filename = File.basename(filename, '.*') + newext unless newext.nil?
      filename
    end

    def webpath(path)
      path = File.join(path, 'index.html') if File.extname(path).empty?
      path = File.join(File.dirname(path), webext(File.basename(path)))
      special_dirs = %w[pages entries] # treat these dirs like the root
      parts = relpath(root, path).split('/')
      parts = parts.drop(1) if special_dirs.include? parts.first
      '/' + parts.join('/')
    end

    def write(path, content)
      FileUtils.mkdir_p(File.dirname(path))
      File.open(path, 'w') { |f| f.write content }
    end
  end

  # Images
  module Images
    include Files

    def image_extensions
      ['.jpg', '.jpeg', '.png', '.bmp', '.svg']
    end

    def image?(filename)
      image_extensions.include? File.extname(filename)
    end

    def images
      files(path('images')).select { |f| image?(f) }
    end

    def banners
      files(path('images/banners')).select { |f| image?(f) }
    end

    def find_banner(basename)
      image_extensions.each do |ext|
        file = path('images/banners', basename + ext)
        return 'banners/' + File.basename(file) if File.exists? file
      end
      nil
    end
  end

  # Shell
  module Shell
    def self.run(cmd)
      out, err, status = Open3.capture3(cmd)
      return out if status.success?

      msg = <<~ERROR
        the command \`#{cmd}\` failed!
        --- exit
        #{status}
        --- stdout
        #{out}
        --- stderr
        #{err}
      ERROR

      raise msg
    end
  end

  # Text
  module Text
    def strip_metadata(txt)
      result = txt.split('---').last || ''
      result.lstrip
    end

    def parse_metadata(str)
      result = YAML.load(str)
      if result.is_a? Hash
        result
      else
        {}
      end
    rescue Psych::Exception
      {}
    end

    def extract_metadata(file)
      parse_metadata(File.read(file))
    end

    def markdown_to_html(src)
      markdown.render(src)
    end

    def markdown
      @markdown ||= ::Redcarpet::Markdown.new(
        Redcarpet::Render::HTML,
        fenced_code_blocks: true,
        space_after_headers: true
      )
    end
  end

  # Logging
  module Logging
    def self.included(base)
      base.extend(self)
    end

    def logger
      ::Blog.logger
    end
  end

  # Git
  module Git
    def self.shorthead
      Shell.run('git rev-parse --short HEAD').chomp
    end

    def self.head
      Shell.run('git rev-parse HEAD').chomp
    end
  end

  # Template Compiler
  class TemplateCompiler
    include Files
    include Singleton

    def layouts
      @layouts ||= dir_as_template_hash(path('layouts'))
    end

    def snippets
      @snippets ||= dir_as_template_hash(path('snippets'))
    end

    private

    def dir_as_template_hash(dir)
      results = {}
      files(dir).each do |file|
        contents = File.read(file)
        results[File.basename(file)] = Liquid::Template.parse(
          contents, error_mode: :strict
        )
      end
      results
    end
  end

  # Templating
  module Templating
    include Files
    include Text

    def template(str)
      ::Liquid::Template.parse(str, error_mode: :strict)
    end

    def templating
      TemplateCompiler.instance
    end
  end

  # Filters
  module Filters
    def filename_to_alt(filename)
      filename = filename.gsub('-', ' ')
      filename = filename.gsub(/.png|.jpg|.jpeg/, '')
      filename
    end
  end
  Liquid::Template.register_filter(Filters)

  # Tags
  module Tags
    # Nickname
    class Nickname < Liquid::Tag
      def render(_context)
        [
          'a big mess',
          'a goat rodeo',
          'a rats nest',
          'a single sprawling ruby script',
          'an absolute eye sore',
          'some shitty code I wrote',
          'some terrible ruby',
        ].sample
      end
    end
    Liquid::Template.register_tag('nickname', Nickname)

    # Link
    class Link < Liquid::Tag
      include Files
      include Text

      def initialize(name, markup, parse_context)
        super
        @page = markup.strip
      end

      def render(_ctx)
        href
      end

      def href
        metadata.fetch('permalink', webpath(target))
      end

      def metadata
        extract_metadata(target)
      end

      def target
        @target ||= path('pages', @page)
      end
    end
    Liquid::Template.register_tag('link', Link)

    # Image
    class Image < Liquid::Tag
      include Files

      def initialize(name, markup, parse_context)
        super
        @image = markup
      end

      def render(_context)
        webpath(path('images', @image))
      end
    end
    Liquid::Template.register_tag('image', Image)

    # Audio
    class Audio < Liquid::Tag
      include Files

      def initialize(name, markup, parse_context)
        super
        @file = markup
      end

      def render(_context)
        webpath(path('audio', @file))
      end
    end
    Liquid::Template.register_tag('audio', Audio)

    # Include
    class Include < Liquid::Tag
      include Files

      def initialize(name, markup, parse_context)
        super
        @markup = markup.strip.gsub("\n", ' ')
      end

      def render(context)
        rendered = try_resolve_values(context, options)
        TemplateCompiler.instance.snippets[filename].render(rendered)
      end

      def options
        @options ||= kwargs.map { |k| k.split('=') }.to_h
      end

      def kwargs
        Shellwords.split(@markup).drop(1)
      end

      def filename
        Shellwords.split(@markup).first
      end

      def try_resolve_values(context, hash)
        # TODO: lol GROSS
        rendered = {}
        hash.each do |k, v|
          result = context.find_variable(v)
          if result.nil?
            if v.include? '.'
              parent = context.find_variable(v.split('.').first)
              if parent.nil?
                result = v
              else
                result = v.split(".").drop(1).inject(parent) { |hash, key| hash[key] }
              end
            else
              result = v
            end
          end
          rendered[k] = result
        end
        rendered
      end
    end
    Liquid::Template.register_tag('include', Include)
  end

  # Page
  class Page
    include Files
    include Images
    include Logging
    include Templating
    include Text

    attr_reader :file, :site

    def initialize(file, site)
      @file = file
      @site = site
    end

    def templating
      site.templating
    end

    def src_dir
      path('pages')
    end

    def to_liquid
      {
        'description' => description,
        'filename' => target_filename,
        'permalink' => permalink,
        'title' => title,
        'url' => url,
        'banner' => banner
      }
    end

    def filename
      File.basename(@file)
    end

    def target_filename
      webext(filename)
    end

    def render!
      logger.debug "rendering page #{file} -> #{target}"
      write(target, render)
    end

    def content
      strip_metadata(File.read(file))
    end

    def pre_layout(result)
      if File.extname(file) == '.md'
        markdown_to_html(result)
      else
        result
      end
    end

    def render
      result = template(content).render(context)
      result = pre_layout(result)
      if layout == 'null'
        result
      else
        templating.layouts[layout].render(
          context.merge({ 'content' => result })
        )
      end
    end

    def context
      {
        'latest' => site.entries.first,
        'config' => CONFIG,
        'page' => self,
        'site' => site
      }
    end

    def banner
      find_banner(File.basename(filename, '.md'))
    end

    def title
      metadata['title']
    end

    def description
      metadata['description']
    end

    def layout
      metadata['layout'] || 'page.html'
    end

    def target
      trg = if File.extname(permalink).empty?
              File.join(permalink, 'index.html')
            else
              permalink
            end
      path('site', trg)
    end

    def permalink
      metadata['permalink'] || webpath(file)
    end

    def url
      CONFIG['url'] + permalink
    end

    def metadata
      @metadata ||= extract_metadata(file)
    end
  end

  # Entry
  class Entry < Page
    include Dates
    include Text

    attr_writer :next

    def self.list_from_files(files, site)
      entries = []
      entries << cur = new(files.shift, site) if files.any?
      while files.any? do
        entries << nxt = new(files.shift, site, previous: cur)
        cur.next = nxt
        cur = nxt
      end
      entries
    end

    def initialize(file, site, previous: nil)
      super(file, site)
      @previous = previous
      @next = nil
    end

    def src_dir
      path('entries')
    end

    def description
      metadata.fetch('title')
    end

    def date
      @date ||= Date.parse(File.basename(filename, '.md'))
    end

    def title
      to_uyd_date(date)
    end

    def to_liquid
      super.merge(
        {
          'previous' => @previous,
          'next' => @next
        }
      )
    end
  end

  # Feed
  class Feed
    include Files
    include Logging
    include Templating

    attr_reader :site

    def initialize(site)
      @site = site
    end

    def target
      path('site', site.config.fetch(:feed_path, '/feed.xml'))
    end

    def permalink
      webpath(target)
    end

    def render!
      logger.debug "rendering feed -> #{target}"
      write(target, render)
    end

    def render
      template(content).render(context)
    end

    def context
      {
        'site' => site
      }
    end

    def content
      <<~BOOYAKASHA
        <?xml version="1.0" encoding="utf-8"?>
        <feed xmlns="http://www.w3.org/2005/Atom">
          <title>Example Feed</title>
          <link href="http://example.org/"/>
          <updated>2003-12-13T18:30:02Z</updated>
          <author>
            <name>John Doe</name>
          </author>
          <id>urn:uuid:60a76c80-d399-11d9-b93C-0003939e0af6</id>
          <entry>
            <title>Atom-Powered Robots Run Amok</title>
            <link href="http://example.org/2003/12/13/atom03"/>
            <id>urn:uuid:1225c695-cfb8-4ebb-aaaa-80da344efa6a</id>
            <updated>2003-12-13T18:30:02Z</updated>
            <summary>Some text.</summary>
          </entry>
        </feed>
      BOOYAKASHA
    end

    def to_liquid
      {
        'path' => path
      }
    end
  end

  # Site
  class Site
    include Dates
    include Files
    include Logging
    include Templating

    def initialize(no_validate: false)
      @no_validate = no_validate
    end

    def config
      CONFIG
    end

    def validate?
      @no_validate != true
    end

    def render!
      pave!
      pages!
      entries!
      feed!
      statics!
      validate!
      coverage!
    end

    def pave!
      logger.info "rebuilding #{path('site')}"
      FileUtils.rm_rf path('site')
      FileUtils.mkdir_p path('site')
    end

    def pages!
      logger.info "rendering #{pages.count} page(s)"
      pages.each(&:render!)
    end

    def entries!
      logger.info "rendering #{entries.count} entries(s)"
      entries.each(&:render!)
    end

    def statics!
      %w[assets images docs audio].each do |dir|
        logger.info "copying #{path(dir)} -> #{path('site', dir)}"
        FileUtils.copy_entry(path(dir), path('site', dir))
      end
    end

    def feed!
      feed.render!
    end

    def coverage!
      logger.info "generating coverage report -> #{path('site/coverage')}"
      Shell.run 'rspec'
    end

    def validate!
      unless validate?
        logger.info "(skipping HTML validation)"
        return
      end
      logger.info "validating generated html in #{path('site')}"
      HTMLProofer.check_directory(
        path('site'),
        file_ignore: [path('site/coverage/index.html')],
        disable_external: true,
        log_level: :error,
      ).run
    end

    def pages
      @pages ||= files(path('pages')).map { |f| Page.new(f, self) }
    end

    def entries
      @entries ||= Entry.list_from_files(files(path('entries')).sort.reverse, self)
    end

    def feed
      @feed ||= Feed.new(self)
    end

    def to_liquid
      {
        'HEAD' => Git.head,
        'config' => config,
        'entries' => entries,
        'feed' => feed,
        'last_updated' => to_uyd_date(today),
        'latest' => entries.first,
        'pages' => pages,
        'shorthead' => Git.shorthead,
        'year' => today.year,
      }
    end
  end

  # Runner
  class Runner
    attr_reader :subcommand

    ALLOWED_SUBCOMMANDS = [
      'build',
      'serve',
      'watch',
    ]

    def initialize(argv)
      parser.parse(argv)
      @subcommand = argv.pop
    end

    def valid?
      ALLOWED_SUBCOMMANDS.include? subcommand
    end

    def verbose?
      options[:verbose] == true
    end

    def banner
      "Usage: blog.rb -v <#{ALLOWED_SUBCOMMANDS.join('|')}>"
    end

    def options
      @options ||= {}
    end

    def parser
      @parser ||= OptionParser.new { |opts| make_options(opts) }
    end

    def run!
      preflight!
      case subcommand
      when 'build'
        build!
      when 'serve'
        build!
        serve!
      end
    end

    def build!
      site = Site.new(no_validate: options[:no_validate])
      site.render!
    end

    def serve!
      Rack::Handler::Thin.run(
        Rack::Builder.new do
          use(Rack::Static, urls: [''], root: 'site', index: 'index.html')
          run ->(_env) { [200, {}, ['hello!']] }
        end, Host: '0.0.0.0', Port: 4000
      )
    end

    private

    def preflight!
      bail! unless valid?
      Blog.logger.level = ::Logger::DEBUG if verbose?
    end

    def bail!
      puts banner
      exit(-1)
    end

    def make_options(opts)
      opts.banner = banner
      opts.on('-v', '--verbose') { |_t| options[:verbose] = true }
      opts.on('-n', '--no-validate') { |_o| options[:no_validate] = true }
    end
  end

  def self.run!
    parser = Runner.new(ARGV)
    parser.run!
  end
end

Blog.run! if __FILE__ == $PROGRAM_NAME
