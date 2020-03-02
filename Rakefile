# frozen_string_literal: true

require 'rspec/core/rake_task'
require_relative './lib/blog'

RSpec::Core::RakeTask.new(:spec)

task default: :spec

desc 'generate wordcloud image'
task :wordcloud do
  config = Blog::Config.load_from_file
  journal = Blog::Journal.from_file(config.journal_path)
  words = journal.public_entries.collect { |e| e.body_text.words }.flatten
  File.open(File.join(config.blog_repo, 'words.txt'), 'w') do |f|
    f.puts words.join(' ')
  end
  command = [
    'wordcloud_cli',
    '--text words.txt',
    '--imagefile images/words.png',
    '--height 200 --width 1500',
    '--background white --color gray'
  ].join(' ')
  system(command)
end
