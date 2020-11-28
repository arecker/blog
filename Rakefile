# frozen_string_literal: true

require 'rubocop/rake_task'
require 'rspec/core/rake_task'
require 'yard'

RuboCop::RakeTask.new(:style)
RSpec::Core::RakeTask.new(:spec)
YARD::Rake::YardocTask.new(:docs) do |t|
  t.options = [
    '--output-dir=_site/docs/',
    '--readme=README.md'
  ]
  t.files = ['src/**/*.rb']
end

task default: %w[style spec docs]
