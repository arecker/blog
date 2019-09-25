# frozen_string_literal: true

require 'git'

module Blog
  # Git
  class Git
    def initialize(config)
      @repo_path = config.blog_repo
      @enabled = config.use_git?
      @git = ::Git.open(@repo_path)
      @logger = Blog.logger
    end

    def enabled?
      @enabled
    end

    def validate_clean!
      if enabled?
        @logger.error 'there are uncommited changes in the repo!' unless clean?
        clean?
      else
        @logger.info '"use_git" set to false, skipping repo validation'
        true
      end
    end

    def validate_changed!
      if enabled?
        @logger.error 'no changes, nothing to do!' if clean?
        !clean?
      else
        @logger.info '"use_git" set to false, skipping repo validation'
        true
      end
    end

    def clean?
      @git.status.changed.any?
    end

    def changes
      @git.status.changed.to_a
    end
  end
end
