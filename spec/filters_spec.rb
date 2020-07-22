# frozen_string_literal: true

require 'spec_helper.rb'

describe JekyllRecker::Filters do
  let(:k) { Class.new { extend ::JekyllRecker::Filters } }

  describe '#uyd_date' do
    it 'should convert a date into standard UYD format' do
      actual = k.uyd_date(Date.new(2020, 7, 21))
      expected = 'Tuesday, July 21 2020'
      expect(actual).to eq(expected)
    end
  end

  describe '#pretty' do
    it 'should add commas to a number' do
      actual = k.pretty(1_000_001)
      expected = '1,000,001'
      expect(actual).to eq(expected)
    end
  end
end
