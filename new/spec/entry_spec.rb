# frozen_string_literal: true

require 'spec_helper'

describe Blog::Entry do
  include Blog::Files

  describe '#target' do
    it 'should replace the markdown extension' do
      entry = Blog::Entry.new('entries/2020-01-01.md', nil)
      expect(entry.target).to eq path('site', '2020-01-01.html')
    end
  end

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

  describe '#banner' do
    it 'should return the image name if it is a png' do
      entry = Blog::Entry.new('2020-01-01.md', nil)
      expect(entry).to receive(:banners).and_return([path('banners/2020-01-01.png')])
      expect(entry.banner).to eq('banners/2020-01-01.png')
    end

    it 'should return nil if there is no matching banner' do
      entry = Blog::Entry.new('2020-01-01.md', nil)
      expect(entry).to receive(:banners).and_return([path('banners/2020-01-02.png')])
      expect(entry.banner).to eq(nil)
    end
  end
end
