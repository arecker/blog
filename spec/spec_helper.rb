# frozen_string_literal: true

require 'bundler'
require 'json'
require 'simplecov'

class JekyllDataReporter
  def format(result)
    data = {}
    data[:timestamp] = result.created_at.to_i
    data[:command_name] = result.command_name
    data[:files] = []
    result.files.each do |sourceFile|
      next unless result.filenames.include? sourceFile.filename
      data[:files] << {
        filename: sourceFile.filename,
        covered_percent: sourceFile.covered_percent,
        coverage: sourceFile.coverage_data,
        covered_strength: sourceFile.covered_strength.nan? ? 0.0 : sourceFile.covered_strength, 
        covered_lines: sourceFile.covered_lines.count, 
        lines_of_code: sourceFile.lines_of_code, 
      }
    end
    data[:metrics] = {
      covered_percent: result.covered_percent,
      covered_strength: result.covered_strength.nan? ? 0.0 : result.covered_strength,
      covered_lines: result.covered_lines,
      total_lines: result.total_lines
    }
    
    json = data.to_json
    
    File.open(output_filepath, "w+") do |file|
      file.puts json
    end
    
    puts output_message(result)
    
    json
  end

  def output_filepath
    File.join Bundler.root, '_data/coverage.json'
  end
    
  def output_message(result)
    "Coverage report generated for #{result.command_name} to #{output_filepath}. #{result.covered_lines} / #{result.total_lines} LOC (#{result.covered_percent.round(2)}%) covered."
  end
end

SimpleCov.formatters = JekyllDataReporter
SimpleCov.start

require 'jekyll-recker'

RSpec.configure do |config|
  config.expect_with :rspec do |expectations|
    expectations.include_chain_clauses_in_custom_matcher_descriptions = true
  end

  config.mock_with :rspec do |mocks|
    mocks.verify_partial_doubles = true
  end

  config.shared_context_metadata_behavior = :apply_to_host_groups
end
