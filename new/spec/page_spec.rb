# frozen_string_literal: true

require 'spec_helper'

describe Blog::Page do
  include Blog::Files

  describe '#permalink' do
    it 'should return a permalink specified in the metadata' do
      page = Blog::Page.new(path('pages/test.html'), nil)
      expect(page).to receive(:metadata).and_return({ 'permalink' => '/test/thing/' })
      expect(page.permalink).to eq('/test/thing/')
    end

    it 'should correctly construct a permalink to an html file' do
      page = Blog::Page.new(path('pages/test.html'), nil)
      allow(page).to receive(:metadata).and_return({})
      expect(page.permalink).to eq('/test.html')
    end

    it 'should correctly construct a permalink to a markdown file' do
      page = Blog::Page.new(path('pages/test.md'), nil)
      allow(page).to receive(:metadata).and_return({})
      expect(page.permalink).to eq('/test.html')
    end
  end
end
