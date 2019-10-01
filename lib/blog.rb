# frozen_string_literal: true

# Blog
module Blog
  require 'fileutils'

  require_relative 'blog/config'
  require_relative 'blog/entry'
  require_relative 'blog/git'
  require_relative 'blog/jekyll'
  require_relative 'blog/journal'
  require_relative 'blog/log'
  require_relative 'blog/s3'
  require_relative 'blog/slack'
  require_relative 'blog/stats'
  require_relative 'blog/twitter'
  require_relative 'blog/words'

  def self.logger
    Blog::Log.logger
  end

  def self.build!
    logger.level = config.log_level
    logger.debug "set log level to #{config.log_level}"
    logger.info "deleting #{config.site_dir.pretty_path}"
    FileUtils.rm_rf(config.site_dir)
    logger.info "parsing #{config.journal_path.pretty_path}"
    journal = Blog::Journal.from_file(config.journal_path)
    logger.info "writing #{journal.public_entries.count.pretty} public entries"
    journal.write_public_entries! config.posts_dir
    logger.info "building jekyll"
    Blog::Jekyll.build(config)
    Blog::Stats.write_stats! journal, config.stats_path
  end

  def self.commit!
    git = Blog::Git.new(config.blog_repo)
    logger.info "getting untracked post from #{config.blog_repo.pretty_path}"
    added = git.one_and_only_untracked_post
    exit 1 if added.nil?
    logger.info "committing #{added}"
    git.commit
  end

  def self.publish!
    logger.info "publishing #{config.site_dir.pretty_path} to s3://#{config.bucket}/"
    Blog::S3.publish config.site_dir, config.bucket, config.aws_creds
  end

  def self.slack!
    logger.info "parsing #{config.journal_path.pretty_path}"
    journal = Blog::Journal.from_file(config.journal_path)
    latest = journal.public_entries.first
    logger.info "fetched latest entry: #{latest.excerpt}"
    config.slacks.each do |info|
      Blog::Slacky.post(latest, `#{info['webhook_cmd']}`, info)
    end
  end

  def self.tweet!
    logger.info "parsing #{config.journal_path.pretty_path}"
    journal = Blog::Journal.from_file(config.journal_path)
    latest = journal.public_entries.first
    logger.info "fetched latest entry: #{latest.excerpt}"
    Blog::Twitter.post(latest, config.twitter_creds)
  end

  def self.everything!
    build!
    commit!
    publish!
    slack!
    tweet!
  end

  def self.config
    @config ||= Blog::Config.load_from_file
  end
end
