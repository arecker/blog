# frozen_string_literal: true

require_relative './blog'

Blog::Files.tests.each do |file|
  require file
end
