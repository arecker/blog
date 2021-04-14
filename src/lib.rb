# frozen_string_literal: true

$LOAD_PATH.unshift File.dirname(__FILE__)

module Blog
  autoload :Page, 'lib/page.rb'

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

  def self.join(*subpaths)
    File.join(root_directory, *subpaths)
  end

  def self.pages
    Dir[join('_pages/*')].sort.map { |s| Page.new s }
  end
end
