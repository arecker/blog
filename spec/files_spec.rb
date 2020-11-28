# frozen_string_literal: true

describe Blog::Files do
  let(:k) { Class.new { extend ::Blog::Files } }

  describe '#root' do
    it 'should return a real path' do
      expect(File.directory?(k.root)).to be true
    end
  end

  describe '#join' do
    it 'should take one argument' do
      actual = k.join('images')
      expect(File.basename(actual)).to eq('images')
    end

    it 'should take multiple arguments' do
      actual = k.join('a', 'b')
      expect(actual.split('/').last(2)).to eq(%w[a b])
    end
  end
end
