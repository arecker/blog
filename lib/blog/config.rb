# frozen_string_literal: true

require 'bundler'
require 'yaml'

module Blog
  # Config
  class Config
    attr_reader :data

    def self.load_from_file(config_path = File.expand_path('~/.blog.yml'),
                            journal_path = File.expand_path('~/Documents/journal.org'))
      new(YAML.load_file(config_path) || {}, journal_path)
    end

    def initialize(data, journal_path)
      @data = data
      @journal_path = journal_path
    end

    def journal_path
      File.expand_path(@journal_path)
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
