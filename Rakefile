# frozen_string_literal: true

require 'bundler/gem_tasks'
require 'pandoc-ruby'
require 'rspec/core/rake_task'
require_relative './lib/blog'

RSpec::Core::RakeTask.new(:spec)

task default: :spec

class JournalConverter
  def initialize
    config = Blog::Config.load_from_file
    @journal = Blog::Journal.from_file(config.journal_path)
  end

  def convert
    @journal.all_entries.each do |e|
      target = "_posts/#{e.date_slug}-#{e.date_slug}.html.md"
      content = <<~CONTENT
        ---
        title: #{e.excerpt}
        ---

        #{body(e)}
      CONTENT
      open(target, 'w') do |f|
        f.puts content
      end
    end
  end

  def body(entry)
    content = entry.body_text.gsub("\n ", "\n").strip
    pandoc = PandocRuby.new(
      content,
      :reference_links,
      from: :org, to: 'markdown-smart'
    )
    pandoc.convert
  end
end

desc 'convert journal.org to jekyll posts'
task :convert do
  converter = JournalConverter.new
  converter.convert
end

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
