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

    def occurences(keys, targets)
      results = Hash.new(0)
      targets.each do |target|
        results[target] += 1 if keys.include? target
      end
      results
    end
  end
end
