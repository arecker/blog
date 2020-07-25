# frozen_string_literal: true

module JekyllRecker
  # Math Module
  module Math
    def average(numlist)
      calc = numlist.inject { |sum, el| sum + el }.to_f / numlist.size
      calc.round
    end

    def total(numlist)
      numlist.inject(0) { |sum, x| sum + x }
    end
  end
end
