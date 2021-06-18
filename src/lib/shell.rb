# frozen_string_literal: true

# Functions for working with the external shell.
module Shell
  # Checks if a command is available (using `which`)
  def self.which?(cmd)
    !`which "#{cmd}"`.chomp.empty?
  end
end
