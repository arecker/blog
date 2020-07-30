# frozen_string_literal: true

require 'spec_helper'

describe Blog::Files do
  let(:k) { Class.new { extend ::Blog::Text } }

  describe '#strip_metadata' do
    it 'should remove metadata from text' do
      text = <<~FILE
        ---
        name: some page
        ---
        HELLO THERE!
      FILE
      expected = <<~FILE
        HELLO THERE!
      FILE
      actual = k.strip_metadata(text)
      expect(actual).to eq(expected)
    end

    it 'should do nothing to text without meatadata' do
      text = <<~FILE
        HELLO THERE!
      FILE
      expected = <<~FILE
        HELLO THERE!
      FILE
      actual = k.strip_metadata(text)
      expect(actual).to eq(expected)
    end

    it 'should still work for an empty string' do
      expect(k.strip_metadata('')).to eq('')
    end
  end
end
