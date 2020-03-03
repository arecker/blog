# frozen_string_literal: true

require 'commander'
require 'fileutils'

module Blog
  # CLI
  class CLI
    include Commander::Methods

    def logger
      Blog::Log.logger
    end

    def config_path
      @config_path ||= File.expand_path '~/.blog.yml'
    end

    def config
      Blog::Config.load_from_file(config_path)
    end

    def journal
      @journal ||= Blog::Journal.from_file(config.journal_path)
    end

    def latest
      @latest ||= journal.public_entries.first
    end

    def build
      logger.info "deleting #{config.site_dir.pretty_path}"
      FileUtils.rm_rf(config.site_dir)
      logger.info "parsing #{config.journal_path.pretty_path}"
      journal = Blog::Journal.from_file(config.journal_path)
      logger.info "writing #{journal.public_entries.count.pretty} public entries"
      journal.write_public_entries! config.posts_dir
      Blog::Stats.write_stats! journal, config.stats_path
      logger.info "building jekyll"
      Blog::Jekyll.build(config)
    end

    def commit
      git = Blog::Git.new(config.blog_repo)
      git.run!
    end

    def slack
      logger.info "fetched latest entry: #{latest.excerpt}"
      config.slacks.each do |info|
        Blog::Slacky.post(latest, `#{info['webhook_cmd']}`, info)
      end
    end

    def tweet
      logger.info "fetched latest entry: #{latest.excerpt}"
      Blog::Twitter.post(latest, config.twitter_creds)
    end

    def run
      program :name, 'blog'
      program :version, 'v0.0.0'
      program :description, 'script to generate and publish my blog'

      default_command :all

      global_option '--config FILE', String, 'path to blog.yml' do |file|
        @config_path = file
      end

      command :build do |c|
        c.syntax = 'build'
        c.description = 'build jekyll site'
        c.action do |_args, _options|
          build
        end
      end

      command :commit do |c|
        c.syntax = 'commit'
        c.description = 'commit and push new post'
        c.action do |_args, _options|
          commit
        end
      end

      command :slack do |c|
        c.syntax = 'slack'
        c.description = 'send slack notifications'
        c.action do |_args, _options|
          slack
        end
      end

      command :tweet do |c|
        c.syntax = 'tweet'
        c.description = 'send tweet notifications'
        c.action do |_args, _options|
          tweet
        end
      end

      command :all do |c|
        c.syntax = 'all'
        c.description = 'build, commit, slack, and tweet'
        c.action do |_args, _options|
          build
          commit
          slack
          tweet
        end
      end

      run!
    end
  end
end
