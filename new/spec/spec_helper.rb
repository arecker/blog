# frozen_string_literal: true

require 'simplecov'

def here_join(path)
  File.expand_path(File.join(__dir__, path))
end

SimpleCov.start do
  SimpleCov.coverage_dir here_join('../site/coverage')
end

require_relative '../blog.rb'

RSpec.configure do |config|
  config.expect_with :rspec do |expectations|
    expectations.include_chain_clauses_in_custom_matcher_descriptions = true
  end

  config.mock_with :rspec do |mocks|
    mocks.verify_partial_doubles = true
  end

  config.shared_context_metadata_behavior = :apply_to_host_groups
end
