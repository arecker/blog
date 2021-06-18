# frozen_string_literal: true

require 'rdoc'

# Functions for working with (shudder) markdown.
module Markdown
  # Render an markdown string to HTML.
  def self.to_html(content)
    formatter = RDoc::Markup::ToHtml.new(RDoc::Options.new, nil)
    RDoc::Markdown.parse(content).accept(formatter)
  end
end
