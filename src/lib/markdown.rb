# frozen_string_literal: true

require 'kramdown'

# Functions for working with (shudder) markdown.
module Markdown
  # Render an markdown string to HTML.
  def self.to_html(content)
    Kramdown::Document.new(content).to_html
  end

  # Strips frontmatter out of a string.
  def self.strip_frontmatter(content)
    pattern = /^-{3}\n.*?\n-{3}\n/m
    content.sub(pattern, '')
  end
end
