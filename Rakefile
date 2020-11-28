# frozen_string_literal: true

require 'rubocop/rake_task'
require 'rspec/core/rake_task'
require 'yard'

RuboCop::RakeTask.new(:style)
RSpec::Core::RakeTask.new(:spec)
YARD::Rake::YardocTask.new(:docs)

task default: %w[style spec docs]
