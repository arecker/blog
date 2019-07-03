# frozen_string_literal: true

lib = File.expand_path('lib', __dir__)
$LOAD_PATH.unshift(lib) unless $LOAD_PATH.include?(lib)
require 'blog/version'

Gem::Specification.new do |spec|
  spec.name          = 'blog'
  spec.version       = Blog::VERSION
  spec.authors       = ['Alex Recker']
  spec.email         = ['alex@reckerfamily.com']
  spec.summary       = 'The script that generates my website.'
  spec.homepage      = 'https://github.com/arecker/blog'
  spec.files         = Dir.chdir(File.expand_path(__dir__)) do
    `git ls-files -z`.split("\x0").reject do |f|
      f.match(%r{^(test|spec|features)/})
    end
  end
  spec.bindir        = 'bin'
  spec.executables   = ['blog']
  spec.require_paths = ['lib']
  spec.add_development_dependency 'bundler', '~> 2.0'
  spec.add_development_dependency 'rake', '~> 10.0'
  spec.add_runtime_dependency 'htmlbeautifier'
  spec.add_runtime_dependency 'org-ruby'
end
