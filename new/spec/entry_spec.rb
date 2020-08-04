# frozen_string_literal: true

require 'spec_helper'

describe Blog::Entry do
  include Blog::Files

  describe '#title' do
    it 'should return the formatted date' do
      entry = Blog::Entry.new('2020-01-01.md', nil)
      expect(entry.title).to eq('Wednesday, January 1 2020')
    end
  end

  describe '#description' do
    it 'should return the page title' do
      entry = Blog::Entry.new('2020-01-01.md', nil)
      expect(entry).to receive(:metadata).and_return({ 'title' => 'eggs, farts, and drama mamas' })
      expect(entry.description).to eq('eggs, farts, and drama mamas')
    end
  end
end
