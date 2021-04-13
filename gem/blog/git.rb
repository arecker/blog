# frozen_string_literal: true

module Blog
  # Git
  module Git
    include Blog::Shell

    def git_short_head
      shell('git rev-parse --short HEAD').chomp
    end

    def git_head
      shell('git rev-parse HEAD').chomp
    end

    def git_head_summary
      shell('git log -1 --pretty=format:"%s" HEAD').chomp
    end

    def git_commit_count
      shell('git rev-list --count master').chomp.to_i
    end
  end
end
