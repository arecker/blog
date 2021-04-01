# frozen_string_literal: true

module Blog
  # For functions that support working with the local Blog filesystem
  module Files
    # The Blog file tree, represented by a flattened object.
    class Tree
      # The root Blog directory (usually something like ~/src/blog)
      def root
        relative = File.join(File.dirname(__FILE__), '../../')
        File.expand_path relative
      end

      # List all blog entries (files, directories, and links)
      def entries
        Dir.entries root
      end

      # List all Blog directories
      def directories
        dirs = entries.select { |e| File.directory? e }
        dirs.reject { |d| d.start_with?('.') || d.start_with?('_') }.sort
      end
    end

    def self.tree
      @tree ||= Tree.new
    end

    def self.directories
      tree.directories
    end
  end
end
