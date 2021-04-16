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

  def test_entry?
    page = Blog::Page.new('_posts/entry.md')
    assert_true(page.entry?)
    page = Blog::Page.new('_pages/page.md')
    assert_false(page.entry?)
  end

  def test_date
    assert_nil(Blog::Page.new('_pages/page.md').date)

    date = Blog::Page.new('_posts/2020-01-01-entry.md').date
    assert_equal(date, Date.new(2020, 1, 1))
  end

  def test_title
    page = Blog::Page.new(
      '_pages/page.md',
      content: <<~FILE
        ---
        title: A Test Title
        ---
      FILE
    )
    assert_equal(page.title, 'A Test Title')
    entry = Blog::Page.new('_posts/2020-01-01-entry.md')
    assert_equal(entry.title, 'Wednesday, January 1 2020')
  end

  def test_description
    page = Blog::Page.new(
      '_pages/page.md',
      content: <<~FILE
        ---
        description: a test description
        ---
      FILE
    )
    assert_equal(page.description, 'a test description')
    entry = Blog::Page.new(
      '_posts/2020-01-01-entry.md',
      content: <<~FILE
        ---
        title: a fart in the wind
        ---
      FILE
    )
    assert_equal(entry.description, 'a fart in the wind')
  end
end
