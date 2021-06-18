# frozen_string_literal: true

require_relative './blog'

Files.tests.each do |file|
  require file
end
