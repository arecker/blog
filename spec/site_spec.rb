# frozen_string_literal: true

require 'spec_helper.rb'

describe JekyllRecker::Site do
  let(:site) { double('site') }

  describe '#entries' do
    it 'should return an ordered list of descending posts' do
      posts = (1..3).map do |n|
        post = double('post')
        expect(post).to receive(:published?).and_return true
        expect(post).to receive(:date).and_return Date.new(2020, 7, n)
        post
      end

      expect(site).to receive_message_chain(:posts, :docs).and_return(posts)
      expect(JekyllRecker::Site.new(site).entries).to eq(posts.reverse)
    end

    it 'should return published posts' do
      posts = []

      published = double('published')
      expect(published).to receive(:published?).and_return true
      posts << published

      unpublished = double('unpublished')
      expect(unpublished).to receive(:published?).and_return false
      posts << unpublished

      posts.each_with_index do |post, i|
        date = Date.new(2020, 7, i + 1)
        allow(post).to receive(:date).and_return date
      end

      expect(site).to receive_message_chain(:posts, :docs).and_return(posts)
      expect(JekyllRecker::Site.new(site).entries).to eq([published])
    end

    describe '#production?' do
      let(:k) { JekyllRecker::Site.new({}) }

      context 'JEKYLL_ENV=production' do
        before(:each) { expect(ENV).to receive(:[]).with('JEKYLL_ENV').and_return('production') }

        it 'should return true' do
          expect(k.production?).to be true
        end
      end

      context 'JEKYLL_ENV=development' do
        before(:each) { expect(ENV).to receive(:[]).with('JEKYLL_ENV').and_return('development') }

        it 'should return false' do
          expect(k.production?).to be false
        end
      end
    end
  end
end
