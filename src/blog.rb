# frozen_string_literal: true

module Blog
  def self.root_directory
    relative = File.join(File.dirname(__FILE__), '..')
    File.expand_path(relative)
  end

  def self.directories
    matches = Dir.entries(root_directory).select do |e|
      File.directory?(e) && !['.', '_'].include?(e[0])
    end
    matches.sort
  end
end
