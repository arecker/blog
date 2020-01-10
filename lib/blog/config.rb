# frozen_string_literal: true

require 'bundler'
require 'yaml'

module Blog
  # Config
  class Config
    attr_reader :data

    def self.load_from_file(config_path = File.expand_path('~/.blog.yml'))
      if File.file? config_path
        Blog.logger.info "loading config from #{config_path.pretty_path}"
        config = new(YAML.load_file(config_path) || {})
        config.validate!
        config
      else
        Blog.logger.error "#{config_path.pretty_path} not found!"
        nil
      end
    end

    def required_keys
      [
        'journal_path'
      ]
    end

    def initialize(data)
      @data = data
    end

    def validate!
      missing = missing_fields

      if missing.any?
        Blog.logger.error "missing configuration: #{missing_fields.to_and_list}"
        false
      else
        Blog.logger.info 'configuration is valid'
        true
      end
    end

    def journal_path
      File.expand_path(@data.fetch('journal_path'))
    end

    def posts_dir
      File.join blog_repo, '_posts'
    end

    def site_dir
      File.join(File.expand_path(blog_repo), '_site')
    end

    def blog_repo
      Bundler.root.to_s
    end

    def stats_path
      File.join blog_repo, '_data/stats.json'
    end

    def log_level
      @data.fetch('log_level', 'INFO').upcase
    end

    def twitter_creds
      twitter = @data.fetch('twitter')
      creds = {}
      [
        'access_token_secret',
        'access_token',
        'consumer_api_key',
        'consumer_api_secret'
      ].each do |key|
        creds[key] = `#{twitter.fetch(key + '_cmd')}`.strip
      end
      creds
    end

    def slacks
      @data.fetch('slacks', [])
    end

    private

    def missing_fields
      required_keys.reject { |k| @data.key? k }
    end
  end
end
