# frozen_string_literal: true

require 'spec_helper'

describe Blog::Entry do
  before(:each) do
    @text = <<~TEXT
      *** 2019-08-06 Tuesday :private:

      Dear Journal

      *** 2019-08-07 Wednesday :salad:reunions:time:

      Dear Journal

      *** 2019-08-08 Thursday :headaches:computers:naps:

      Dear Journal

      *** 2019-08-09 Friday :plex:cables:strongbad:

      Dear Journal
    TEXT
  end

  it 'should sort the blog entries by date' do
    parser = Orgmode::Parser.new(@text)
    journal = Blog::Journal.new(parser)
    expect(journal.entries.first.tags).to eq(%w[plex cables strongbad])
  end

  it 'should filter out private entries' do
    parser = Orgmode::Parser.new(@text)
    journal = Blog::Journal.new(parser)
    matching = journal.entries.select { |e| e.tags.include? 'private' }
    expect(matching.any?).to be false
  end
end
