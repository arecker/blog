#!/usr/bin/env ruby
# -*- mode: ruby -*-
# frozen_string_literal: true

require 'date'
require 'fastimage'
require 'fileutils'
require 'html-proofer'
require 'json'
require 'liquid'
require 'logger'
require 'mini_magick'
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
  'timezone' => 'CST',
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
    def slice_by_consecutive(dates)
      dates.slice_when { |p, c| c != p - 1 && c != p + 1 }.to_a
    end

    def calculate_streaks(dates)
      slice_by_consecutive(dates).map do |pair|
        first, last = pair.minmax
        {
          'days' => (last - first).to_i,
          'start' => first,
          'end' => last
        }
      end
    end

    def time_to_date(time)
      ::Date.parse(time.strftime('%Y-%m-%d'))
    end

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

  # Math
  module Math
    def average(numlist)
      calc = numlist.inject { |sum, el| sum + el }.to_f / numlist.size
      calc.round
    end

    def total(numlist)
      numlist.inject(0) { |sum, x| sum + x }
    end

    def occurences(keys, targets)
      results = Hash.new(0)
      targets.each do |target|
        results[target] += 1 if keys.include? target
      end
      results
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

    def dimensions(file)
      result = FastImage.size(file)
      if result.instance_of?(String)
        result.split('x').map(&:to_i)
      else
        result
      end
    end

    def resize(file, dims)
      image = MiniMagick::Image.new(file)
      image.resize "#{dims.first}x#{dims.last}"
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
      txt.sub(/\A---(.|\n)*?---/, '').lstrip
    end

    def parse_metadata(str)
      result = YAML.safe_load(str)
      if result.is_a? Hash
        result
      else
        {}
      end
    rescue Psych::Exception
      {}
    end

    def extract_metadata(file)
      split = File.read(file).split('---')
      if split.count >= 3
        parse_metadata(split[1])
      else
        {}
      end
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

    def to_words(str)
      str.split.map do |token|
        token.gsub!(/[^0-9a-z ']/i, '')
        token.downcase
      end
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

    def self.commit_count
      Shell.run('git rev-list --count master').chomp
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

  # Stats
  class Stats
    include Math
    include Dates

    attr_reader :entries

    def initialize(entries)
      @entries = entries
    end

    def to_liquid
      {
        'total_words' => total(word_counts),
        'average_words' => average(word_counts),
        'total_posts' => entries.size,
        'consecutive_posts' => consecutive_posts
      }
    end

    private

    def consecutive_posts
      calculate_streaks(entries.collect(&:date)).first['days']
    end

    def word_counts
      @word_counts ||= entries.collect(&:word_count)
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

    def pretty_number(num)
      num.to_s.reverse.gsub(/(\d{3})(?=\d)/, '\\1,').reverse
    end
  end
  Liquid::Template.register_filter(Filters)

  # Tags
  module Tags
    # Nickname
    class Nickname < Liquid::Tag
      def render(_context)
        [
          'a sprawling mess of ruby'
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

    # Asset
    class Asset < Liquid::Tag
      include Files

      def initialize(name, markup, parse_context)
        super
        @file = markup
      end

      def render(_context)
        webpath(path('assets', @file))
      end
    end
    Liquid::Template.register_tag('asset', Asset)

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

    def initialize(file)
      @file = file
    end

    def src_dir
      path('pages')
    end

    def to_liquid
      metadata.merge(
        {
          'description' => description,
          'filename' => target_filename,
          'permalink' => permalink,
          'title' => title,
          'url' => url,
          'banner' => banner
        }
      )
    end

    def filename
      File.basename(@file)
    end

    def target_filename
      webext(filename)
    end

    def render!(ctx = {})
      logger.debug "rendering page #{file} -> #{target}"
      write(target, render(ctx))
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

    def render(ctx = {})
      full_ctx = ctx.merge(context)
      result = template(content).render(full_ctx)
      result = pre_layout(result)
      if layout == 'null'
        result
      else
        templating.layouts[layout].render(
          full_ctx.merge({ 'content' => result })
        )
      end
    end

    def context
      {
        'page' => self
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

    def self.list_from_files(files)
      entries = []
      entries << cur = new(files.shift) if files.any?
      while files.any?
        entries << nxt = new(files.shift, previous: cur)
        cur.next = nxt
        cur = nxt
      end
      entries
    end

    def initialize(file, previous: nil)
      super(file)
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

    def words
      to_words(content)
    end

    def word_count
      @word_count ||= words.size
    end
  end

  # Builder
  class Builder
    include Files
    include Images
    include Logging

    def self.generate_all!
      context = {}
      builders = descendants.map(&:new)
      builders.each { |b| context.merge!(b.context) }
      builders.each { |b| b.generate(context) }
    end

    def self.descendants
      ObjectSpace.each_object(Class).select { |klass| klass < self }
    end

    def initialize; end

    def generate(_ctx); end

    def context
      {}
    end
  end

  # Config Generator
  class ConfigBuilder < Builder
    def context
      { 'config' => CONFIG }
    end
  end

  # Date Builder
  class DateBuilder < Builder
    include Dates

    def context
      {
        'last_updated' => to_uyd_date(today),
        'year' => today.year,
      }
    end
  end

  # Git Builder
  class GitBuilder < Builder
    def context
      {
        'git' => {
          'commit_count' => Git.commit_count,
          'HEAD' => Git.head,
          'shorthead' => Git.shorthead
        }
      }
    end
  end

  # Static Builder
  class StaticBuilder < Builder
    def dirs
      @dirs ||= %w[
        assets
        audio
        docs
        vids
      ].sort.select { |f| File.directory? path(f) }
    end

    def generate(_ctx)
      logger.info "copying #{dirs.count} static dir(s) -> site/{#{dirs.join(',')}}"
      dirs.each do |dir|
        src = path(dir)
        trg = path('site', dir)
        logger.debug "copying #{src} -> #{trg}"
        FileUtils.copy_entry(src, trg)
      end
    end
  end

  # Docs Builder
  class DocsBuilder < Builder
    def generate(_ctx)
      logger.info "generating documentation -> #{target}"
      Shell.run "yard #{options}  #{path('blog.rb')}"
    end

    def options
      "-o #{target} -r #{path('README.md')} -q"
    end

    def context
      {
        'docs_permalink' => docs_permalink
      }
    end

    def target
      path('site', docs_permalink)
    end

    def docs_permalink
      '/docs/'
    end
  end

  # Coverage Builder
  class CoverageBuilder < Builder
    def context
      logger.info "generating coverage report -> #{path('site/coverage')}"
      Shell.run 'rspec'
      {
        'coverage' => results['metrics']
      }
    end

    def results
      @results ||= JSON.parse(File.read(expected_results_path))
    end

    def expected_results_path
      path('tmp', 'coverage.json')
    end
  end

  # Image Builder
  class ImageBuilder < Builder
    def generate(_ctx)
      resizeable_images.each do |image|
        logger.info "resizing #{image}"
        resize(image, [800, 800])
      end
      FileUtils.copy_entry(src, target)
      logger.info "caching #{images.count} image(s) -> #{target}"
    end

    def resizeable_images
      images.select { |i| too_big?(dimensions(i)) }
    end

    def target
      path('site', 'images')
    end

    def src
      path('images')
    end

    def too_big?(dimensions)
      dimensions.first > 800 || dimensions.last > 800
    end
  end

  # Entry Builder
  class EntryBuilder < Builder
    def generate(ctx)
      logger.info "rendering #{entries.count} entries(s)"
      entries.each do |entry|
        entry.render!(ctx)
      end
    end

    def context
      {
        'entries' => entries,
        'latest' => entries.first,
        'stats' => Stats.new(entries)
      }
    end

    def entries
      @entries ||= Entry.list_from_files(entry_files)
    end

    private

    def entry_files
      files(path('entries')).sort.reverse
    end
  end

  # Page Builder
  class PageBuilder < Builder
    def generate(ctx)
      logger.info "rendering #{pages.count} page(s)"
      pages.each do |page|
        page.render!(ctx)
      end
    end

    def context
      {
        'pages' => pages
      }
    end

    def pages
      @pages ||= page_files.map { |f| Page.new(f) }
    end

    private

    def page_files
      files(path('pages')).sort
    end
  end

  # Feed Builder
  class FeedBuilder < Builder
    include Templating

    def target
      path('site', permalink)
    end

    def permalink
      '/feed.xml'
    end

    def generate(ctx)
      logger.info "rendering feed -> #{target}"
      write(target, render(ctx))
    end

    def render(ctx = {})
      template(content).render(ctx.merge(context))
    end

    def context
      {
        'feed_permalink' => permalink
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
            <name>{{ config.author }}</name>
          </author>
          <id>{{ config.url }}</id>
          {% for entry in entries %}
          <entry>
            <title>{{ entry.title }}</title>
            <link href="{{ entry.url }}"/>
            <id>{{ entry.url }}</id>
            <updated>2003-12-13T18:30:02Z</updated>
            <summary><![CDATA[{{ entry.description }}]]></summary>
          </entry>
          {% endfor %}
        </feed>
      BOOYAKASHA
    end
  end

  # Runner
  class Runner
    include Files
    include Logging

    attr_reader :subcommand

    ALLOWED_SUBCOMMANDS = [
      'build',
      'serve',
      'watch'
    ]

    def initialize(argv)
      parser.parse(argv)
      @subcommand = argv.pop
    end

    def valid?
      ALLOWED_SUBCOMMANDS.include? subcommand
    end

    def validate?
      options[:no_validate] != true
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
      pave!
      Builder.generate_all!
      if validate?
        validate!
      else
        logger.info '(skipping HTML validation)'
      end
    end

    def pave!
      FileUtils.rm_rf path('site')
      FileUtils.mkdir_p path('site')
    end

    def serve!
      Rack::Handler::Thin.run(
        Rack::Builder.new do
          use(Rack::Static, urls: [''], root: 'site', index: 'index.html')
          run ->(_env) { [200, {}, ['hello!']] }
        end, Host: '0.0.0.0', Port: 4000
      )
    end

    def validate!
      logger.info "validating #{validate_files_count} pages(s) -> #{path('site')}/**/*.html"
      HTMLProofer.check_directory(
        path('site'),
        file_ignore: ignore_files,
        disable_external: true,
        log_level: :error
      ).run
    end

    private

    def validate_files_count
      files(path('site')).count - ignore_files.count
    end

    def ignore_files
      @ignore_files ||= [path('site/coverage/index.html'), files(path('site/docs'))].flatten
    end

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
