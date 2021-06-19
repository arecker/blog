# frozen_string_literal: true

# Functions for extracting projects from entries.
module Projects
  # Returns a map of project keys to patterns.
  def self.pattern_map
    {
      anti_journal: /^anti-journal\ \d+$/,
      look_back: /^looking back on/,
      homework_vault: /^from the homework vault: /,
      fred_poems: /^fred, the poet: \d$/
    }
  end

  # Returns the project context.
  def self.context
    results = pattern_map.keys.map { |k| [k, []] }.to_h
    Files.entries.reverse.each do |e|
      pattern_map.each do |key, pattern|
        results[key] << e if pattern.match?(e.description)
      end
    end
    results
  end
end
