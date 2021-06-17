# frozen_string_literal: true

# Functions for working with version control.
module Git
  # Returns the current HEAD
  def self.head
    `git rev-parse HEAD`.chomp
  end

  # Returns the current git HEAD, only the short version.
  def self.short_head
    `git rev-parse --short HEAD`.chomp
  end

  # Returns the commit message summary for the current HEAD.
  def self.head_summary
    `git log -1 --pretty=format:%s #{head}`
  end

  # Returns the number of commits on master.
  def self.commit_count
    `git rev-list --count master`.chomp.to_i
  end

  # Returns all git data for site.
  def self.context
    {
      'git_head' => head,
      'git_head_summary' => head_summary,
      'git_short_head' => short_head,
      'git_commit_count' => commit_count
    }
  end
end
