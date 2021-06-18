# frozen_string_literal: true

require 'test/unit'

# Unit tests for Files module
class TestFiles < Test::Unit::TestCase
  def test_root
    assert(File.directory?(Files.root), 'Files.root should be a real directory.')
  end

  def test_shorten
    short_path = 'src/blog.rb'
    full_path = Files.join(short_path)
    assert_equal('src/blog.rb', Files.shorten(full_path), 'Files.shorten should return short_path')
  end
end
