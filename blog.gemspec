# frozen_string_literal: true

Gem::Specification.new do |s|
  s.name        = 'blog'
  s.version     = '0.1.0'
  s.licenses    = ['MIT']
  s.summary     = ''
  s.description = ''
  s.authors     = ['Alex Recker']
  s.email       = 'alex@reckerfamily.com'

  s.files          = Dir.glob('src/**/*').reject { |e| File.directory?(e) }
  s.require_paths  = ['src']

  s.bindir      = 'src/bin'
  s.executables = ['blog']

  s.required_ruby_version = "= #{File.read('.ruby-version').chomp}"

  s.add_runtime_dependency 'kramdown', '2.3.1'
  s.add_runtime_dependency 'parallel', '1.20.1'

  s.add_development_dependency 'pry', '0.14.1'
  s.add_development_dependency 'rubocop', '1.17.0'
end
