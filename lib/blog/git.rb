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
      commit!
    end

    def commit!
      commit = '[auto] Automatic Publish'
      @logger.info "writing commit: #{commit}"
      @client.add
      @client.commit(commit)
      @logger.info 'pushing commit'
      @client.push
    end
  end
end
