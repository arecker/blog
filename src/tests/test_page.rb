# frozen_string_literal: true

require_relative '../lib'

class TestPage < Test::Unit::TestCase
  def test_filename
    page = Blog::Page.new('something.md')
    assert_equal(page.filename, 'something.html')
    page = Blog::Page.new('something.html')
    assert_equal(page.filename, 'something.html')
    page = Blog::Page.new('entry/thing/something.md')
    assert_equal(page.filename, 'something.html')
  end

  def test_pathname
    page = Blog::Page.new('something.md')
    assert_equal(page.pathname, '/something.html')
    page = Blog::Page.new('something.html')
    assert_equal(page.pathname, '/something.html')
    page = Blog::Page.new('entry/thing/something.md')
    assert_equal(page.pathname, '/something.html')
  end

  def test_frontmatter
    content = <<~CONTENT.strip
      ---
      title: something
      nav: 1
      ---

      This is a test entry!
    CONTENT
    page = Blog::Page.new('test.md', content: content)
    assert_equal(
      page.frontmatter,
      {
        'title' => 'something',
        'nav' => 1
      }
    )
  end

  def test_nav?
    content = <<~CONTENT.strip
      ---
      title: something
      nav: 1
      ---

      This is a test entry!
    CONTENT
    page = Blog::Page.new('test.md', content: content)
    assert_true(page.nav?)
  end
end
