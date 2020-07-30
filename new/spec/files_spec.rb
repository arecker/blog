# frozen_string_literal: true

require 'spec_helper'

describe Blog::Files do
  let(:k) { Class.new { extend ::Blog::Files } }

  describe '#relpath' do
    it 'should calculate a relative path from an absolulte path' do
      expected = 'old/index.html'
      actual = k.relpath('/code/repo/', '/code/repo/old/index.html')
      expect(actual).to eq(expected)
    end
  end
end
