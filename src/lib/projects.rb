# frozen_string_literal: true

require 'yaml'

# Functions for extracting projects from entries.
module Projects
  # Returns the permalink for an entry file.
  def self.url(file)
    "#{File.basename(file, '-entry.md')}.html"
  end

  # Returns the project context.
  def self.context
    results = {
      'anti_journal' => [],
      'look_back' => [],
      'homework_vault' => [],
      'fred_poems' => []
    }
    entries.each do |e|
      title = YAML.load_file(e.source).fetch('title')
      results['anti_journal'] << { 'url' => url(e.source), 'title' => title } if title =~ /^anti-journal\ \d+$/
      results['look_back'] << { 'url' => url(e.source), 'title' => title } if title =~ /^looking back on/
      results['homework_vault'] << { 'url' => url(e.source), 'title' => title } if title =~ /^from the homework vault: /
      results['fred_poems'] << { 'url' => url(e.source), 'title' => title } if title =~ /^fred, the poet: \d$/
    end
    results
  end
end
