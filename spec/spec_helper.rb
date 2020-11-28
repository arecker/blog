# frozen_string_literal: true

plugin_dir = File.expand_path(File.join(__dir__, '../_plugins'))
$LOAD_PATH.unshift(plugin_dir) unless $LOAD_PATH.include? plugin_dir

require 'blog'

RSpec.configure do |config|
  config.expect_with :rspec do |expectations|
    expectations.include_chain_clauses_in_custom_matcher_descriptions = true
  end

  config.mock_with :rspec do |mocks|
    mocks.verify_partial_doubles = true
  end

  config.shared_context_metadata_behavior = :apply_to_host_groups
end
