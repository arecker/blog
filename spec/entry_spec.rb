# frozen_string_literal: true

require 'spec_helper.rb'

describe JekyllRecker::Entry do
  let(:doc) { double('doc') }

  describe '#date' do
    it 'should convert Time to a Date' do
      expect(doc).to receive('date').and_return Time.parse('2020-07-03').localtime

      actual = JekyllRecker::Entry.new(doc).date
      expected = Date.new(2020, 0o7, 0o3)
      expect(actual).to eq(expected)
    end
  end

  describe '#word_count' do
    it 'should count the words in content' do
      expect(doc).to receive(:content).and_return 'This is a test, see?'
      actual = JekyllRecker::Entry.new(doc).word_count
      expect(actual).to eq(5)
    end
  end

  describe '#words' do
    it 'should remove punctuation' do
      expect(doc).to receive(:content).and_return 'alex...!'
      actual = JekyllRecker::Entry.new(doc).words
      expected = ['alex']
      expect(actual).to eq(expected)
    end

    it 'should make all words lowercase' do
      expect(doc).to receive(:content).and_return 'Alex Martin Recker'
      actual = JekyllRecker::Entry.new(doc).words
      expected = %w[alex martin recker]
      expect(actual).to eq(expected)
    end

    it 'should remove newlines and whitespace' do
      content = <<~TEXT
        But soft!
        What light through yonder window breaks?
        It is the east, and Juliet, is the sun!
      TEXT
      expect(doc).to receive(:content).and_return content
      expected = %w[
        but soft what light through
        yonder window breaks it is
        the east and juliet is the sun
      ]
      actual = JekyllRecker::Entry.new(doc).words
      expect(actual).to eq(expected)
    end
  end
end
