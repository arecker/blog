# frozen_string_literal: true

require 'spec_helper.rb'

describe JekyllRecker::Entry do
  let(:doc) { double('doc') }

  describe '#date' do
    it 'should convert Time to a Date' do
      expect(doc).to receive('date').and_return Time.parse('2020-07-03').localtime

      actual = JekyllRecker::Entry.new(doc).date
      expected = Date.new(2020, 07, 03)
      expect(actual).to eq(expected)
    end
  end
end
