 # frozen_string_literal: true

src = File.expand_path('src', __dir__)
$LOAD_PATH.unshift(src) unless $LOAD_PATH.include?(src)

Gem::Specification.new do |spec|
  spec.name          = 'blog'
  spec.version       = '0.0.0'
  spec.authors       = ['Alex Recker']
  spec.email         = ['alex@reckerfamily.com']
  spec.summary       = 'The Greatest Jekyll Plugin in the World'
  spec.homepage      = 'https://www.github.com/arecker/blog'
  spec.license       = 'GPLv3'
  spec.files         = [
    Dir['src/**/*.rb']
  ].flatten

  spec.add_runtime_dependency 'jekyll'
  spec.add_runtime_dependency 'rake'
  spec.add_runtime_dependency 'rspec'
  spec.add_runtime_dependency 'rubocop'
  spec.add_runtime_dependency 'simplecov'
  spec.add_runtime_dependency 'yard'
end
