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
  end
end

Liquid::Template.register_tag('version', JekyllRecker::Tags::Version)
