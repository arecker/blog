# frozen_string_literal: true

lib = File.expand_path('lib', __dir__)
$LOAD_PATH.unshift(lib) unless $LOAD_PATH.include?(lib)

require 'jekyll_recker/version'

Gem::Specification.new do |spec|
  spec.name          = 'jekyll-recker'
  spec.version       = JekyllRecker::VERSION
  spec.authors       = ['Alex Recker']
  spec.email         = ['alex@reckerfamily.com']
  spec.summary       = 'The Greatest Jekyll Plugin in the World'
  spec.homepage      = 'https://www.github.com/arecker/blog'
  spec.license       = 'GPLv3'
  spec.files         = [
    Dir['lib/**/*.rb']
  ].flatten

  spec.add_runtime_dependency 'fastimage'
  spec.add_runtime_dependency 'gruff'
  spec.add_runtime_dependency 'jekyll', '~> 3.8'
  spec.add_runtime_dependency 'mini_magick'
  spec.add_runtime_dependency 'slack-notifier'
  spec.add_runtime_dependency 'twitter'
end
