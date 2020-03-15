# frozen_string_literal: true

lib = File.expand_path("lib", __dir__)
$LOAD_PATH.unshift(lib) unless $LOAD_PATH.include?(lib)

require 'jekyll-recker/version'

Gem::Specification.new do |spec|
  spec.name          = 'jekyll-recker'
  spec.version       = Jekyll::Recker::VERSION
  spec.authors       = ['Alex Recker']
  spec.email         = ['alex@reckerfamily.com']
  spec.summary       = 'This is the jekyll theme for my personal website.'
  spec.homepage      = 'https://www.alexrecker.com/jekyll-recker.html'
  spec.license       = 'GPLv3'
  spec.files         = [
    'LICENSE',
    'README.org',
    Dir['_includes/**/*.html'],
    Dir['_layouts/**/*.html'],
    Dir['assets/jekyll-recker.scss'],
    Dir['lib/**/*.rb'],
  ].flatten

  spec.add_runtime_dependency 'jekyll', '~> 3.8'
  spec.add_runtime_dependency 'slack-notifier'
  spec.add_runtime_dependency 'twitter'

  spec.add_development_dependency 'bundler'
  spec.add_development_dependency 'rake'
end
