#!/usr/bin/env ruby
# -*- mode: ruby -*-
# frozen_string_literal: true

require 'fileutils'
require 'liquid'
require 'logger'
require 'pathname'
require 'yaml'

begin
  require 'liquid/debug'
rescue LoadError # rubocop:disable Lint/SuppressedException
end

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
    def self.included(base)
      base.extend(self)
    end

    def files(path)
      Dir["#{path}/**/*"].select { |o| File.file?(o) }
    end

    def root_dir
      File.dirname(__FILE__)
    end

    def site_dir
      root_join('site')
    end

    def site_join(path)
      File.join(site_dir, path)
    end

    def relpath(root, path)
      Pathname.new(path).relative_path_from(Pathname.new(root)).to_s
    end

    def root_join(path)
      File.join(root_dir, path)
    end

    def pages_dir
      root_join('pages')
    end

    def layouts_dir
      root_join('layouts')
    end

    def layouts_join(path)
      File.join(layouts_dir, path)
    end

    def snippets_dir
      root_join('snippets')
    end

    def snippets_join(path)
      File.join(snippets_dir, path)
    end

    def mkdir_write(path, content)
      FileUtils.mkdir_p(File.dirname(path))
      File.open(path, 'w') { |f| f.write content }
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
        template(layouts_join(layout)).render('content' => result)
      end
    end
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
        'webpath' => webpath
      }
    end

    def render!
      logger.debug "rendering page #{file} -> #{target}"
      mkdir_write(target, content)
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
      if webpath.end_with? '/'
        site_join(File.join(webpath, 'index.html'))
      else
        site_join(webpath)
      end
    end

    def webpath
      default = '/' + relpath(pages_dir, file)
      metadata.fetch('permalink', default)
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
      logger.info "rebuilding #{site_dir}"
      FileUtils.rm_rf site_dir
      FileUtils.mkdir_p site_dir
    end

    def pages!
      logger.info "rendering #{pages.count} page(s)"
      pages.each(&:render!)
    end

    def pages
      @pages ||= files(pages_dir).map { |f| Page.new(f, self) }
    end

    def to_liquid
      {
        'title' => 'Dear Journal',
        'description' => 'Daily, public journal by Alex Recker'
      }
    end
  end

  # Runner
  class Runner
    include Logging

    def run!
      logger.info 'starting blog'
      site = Site.new
      site.render!
    end
  end

  def self.run!
    Runner.new.run!
  end
end

Blog.run! if __FILE__ == $PROGRAM_NAME
