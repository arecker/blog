# frozen_string_literal: true

require 'test/unit'

# Unit tests for Shell module
class TestShell < Test::Unit::TestCase
  def test_which?
    result = Blog::Shell.which?('which') == true
    assert(result, 'Shell.which? should return true for `which`.')
  end
end
