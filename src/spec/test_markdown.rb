# frozen_string_literal: true

require 'test/unit'

# Unit tests for Markdown module
class TestMarkdown < Test::Unit::TestCase
  def test_to_html
    expected = "<p><em>Hello World</em></p>\n"
    actual = Blog::Markdown.to_html('_Hello World_')
    assert_equal(expected, actual)
  end

  def test_strip_frontmatter
    content = <<~TEXT
      ---
      title: some title
      description: some description
      ---
      Document begins here!
    TEXT

    actual = Blog::Markdown.strip_frontmatter(content.chomp)
    expected = 'Document begins here!'
    assert_equal(expected, actual)
  end
end
