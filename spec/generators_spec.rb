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
end
