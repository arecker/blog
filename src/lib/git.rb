# frozen_string_literal: true

# Functions for working with version control.
module Git
  def self.head
    `git rev-parse HEAD`.chomp
  end

  def self.short_head
    `git rev-parse --short HEAD`.chomp
  end

  def self.head_summary
    `git log -1 --pretty=format:%s #{head}`
  end
end
