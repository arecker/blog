# frozen_string_literal: true

require 'html-proofer'
require 'jekyll'
require 'rspec/core/rake_task'
require 'rubocop/rake_task'
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

task :build do
  config = Jekyll.configuration(
    {
      'source' => './',
      'destination' => './_site'
    }
  )
  site = Jekyll::Site.new(config)
  Jekyll::Commands::Build.build site, config
end

task :html do
  options = {
    assume_extension: true,
    disable_external: true,
    file_ignore: [
      %r{/.*/docs/.*},
      %r{/.*/coverage/.*}
    ]
  }
  HTMLProofer.check_directory('./_site', options).run
end

task default: %w[style spec build docs html]
