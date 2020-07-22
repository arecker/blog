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

  describe '#slice_by_consecutive_dates' do
    it 'should slice a list of ascending dates' do
      dates = [
        Date.new(2001, 2, 3),
        Date.new(2001, 2, 4),
        Date.new(2001, 2, 6),
        Date.new(2001, 2, 7),
        Date.new(2001, 2, 8)
      ]

      expected = [
        [
          Date.new(2001, 2, 3),
          Date.new(2001, 2, 4)
        ],
        [
          Date.new(2001, 2, 6),
          Date.new(2001, 2, 7),
          Date.new(2001, 2, 8)
        ]
      ]

      expect(k.slice_by_consecutive_days(dates)).to eq(expected)
    end

    it 'should slice a list of descending dates' do
      dates = [
        Date.new(2001, 2, 8),
        Date.new(2001, 2, 7),
        Date.new(2001, 2, 6),
        Date.new(2001, 2, 4),
        Date.new(2001, 2, 3)
      ]

      expected = [
        [
          Date.new(2001, 2, 8),
          Date.new(2001, 2, 7),
          Date.new(2001, 2, 6)
        ],
        [
          Date.new(2001, 2, 4),
          Date.new(2001, 2, 3)
        ]
      ]

      expect(k.slice_by_consecutive_days(dates)).to eq(expected)
    end
  end

  describe '#calculate_streaks' do
    it 'should calculate streaks from ascending dates' do
      dates = [
        Date.new(2001, 2, 3),
        Date.new(2001, 2, 4),
        Date.new(2001, 2, 6),
        Date.new(2001, 2, 7),
        Date.new(2001, 2, 8)
      ]

      expected = [
        {
          'days' => 1,
          'start' => Date.new(2001, 2, 3),
          'end' => Date.new(2001, 2, 4)
        },
        {
          'days' => 2,
          'start' => Date.new(2001, 2, 6),
          'end' => Date.new(2001, 2, 8)
        }
      ]

      expect(k.calculate_streaks(dates)).to eq(expected)
    end

    it 'should calculate streaks from descending dates' do
      dates = [
        Date.new(2001, 2, 8),
        Date.new(2001, 2, 7),
        Date.new(2001, 2, 6),
        Date.new(2001, 2, 4),
        Date.new(2001, 2, 3)
      ]

      expected = [
        {
          'days' => 2,
          'start' => Date.new(2001, 2, 6),
          'end' => Date.new(2001, 2, 8)
        },
        {
          'days' => 1,
          'start' => Date.new(2001, 2, 3),
          'end' => Date.new(2001, 2, 4)
        }
      ]

      expect(k.calculate_streaks(dates)).to eq(expected)
    end
  end
end
