# frozen_string_literal: true

# Blog
module Blog
  require_relative 'blog/config'
  require_relative 'blog/entry'
  require_relative 'blog/git'
  require_relative 'blog/journal'
  require_relative 'blog/log'
  require_relative 'blog/s3'
  require_relative 'blog/stats'
  require_relative 'blog/words'

  def self.logger
    Blog::Log.logger
  end

  def self.go_go_gadget_publish!
    logger.info 'starting publisher'
    config = Blog::Config.load_from_file || exit(1)
    logger.level = config.log_level
    logger.debug "set log level to #{config.log_level}"

    logger.info 'validating config'
    exit 1 unless config.validate!

    logger.info "checking status of repo at #{config.blog_repo.pretty_path}"
    repo = Blog::Git.new(config)
    exit 1 unless repo.validate_clean!

    logger.info "loading journal from #{config.journal_path.pretty_path}"
    journal = Blog::Journal.from_file(config.journal_path)

    logger.info "writing #{journal.public_entries.count.pretty} public entries"
    journal.write_public_entries! config.posts_dir

    Blog::Stats.write_stats! journal, config.stats_path

    logger.info 'reviewing changes'
    repo.validate_changed!

    logger.info 'delaying 5 seconds'
    sleep 5

    Blog.logger.info "publishing #{config.site_dir.pretty_path} to s3://#{config.bucket}/"
    Blog::S3.publish config.site_dir, config.bucket, config.aws_creds
  end
end
