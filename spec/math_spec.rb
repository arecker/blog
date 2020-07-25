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
end
