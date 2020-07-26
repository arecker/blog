# frozen_string_literal: true

module JekyllRecker
  # Tags
  module Tags
    # Render the current plugin version
    class Version < Liquid::Tag
      def render(_ctx)
        "v#{JekyllRecker::VERSION}"
      end
    end

    # Get the number of commits
    class CommitCount < Liquid::Tag
      def render(_ctx)
        count
      end

      def count
        @count ||= Shell.run 'git rev-list --count master'
      end
    end
  end
end

Liquid::Template.register_tag('version', JekyllRecker::Tags::Version)
Liquid::Template.register_tag('commit_count', JekyllRecker::Tags::CommitCount)
