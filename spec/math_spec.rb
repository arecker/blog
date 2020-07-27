# frozen_string_literal: true

require_relative 'spec_helper.rb'

describe JekyllRecker::Math do
  let(:k) { Class.new { extend ::JekyllRecker::Math } }

  describe '#average' do
    it 'should average a list of integers' do
      expect(k.average([1, 1, 2, 2, 3, 3])).to eq(2)
    end
  end

  describe '#total' do
    it 'should total a list of integers' do
      expect(k.total([1, 1, 2, 2, 3, 3])).to eq(12)
    end
  end

  describe '#occurences' do
    it 'should count occurances of keys in a list of targets' do
      keys = %w[Kelly Alex Sarah Frank]
      text = 'Kelly and Alex and Sarah are siblings.  Kelly and Sarah are sisters'

      expected = {
        'Kelly' => 2,
        'Alex' => 1,
        'Sarah' => 2
      }

      expect(k.occurences(keys, text.split)).to eq(expected)
    end
  end
end
