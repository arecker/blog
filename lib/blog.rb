# frozen_string_literal: true

# Blog
module Blog
  require 'fileutils'

  require_relative 'blog/config'
  require_relative 'blog/entry'
  require_relative 'blog/git'
  require_relative 'blog/journal'
  require_relative 'blog/log'
  require_relative 'blog/s3'
  require_relative 'blog/slack'
  require_relative 'blog/stats'
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

  def self.go_go_gadget_publish!
    # Blog.logger.info "publishing #{config.site_dir.pretty_path} to s3://#{config.bucket}/"
    # Blog::S3.publish config.site_dir, config.bucket, config.aws_creds

    # config.slacks.each do |info|
    #   url = `#{info.fetch('webhook_cmd')}`.strip
    #   Blog::Slacky.post info.fetch('channel'), url
    # end
  end

  def self.repo
    @repo ||= Blog::Git.new(config)
  end

  def self.config
    @config ||= Blog::Config.load_from_file
  end
end
