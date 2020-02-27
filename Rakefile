# frozen_string_literal: true

require 'rspec/core/rake_task'
require_relative './lib/blog'

RSpec::Core::RakeTask.new(:spec)

task default: :spec

desc 'generate wordcloud image'
task :wordcloud do
  reject = %w[
  a the me i and as
  ]

  config = Blog::Config.load_from_file
  journal = Blog::Journal.from_file(config.journal_path)
  words = journal.public_entries.collect { |e| e.body_text.words }.flatten
  words = words.map { |w| w.gsub(/[^a-z]/i, '') }
  words = words.reject(&:empty?)
  words = words.map(&:downcase).reject { |w| reject.include? w }.sort
  File.open(File.join(config.blog_repo, 'words.txt'), 'w') do |f|
    f.puts words.join(' ')
  end
end
