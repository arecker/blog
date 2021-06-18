# frozen_string_literal: true

require 'test/unit'

# Unit tests for Markdown module
class TestMarkdown < Test::Unit::TestCase
  def test_to_html
    expected = "\n<p><em>Hello World</em></p>\n"
    actual = Markdown.to_html('_Hello World_')
    assert_equal(expected, actual, 'Markdown.to_html to convert a markdown string to HTML')
  end
end
