# frozen_string_literal: true

require 'test/unit'

# Unit tests for Files module
class TestFiles < Test::Unit::TestCase
  def test_root
    assert(File.directory?(Files.root), 'Files.root should be a real directory.')
  end
end
