# frozen_string_literal: true

# Functions for clever list things.
module Lists
  def self.each_previous_next(collection, &block)
    collection.each_with_index do |element, index|
      prv = collection[index - 1] unless index.zero?
      nxt = collection[index + 1] unless index == collection.size - 1
      block.call(prv, element, nxt)
    end
  end
end
