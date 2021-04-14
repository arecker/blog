# frozen_string_literal: true

class TestBlog < Test::Unit::TestCase
  def test_directories
    assert_equal Blog.directories, Blog.directories.sort
    Blog.directories.each do |d|
      assert_true(File.directory?(d))
    end
  end

  def test_root_directory
    assert_true(File.directory?(Blog.root_directory))
  end
end
