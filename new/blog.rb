#!/usr/bin/env ruby
# coding: utf-8
# -*- mode: ruby -*-
# frozen_string_literal: true

require 'fileutils'
require 'liquid'
require 'logger'
require 'open3'
require 'pathname'
require 'shellwords'
require 'yaml'

begin
  require 'liquid/debug'
rescue LoadError # rubocop:disable Lint/SuppressedException
end

CONFIG = {
  github_username: 'arecker'
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

  # Shell
  module Shell
    def shell(cmd)
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
    include Shell

    def self.head
      shell('git rev-parse --short HEAD').chomp
    end
  end

  # Template
  module Template
    include Files
    include Text

    def template(file)
      raw = strip_metadata(File.read(file))
      ::Liquid::Template.parse(raw, error_mode: :strict)
    end

    def render_template(file, context: {}, layout: nil)
      result = template(file).render(context)
      if layout.nil?
        result
      else
        template(path('layouts', layout)).render('content' => result)
      end
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

      def render(_context)
        render_template(filename, context: options)
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
    end
    Liquid::Template.register_tag('include', Include)
  end

  # Page
  class Page
    include Files
    include Logging
    include Template

    attr_reader :file, :site

    def initialize(file, site)
      @file = file
      @site = site
    end

    def to_liquid
      {
        'permalink' => permalink
      }
    end

    def render!
      logger.debug "rendering page #{file} -> #{target}"
      write(target, content)
    end

    def content
      render_template(file, context: context, layout: layout)
    end

    def context
      {
        'page' => self,
        'site' => site
      }
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

    def metadata
      result = YAML.load_file(file)
      if result.is_a? Hash
        result
      else
        {}
      end
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
    end

    def pages
      @pages ||= files(path('pages')).map { |f| Page.new(f, self) }
    end

    def to_liquid
      {
        'config' => CONFIG,
        'gitref' => Git.head
      }
    end
  end

  # Builder
  class Builder
    include Files
    include Logging
    include Shell

    attr_reader :site

    def initialize
      @site = Site.new
    end

    def build!
      site.render!

      logger.info "copying #{path('assets')} -> #{path('site/assets')}"
      FileUtils.copy_entry(path('assets'), path('site/assets'))

      logger.info "generating coverage report -> #{path('site/coverage')}"
      shell 'rspec'
    end
  end

  def self.run!
    logger.info 'starting blog'
    Builder.new.build!
  end
end

Blog.run! if __FILE__ == $PROGRAM_NAME
