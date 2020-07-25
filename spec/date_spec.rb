# frozen_string_literal: true

require_relative 'spec_helper.rb'

describe JekyllRecker::Date do
  let(:k) { Class.new { extend ::JekyllRecker::Date } }

  describe '#slice_by_consecutive' do
    it 'should slice a list of ascending dates' do
      dates = [
        ::Date.new(2001, 2, 3),
        ::Date.new(2001, 2, 4),
        ::Date.new(2001, 2, 6),
        ::Date.new(2001, 2, 7),
        ::Date.new(2001, 2, 8)
      ]

      expected = [
        [
          ::Date.new(2001, 2, 3),
          ::Date.new(2001, 2, 4)
        ],
        [
          ::Date.new(2001, 2, 6),
          ::Date.new(2001, 2, 7),
          ::Date.new(2001, 2, 8)
        ]
      ]

      expect(k.slice_by_consecutive(dates)).to eq(expected)
    end

    it 'should slice a list of descending dates' do
      dates = [
        ::Date.new(2001, 2, 8),
        ::Date.new(2001, 2, 7),
        ::Date.new(2001, 2, 6),
        ::Date.new(2001, 2, 4),
        ::Date.new(2001, 2, 3)
      ]

      expected = [
        [
          ::Date.new(2001, 2, 8),
          ::Date.new(2001, 2, 7),
          ::Date.new(2001, 2, 6)
        ],
        [
          ::Date.new(2001, 2, 4),
          ::Date.new(2001, 2, 3)
        ]
      ]

      expect(k.slice_by_consecutive(dates)).to eq(expected)
    end
  end

  describe '#calculate_streaks' do
    it 'should calculate streaks from ascending dates' do
      dates = [
        ::Date.new(2001, 2, 3),
        ::Date.new(2001, 2, 4),
        ::Date.new(2001, 2, 6),
        ::Date.new(2001, 2, 7),
        ::Date.new(2001, 2, 8)
      ]

      expected = [
        {
          'days' => 1,
          'start' => ::Date.new(2001, 2, 3),
          'end' => ::Date.new(2001, 2, 4)
        },
        {
          'days' => 2,
          'start' => ::Date.new(2001, 2, 6),
          'end' => ::Date.new(2001, 2, 8)
        }
      ]

      expect(k.calculate_streaks(dates)).to eq(expected)
    end

    it 'should calculate streaks from descending dates' do
      dates = [
        ::Date.new(2001, 2, 8),
        ::Date.new(2001, 2, 7),
        ::Date.new(2001, 2, 6),
        ::Date.new(2001, 2, 4),
        ::Date.new(2001, 2, 3)
      ]

      expected = [
        {
          'days' => 2,
          'start' => ::Date.new(2001, 2, 6),
          'end' => ::Date.new(2001, 2, 8)
        },
        {
          'days' => 1,
          'start' => ::Date.new(2001, 2, 3),
          'end' => ::Date.new(2001, 2, 4)
        }
      ]

      expect(k.calculate_streaks(dates)).to eq(expected)
    end
  end

  describe '#time_to_date' do
    it 'should convert a time to a date' do
      actual = k.time_to_date(Time.parse('2020-07-03').localtime)
      expected = Date.new(2020, 0o7, 0o3)
      expect(actual).to eq(expected)
    end
  end
end
