# frozen_string_literal: true

# rubocop:disable Metrics/BlockLength
describe Blog::Time do
  let(:k) { Class.new { extend ::Blog::Time } }

  describe '#to_uyd_date' do
    it 'should convert a date into UYD show opening format' do
      expect(k.to_uyd_date(::Date.new(2020, 1, 1))).to eq 'Wednesday, January 1 2020'
    end
  end

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

  describe '#date_to_time' do
    it 'should convert a date to a time' do
      actual = k.date_to_time(::Date.new(2020, 1, 1))
      expect(actual).to be_a ::DateTime
      expect([actual.hour, actual.minute, actual.second]).to eq([0, 0, 0])
    end
  end
end
# rubocop:enable Metrics/BlockLength
