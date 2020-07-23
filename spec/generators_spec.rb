# frozen_string_literal: true

require_relative 'spec_helper.rb'

class Dummy
  include JekyllRecker::Generators::Base
  attr_writer :site
end

describe JekyllRecker::Generators::Base do
  let(:k) { Dummy.new }

  describe '#production?' do
    context 'JEKYLL_ENV=production' do
      before(:each) { allow(ENV).to receive(:[]).with('JEKYLL_ENV').and_return('production') }

      it 'should return true' do
        expect(k.production?).to be true
      end
    end

    context 'JEKYLL_ENV=development' do
      before(:each) { allow(ENV).to receive(:[]).with('JEKYLL_ENV').and_return('development') }

      it 'should return false' do
        expect(k.production?).to be false
      end
    end
  end

  describe '#entries' do
    let(:site) { double('site') }

    it 'should only return published entries' do
      published = double('post')
      expect(published).to receive(:published?).and_return(true)
      expect(published).to receive(:date).and_return(Date.new(2020, 1, 1))

      unpublished = double('post')
      expect(unpublished).to receive(:published?).and_return(false)

      allow(site).to receive_message_chain(:posts, :docs).and_return([published, unpublished])
      dummy = Dummy.new
      dummy.site = site
      expect(dummy.entries).to eq([published])
    end

    it 'should order entries by descending date' do
      posts = [1, 10, 5].map do |i|
        post = double("post-#{i}")
        expect(post).to receive(:published?).and_return(true)
        expect(post).to receive(:date).and_return(Date.new(2020, 1, i))
        post
      end

      allow(site).to receive_message_chain(:posts, :docs).and_return(posts)
      dummy = Dummy.new
      dummy.site = site

      expected = [posts[1], posts[2], posts[0]]
      expect(dummy.entries).to eq(expected)
    end
  end

  describe '#dates' do
    let(:site) { double('site') }

    it 'should return the descending entry dates' do
      dates = [
        Date.new(2020, 2, 1),
        Date.new(2020, 1, 20),
        Date.new(2020, 1, 2),
        Date.new(2020, 1, 4),
        Date.new(2020, 1, 10)
      ]

      posts = dates.each.map do |d|
        post = double('post')
        expect(post).to receive(:published?).and_return true
        allow(post).to receive(:date).and_return(d)
        post
      end

      allow(site).to receive_message_chain(:posts, :docs).and_return(posts)
      dummy = Dummy.new
      dummy.site = site

      expect(dummy.dates).to eq(dates.sort.reverse)
    end
  end

  describe '#bodies' do
    let(:k) { Dummy.new }

    it 'should return the content of each post' do
      post = double('post')
      expect(post).to receive(:content).and_return('This is test content')
      expect(k).to receive(:entries).and_return([post])

      expected = ['This is test content']
      expect(k.bodies).to eq(expected)
    end
  end

  describe '#words' do
    let(:k) { Dummy.new }

    it 'should return a flat list of words' do
      posts = [
        'In the beginning was the Word, and the Word was with God, and the Word was God.',
        'The same was in the beginning with God.',
        'All things were made by him; and without him was not any thing made that was made.'
      ]
      expect(k).to receive(:bodies).and_return(posts)

      expected = %w[In the beginning was the Word and the Word was with God and the Word was God. The same was in the beginning with God. All things were made by him; and without him was not any thing made that was made.]

      expect(k.words).to eq(expected)
    end
  end

  describe '#word_counts' do
    let(:k) { Dummy.new }

    it 'should return a list of word counts' do
      posts = ['Hello World', 'Another Post', 'What is the point?']
      expect(k).to receive(:bodies).and_return(posts)
      expect(k.word_counts).to eq([2, 2, 4])
    end
  end
end
