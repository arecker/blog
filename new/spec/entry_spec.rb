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
end
