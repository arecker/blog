# frozen_string_literal: true

require 'git'

module Blog
  # Git
  class Git
    def initialize(path)
      @client = ::Git.open(path)
      @logger = Blog::Log.logger
    end

    def untracked_files
      @client.status.untracked.keys
    end

    def untracked_posts
      untracked_files.select { |f| f.start_with? '_posts/' }
    end

    def one_and_only_untracked_post
      posts = untracked_posts
      unless posts.count == 1
        @logger.error("#{posts.count} number of untracked posts")
        nil
      end
      posts.first
    end

    def commit
      untracked = one_and_only_untracked_post
      @client.add
      @client.commit("[auto] #{untracked}")
      @client.push
    end
  end
end
