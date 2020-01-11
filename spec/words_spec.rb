# frozen_string_literal: true

require 'spec_helper'

describe Blog::Words do
  it 'should make an and list from an array' do
    expect(%w[a].to_and_list).to eq('a')
    expect(%w[a b].to_and_list).to eq('a and b')
    expect(%w[a b c].to_and_list).to eq('a, b, and c')
    expect(%w[a b c d].to_and_list).to eq('a, b, c, and d')
  end

  it 'should make a pretty number from an integer' do
    expect(1_200.pretty).to eq('1,200')
    expect(1_000_000.pretty).to eq('1,000,000')
  end

  it 'should turn a string into a list of words' do
    expect('this is a test'.words).to eq(%w[this is a test])
    text = <<~TEXT
  THIS
  IS  
  A  
  TEST   
  WITH     
  NEWLINES  
    TEXT
    expect(text.words).to eq(%w[THIS IS A TEST WITH NEWLINES])
  end

  it 'should get the word count from a string' do
    text = <<~TEXT
      Hey Journal,

      Today while cleaning up my sister's old laptop I discovered the ruins
      of an ambition project I started to write one thousand words a day.
      The funny thing is I remember telling everyone that I wanted to do
      this, but I didn't remember I only made it five days.  Well today I
      set out on the same venture.  Accept hopefully I'm older, wiser, and
      just a little more patient.  Plus I have a better system now.  I have
      to admit, the writing got a little whiney, which is perhaps why I
      tweaked the rules to just let me write as much as I want.  Short and
      sweet.

      Tonight I tried making gnocchi.  Damn Gordon Ramsey makes everything
      look so easy, I think it might be witchcraft.  Eh, I'm going to rally,
      I'm bound for a gnocchi redemption this week.  I'll let you know how
      it goes.
    TEXT

    expect(text.word_count).to eq(148)
  end

  it 'should prettify a path' do
    actual = '/Users/butthead/tmp'.pretty_path('/Users/butthead')
    expected = '~/tmp'
    expect(actual).to eq expected
  end
end
