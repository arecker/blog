#frozen_string_literal: true

require 'commander'

module Blog
  # CLI
  class CLI
    include Commander::Methods

    def run
      program :name, 'blog'
      program :version, 'v0.0.0'
      program :description, 'script to generate and publish my blog'

      default_command :all

      journal_path = File.expand_path '~/Documents/journal.org'
      config_path = File.expand_path '~/.blog.yml'

      global_option '--journal FILE', String, 'path to journal.org' do |file|
        journal_path = file
      end

      global_option '--config FILE', String, 'path to blog.yml' do |file|
        config_path = file
      end

      logger = Blog::Log.logger

      config = Blog::Config.load_from_file(config_path)
      logger.level = config.log_level
      logger.debug "set log level to #{config.log_level}"

      command :build do |c|
        c.syntax = 'build'
        c.description = 'build jekyll site'
        c.action do |_args, _options|
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
      end

      command :commit do |c|
        c.syntax 'commit'
        c.description 'commit and push new post'
        c.action do |_args, _options|
          git = Blog::Git.new(config.blog_repo)
          logger.info "getting untracked post from #{config.blog_repo.pretty_path}"
          added = git.one_and_only_untracked_post
          exit 1 if added.nil?
          logger.info "committing #{added}"
          git.commit
        end
      end

      command :all do |c|
        c.syntax 'all'
        c.description 'build, commit, slack, and tweet'
        c.action do |_args, _options|

        end
      end

      run!
    end
  end
end
