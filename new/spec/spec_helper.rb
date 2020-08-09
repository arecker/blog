# frozen_string_literal: true

require 'json'
require 'simplecov'

def here_join(path)
  File.expand_path(File.join(__dir__, path))
end

class DumpToTemp
  def format(result)
    json = JSON.pretty_generate(data(result))

    File.open(output_filepath, 'w+') do |file|
      file.puts json
    end

    json
  end

  def data(result)
    {
      metrics: {
        covered_percent: result.covered_percent,
        covered_strength: result.covered_strength.nan? ? 0.0 : result.covered_strength,
        covered_lines: result.covered_lines,
        total_lines: result.total_lines
      }
    }
  end

  def output_filepath
    here_join('../tmp/coverage.json')
  end
end

SimpleCov.formatters = SimpleCov::Formatter::MultiFormatter.new(
  [
    SimpleCov::Formatter::HTMLFormatter,
    DumpToTemp
  ]
)

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
