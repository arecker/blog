# frozen_string_literal: true

lib = File.expand_path("lib", __dir__)
$LOAD_PATH.unshift(lib) unless $LOAD_PATH.include?(lib)

require "jekyll-recker/version"

Gem::Specification.new do |spec|
  spec.name          = "jekyll-recker"
  spec.version       = Jekyll::Recker::VERSION
  spec.authors       = ["Alex Recker"]
  spec.email         = ["alex@reckerfamily.com"]

  spec.summary       = 'This is the jekyll theme for my personal website.'
  spec.homepage      = "https://www.alexrecker.com/jekyll-recker/"
  spec.license       = "GPLv3"

  spec.files         = `git ls-files -z`.split("\x0").select { |f| f.match(%r!^(assets|_layouts|_includes|_sass|LICENSE|README)!i) }

  spec.add_runtime_dependency "jekyll", "~> 3.8"

  spec.add_development_dependency "bundler", "~> 1.16"
  spec.add_development_dependency "rake", "~> 12.0"
end
