# frozen_string_literal: true

require 'git'

module Blog
  # Git
  class Git
    attr_reader :client

    def initialize(path)
      @client = ::Git.open(path)
      @logger = Blog::Log.logger
    end

    def run!
      validate!
      commit!
    end

    def validate!
      @logger.info "validating unstaged changes to #{config.blog_repo.pretty_path}"
      if changed & expected == expected
        @logger.info "validation passed, staging: #{changed}"
      else
        @logger.error "validation failed, unexpected changed: #{changed}"
        exit 1
      end
    end

    def commit!
      commit = '[auto] Automatic Publish}'
      @logger.info "writing commit: #{commit}"
      @client.add
      @client.commit(commit)
      @logger.info 'pushing commit'
      @client.push
    end

    private

    def expected
      ['journal.org', '_data/stats.json']
    end

    def changed
      @client.status.changed.collect(&:first)
    end
  end
end
