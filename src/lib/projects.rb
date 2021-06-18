# frozen_string_literal: true

# Functions for extracting projects from entries.
module Projects
  # Returns a map of project keys to patterns.
  def self.pattern_map
    {
      'anti_journal' => /^anti-journal\ \d+$/,
      'look_back' => /^looking back on/,
      'homework_vault' => /^from the homework vault: /,
      'fred_poems' => /^fred, the poet: \d$/
    }.sort
  end

  # Returns the project context.
  def self.context
    results = Hash.new { |h, k| h[k] = [] }
    Files.entries.reverse.each do |e|
      pattern_map.each do |key, pattern|
        if pattern.match?(e.description)
          results[key] << { 'url' => e.permalink, 'title' => e.description }
          break
        end
      end
    end
    results
  end
end
