#!/usr/bin/env ruby
# -*- mode: ruby -*-
# frozen_string_literal: true

require 'date'
require 'fileutils'
require 'html-proofer'
require 'json'
require 'liquid'
require 'logger'
require 'open3'
require 'optparse'
require 'pathname'
require 'redcarpet'
require 'shellwords'
require 'singleton'
require 'time'
require 'yaml'

begin
  require 'liquid/debug'
rescue LoadError # rubocop:disable Lint/SuppressedException
end

CONFIG = {
  'author' => 'Alex Recker',
  'email' => 'alex@reckerfamily.com',
  'title' => 'Dear Journal',
  'description' => 'Daily, public journal by Alex Recker',
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

    def date_to_time(date)
      date.to_time.to_datetime
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

    def now
      @now ||= DateTime.now.new_offset(offset)
    end

    def offset
      Time.zone_offset(timezone)
    end

    def parse_date(datestr)
      ::Date.parse(datestr).to_datetime.new_offset(offset).to_date
    end
  end

  # Dependencies
  module Dependencies
    def self.graphs?
      require 'gruff'
      true
    rescue LoadError
      false
    end

    def self.server?
      require 'rack'
      require 'thin'
      true
    rescue LoadError
      false
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
      Dir[File.join(path, '/**/*')].select { |o| File.file?(o) }
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
  end

  # Graphs
  module Graphs
    def self.generate_graphs(ctx)
      WordCount.new(ctx).write
      Swears.new(ctx).write
    end

    # Base Graph
    module Base
      include Files

      attr_reader :ctx

      def initialize(ctx)
        @ctx = ctx
      end

      def graphs_join(path)
        path('images/graphs', path)
      end
    end

    # Word Count Graph
    class WordCount
      include Base

      def posts
        ctx['entries'][0..6].reverse
      end

      def word_counts
        posts.collect(&:word_count)
      end

      def title
        format = '%m/%d/%y'
        first = posts.first.date.strftime(format)
        last = posts.last.date.strftime(format)
        "Word Count: #{first} - #{last}"
      end

      def labels
        Hash[posts.each_with_index.map { |p, i| [i, p.date.strftime('%a')] }]
      end

      def write
        g = ::Gruff::Line.new('800x600')
        g.theme = Gruff::Themes::PASTEL
        g.hide_legend = true
        g.labels = labels
        g.data :words, word_counts
        g.title = title
        g.x_axis_label = 'Day'
        g.y_axis_label = 'Word Count'
        g.minimum_value = 0
        g.write(graphs_join('words.png'))
      end
    end

    # Swears Chart
    class Swears
      include Base

      def results
        data = ctx['stats'].swear_results.clone
        data.delete('total')
        data
      end

      def write
        g = ::Gruff::Pie.new('800x600')
        g.theme = Gruff::Themes::PASTEL
        g.hide_legend = false
        g.legend_at_bottom = true
        g.minimum_value = 0
        results.each { |w, n| g.data w, n }
        g.write(graphs_join('swears.png'))
      end
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
        'consecutive_posts' => consecutive_posts,
        'swears' => swear_results
      }
    end

    def swear_results
      @swear_results ||= calculate_swears
    end

    private

    def consecutive_posts
      calculate_streaks(entries.collect(&:date)).first['days']
    end

    def word_counts
      @word_counts ||= entries.collect(&:word_count)
    end

    def words
      entries.collect(&:words).flatten
    end

    def calculate_swears
      results = Hash[count_swears]
      results['total'] = total(results.values)
      results
    end

    def count_swears
      occurences(swears, words).reject { |_k, v| v.zero? }.sort_by { |_k, v| -v }
    end

    def swears
      %w[
        ass
        asshole
        booger
        crap
        damn
        fart
        fuck
        hell
        jackass
        piss
        poop
        shit
      ]
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
      metadata['banner']
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
      @date ||= parse_date(File.basename(filename, '.md'))
    end

    def title
      to_uyd_date(date)
    end

    def to_liquid
      super.merge(
        {
          'date' => date,
          'datetime' => date_to_time(date),
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

    attr_reader :options

    def self.generate_all!(options = {})
      context = {}
      builders = descendants.map { |b| b.new options }
      builders.each { |b| context.merge!(b.context) }
      builders.each { |b| b.generate(context) }
      builders.each { |b| b.validate(context) }
    end

    def self.descendants
      ObjectSpace.each_object(Class).select { |klass| klass < self }
    end

    def initialize(options)
      @options = options
    end

    def generate(_ctx); end

    def validate(_ctx); end

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
      logger.info "generating documentation -> site#{docs_permalink}"
      Shell.run "yard #{options} #{path('blog.rb')}"
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
      logger.info "generating coverage report -> site#{report_permalink}"
      Shell.run 'rspec'
      {
        'coverage' => results['metrics'],
        'coverage_permalink' => report_permalink
      }
    end

    def report_permalink
      '/coverage/'
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
      logger.info "caching #{images.count} image(s) -> site/images"
      cache_images
    end

    def cache_images
      FileUtils.copy_entry(src, target)
    end

    def target
      path('site', 'images')
    end

    def src
      path('images')
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
    include Dates
    include Templating

    def target
      path('site', permalink)
    end

    def permalink
      '/feed.xml'
    end

    def generate(ctx)
      logger.info "rendering feed -> site#{permalink}"
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
          <generator uri="https://www.github.com/arecker/blog">
            blog
          </generator>
          <title>{{ config.title }}</title>
          <subtitle>{{ config.description }}</subtitle>
          <link href="{{ config.url }}{{ feed_permalink }}" rel="self"/>
          <updated>#{now.strftime}</updated>
          <author>
            <name>{{ config.author }}</name>
            <email>{{ config.email }}</email>
          </author>
          <id>{{ config.url }}/</id>
          {% for entry in entries limit:30 %}
          #{entry}
          {% endfor %}
        </feed>
      BOOYAKASHA
    end

    def entry
      <<~XMLDADDY
        <entry>
          <title>{{ entry.title }}</title>
          <id>{{ entry.url }}</id>
          <link href="{{ entry.url }}" rel="alternate" type="text/html" title="{{ entry.description }}" />
          <published>{{ entry.datetime }}</published>
          <updated>{{ entry.datetime }}</updated>
          <summary><![CDATA[{{ entry.description }}]]></summary>
        </entry>
      XMLDADDY
    end
  end

  # Graph Builder
  class GraphBuilder < Builder
    def generate(ctx)
      if generate?
        logger.info 'generating graphs -> images/graphs'
        Graphs.generate_graphs(ctx)
      else
        logger.info '(skipping graph generation)'
      end
    end

    def generate?
      options[:no_generate_graphs] != true && Dependencies.graphs?
    end
  end

  # Markup Validator
  class MarkupValidator < Builder
    def validate(ctx)
      @ctx = ctx
      if validate?
        logger.info "validating #{validate_files_count} pages(s) -> site/**/*.html"
        proof!
      else
        logger.info '(skipping HTML validation)'
      end
    end

    def proof!
      logger.debug("ignoring: #{ignore_files}")
      HTMLProofer.check_directory(
        path('site'),
        file_ignore: ignore_files,
        disable_external: true,
        log_level: :error
      ).run
    end

    def validate?
      options[:no_validate_html] != true
    end

    def validate_files_count
      files(path('site')).count - ignore_files.count
    end

    def docs
      files(path('site', @ctx['docs_permalink']))
    end

    def coverage
      files(path('site', @ctx['coverage_permalink']))
    end

    def ignore_files
      @ignore_files ||= coverage + docs
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
        bail!('server dependenices not installed!') unless Dependencies.server?
        build!
        serve!
      end
    end

    def build!
      pave!
      Builder.generate_all!(options)
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

    private

    def preflight!
      bail! unless valid?
      Blog.logger.level = ::Logger::DEBUG if verbose?
    end

    def bail!(message = nil)
      puts message || banner
      exit(-1)
    end

    def make_options(opts)
      opts.banner = banner
      opts.on('-v', '--verbose') { |_t| options[:verbose] = true }
      opts.on('--no-validate-html') { |_o| options[:no_validate_html] = true }
      opts.on('--no-resize-images') { |_o| options[:no_resize_images] = true }
      opts.on('--no-generate-graphs') { |_o| options[:no_generate_graphs] = true }
    end
  end

  def self.run!
    parser = Runner.new(ARGV)
    parser.run!
  end
end

Blog.run! if __FILE__ == $PROGRAM_NAME
