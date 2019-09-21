# frozen_string_literal: true

require 'git'

module Blog
  # Git
  module Git
    def self.repo_path=(path)
      @git = ::Git.open(path)
    end

    def self.dirty?
      @git.status.changed.any?
    end

    def self.changes
      @git.status.changed
    end
  end
end
