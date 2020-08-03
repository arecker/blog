# frozen_string_literal: true

require 'spec_helper'

describe Blog::Dates do
  let(:k) { Class.new { extend ::Blog::Dates } }

  describe '#to_uyd_date' do
    it 'should convert a date into UYD show opening format' do
      expect(k.to_uyd_date(Date.new(2020, 1, 1))).to eq 'Wednesday, January 1 2020'
    end
  end
end
