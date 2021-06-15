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
end
