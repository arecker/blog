# frozen_string_literal: true

# rubocop:disable Metrics/BlockLength
describe Blog::Site do
  let(:site) { double('site') }

  describe '#entries' do
    it 'should return an ordered list of descending posts' do
      dates = (1..3).map { |n| Date.new(2020, 7, n) }

      posts = dates.map do |date|
        post = double('post')
        allow(post).to receive(:published?).and_return true
        allow(post).to receive(:date).and_return date
        post
      end

      expect(site).to receive_message_chain(:posts, :docs).and_return(posts)

      actual = Blog::Site.new(site).entries.collect(&:date)
      expect(actual).to eq(dates.reverse)
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

      actual = Blog::Site.new(site).entries
      expect(actual.count).to eq(1)
      expect(actual.first.date).to eq(Date.new(2020, 7, 1))
    end

    describe '#data' do
      it 'should pass through to @site.data' do
        site = double('site')
        data = {}
        expect(site).to receive(:data).and_return(data)
        Blog::Site.new(site).data['hello'] = 'world'
        expect(data).to eq({ 'hello' => 'world' })
      end
    end

    describe '#word_counts' do
      it 'should aggregate entry word counts' do
        entries = []

        3.times do
          entry = double('entry')
          expect(entry).to receive(:word_count).and_return 100
          entries << entry
        end

        site = Blog::Site.new({})
        expect(site).to receive(:entries).and_return entries

        expect(site.word_counts).to eq([100, 100, 100])
      end
    end

    describe '#dates' do
      it 'should aggregate entry dates' do
        dates = (1..3).map { |n| ::Date.new(2020, 1, n) }
        entries = dates.map do |date|
          entry = double('entry')
          expect(entry).to receive(:date).and_return(date)
          entry
        end
        site = Blog::Site.new(site)
        expect(site).to receive(:entries).and_return entries.reverse
        expect(site.dates).to eq(dates.reverse)
      end
    end

    describe '#recker_config' do
      it 'should default to empty' do
        expect(site).to receive(:config).and_return({})
        expect(Blog::Site.new(site).recker_config).to eq({})
      end
    end

    describe '#production?' do
      let(:k) { Blog::Site.new({}) }

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
# rubocop:enable Metrics/BlockLength
