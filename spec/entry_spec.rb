# frozen_string_literal: true

require 'spec_helper'

describe Blog::Entry do
  it 'should report if public based on :private: tag' do
    parser = Orgmode::Parser.new('*** 2019-04-14 Sunday :private:')
    entry = Blog::Entry.new(parser.headlines.first)
    expect(entry.public?).to be false

    parser = Orgmode::Parser.new('*** 2019-04-14 Sunday :hotdogs:')
    entry = Blog::Entry.new(parser.headlines.first)
    expect(entry.public?).to be true
  end

  it 'should parse the date from the headline' do
    parser = Orgmode::Parser.new('*** 2019-04-14 Sunday :hotdogs:')
    entry = Blog::Entry.new(parser.headlines.first)
    expect(entry.date.to_s).to eq(Date.new(2019, 4, 14).to_s)
  end

  it 'should make a date slug from the headline' do
    parser = Orgmode::Parser.new('*** 2030-01-02 Sunday :hotdogs:hamburgers:')
    entry = Blog::Entry.new(parser.headlines.first)
    expect(entry.date_slug).to eq('2030-01-02')
  end

  it 'should make filename form the date slug' do
    parser = Orgmode::Parser.new('*** 2030-01-02 Sunday :hotdogs:hamburgers:')
    entry = Blog::Entry.new(parser.headlines.first)
    expect(entry.filename).to eq('2030-01-02-2030-01-02.html.html')
  end

  it 'extract the body text from the entry' do
    text = <<~TEXT
      *** 2019-09-13 Friday :thunderstorms:bulgogi:pto:

      Dear Journal,

      Good morning everyone!  Happy Friday to you, reader.
    TEXT
    parser = Orgmode::Parser.new(text)
    entry = Blog::Entry.new(parser.headlines.first)
    expected = <<~TEXT
      Dear Journal,

      Good morning everyone!  Happy Friday to you, reader.
    TEXT
    expect(entry.body_text).to eq(expected.strip)
  end
end
