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
require 'thin'
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
      formatter: proc { |_sev, _dt, _name, msg| "blog: #{msg}\n" }
    )
  end

  # Dates
  module Dates
    def uyd(date)
      date.strftime('%A, %B %-d %Y')
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

    def webpath(path)
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
    def image?(filename)
      extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.svg']
      extensions.include? File.extname(filename)
    end

    def images
      files(path('images')).select { |f| image?(f) }
    end

    def banners
      files(path('images/banners')).select { |f| image?(f) }
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

    def markdown_to_html(src)
      markdown.render(src)
    end

    def markdown
      @markdown ||= ::Redcarpet::Markdown.new(Redcarpet::Render::HTML)
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

  # Template
  module Template
    include Files
    include Text

    def template(str)
      ::Liquid::Template.parse(str, error_mode: :strict)
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
    # Version
    class Include < Liquid::Tag
      include Files
      include Template

      def initialize(name, markup, parse_context)
        super
        @markup = markup.strip.gsub("\n", ' ')
        raise "#{filename} does not exist" unless File.exist? filename
      end

      def render(context)
        rendered = try_resolve_values(context, options)
        template(File.read(filename)).render(rendered)
      end

      def options
        @options ||= kwargs.map { |k| k.split('=') }.to_h
      end

      def kwargs
        Shellwords.split(@markup).drop(1)
      end

      def filename
        path('snippets', Shellwords.split(@markup).first)
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
    include Logging
    include Template
    include Text

    attr_reader :file, :site

    def initialize(file, site)
      @file = file
      @site = site
    end

    def to_liquid
      {
        'description' => description,
        'filename' => filename,
        'permalink' => permalink,
        'title' => title,
        'url' => url
      }
    end

    def filename
      File.basename(@file)
    end

    def render!
      logger.debug "rendering page #{file} -> #{target}"
      write(target, render)
    end

    def content
      strip_metadata(File.read(file))
    end

    def render
      result = template(content).render(context)
      if layout.nil?
        result
      else
        template(File.read(path('layouts', layout))).render(
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

    def title
      metadata.fetch('title')
    end

    def description
      metadata.fetch('description')
    end

    def layout
      metadata['layout'] || 'page.html'
    end

    def target
      if permalink.end_with? '/'
        path('site', permalink, 'index.html')
      else
        path('site', permalink)
      end
    end

    def permalink
      metadata.fetch('permalink', webpath(file))
    end

    def url
      CONFIG['url'] + permalink
    end

    def metadata
      @metadata ||= load_metadata
    end

    private

    def load_metadata
      result = YAML.load_file(file)
      if result.is_a? Hash
        result
      else
        {}
      end
    end
  end

  # Entry
  class Entry < Page
    include Dates
    include Images
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

    def render
      result = template(content).render(context)
      result = markdown_to_html(result)
      if layout.nil?
        result
      else
        template(File.read(path('layouts', layout))).render(
          context.merge({ 'content' => result })
        )
      end
    end

    def description
      metadata.fetch('title')
    end

    def date
      @date ||= Date.parse(File.basename(filename, '.md'))
    end

    def permalink
      webpath(target_filename)
    end

    def title
      uyd(date)
    end

    def target_filename
      File.basename(filename, '.md') + '.html'
    end

    def target
      path('site', target_filename)
    end

    def banner
      basename = File.basename(filename, '.md')
      result = banners.find { |i| File.basename(i, '.*') == basename }
      'banners/' + File.basename(result) unless result.nil?
    end

    def to_liquid
      super.merge(
        {
          'banner' => banner,
          'previous' => @previous,
          'next' => @next,
          'filename' => target_filename
        }
      )
    end
  end

  # Site
  class Site
    include Files
    include Logging

    def render!
      pave!
      pages!
    end

    def pave!
      logger.info "rebuilding #{path('site')}"
      FileUtils.rm_rf path('site')
      FileUtils.mkdir_p path('site')
    end

    def pages!
      logger.info "rendering #{pages.count} page(s)"
      pages.each(&:render!)
      logger.info "rendering #{entries.count} page(s)"
      entries.each(&:render!)
    end

    def pages
      @pages ||= files(path('pages')).map { |f| Page.new(f, self) }
    end

    def entries
      @entries ||= Entry.list_from_files(files(path('entries')).sort.reverse, self)
    end

    def to_liquid
      {
        'latest' => entries.first,
        'entries' => entries,
        'shorthead' => Git.shorthead,
        'HEAD' => Git.head,
        'year' => Date.today.year,
        'last_updated' => Date.today.strftime('%A, %B %-d %Y')
      }
    end
  end

  # Builder
  class Builder
    include Files
    include Logging

    attr_reader :site

    def initialize
      @site = Site.new
    end

    def build!
      site.render!
      statics!
      logger.info "generating coverage report -> #{path('site/coverage')}"
      Shell.run 'rspec'

      logger.info "validating generated html in #{path('site')}"
      # HTMLProofer.check_directory(
      #   path('site'),
      #   file_ignore: [path('site/coverage/index.html')],
      #   disable_external: true,
      #   log_level: :error,
      # ).run
    end

    def statics!
      %w[assets images docs].each do |dir|
        logger.info "copying #{path(dir)} -> #{path('site', dir)}"
        FileUtils.copy_entry(path(dir), path('site', dir))
      end
    end
  end

  # ArgParser
  class ArgParser
    attr_reader :subcommand

    ALLOWED_SUBCOMMANDS = [
      'build',
      'serve',
      'watch',
    ]

    def initialize(argv)
      parser.parse(argv, into: options)
      @subcommand = argv.pop
    end

    def verbose?
      options.fetch(:verbose, false)
    end

    def valid?
      ALLOWED_SUBCOMMANDS.include? subcommand
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

    def bail!
      puts banner
      exit -1
    end

    private
    
    def make_options(opts)
      opts.banner = banner
      opts.on('-v', '--verbose') { |t| options[:verbose] = t }
    end
  end

  def self.build!
    Builder.new.build!
  end

  def self.serve!
    build!
    Rack::Handler::Thin.run(
      Rack::Builder.new {
        use(Rack::Static, urls: [""], :root => 'site', :index => 'index.html')
        run ->env{[200, {}, ["hello!"]]}
      }, Host: '0.0.0.0', Port: 4000
    )
  end

  def self.run!
    parser = ArgParser.new(ARGV)
    parser.bail! unless parser.valid?
    case parser.subcommand
    when 'build'
      build!
    when 'serve'
      serve!
    end
  end
end

Blog.run! if __FILE__ == $PROGRAM_NAME
