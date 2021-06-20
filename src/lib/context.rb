# frozen_string_literal: true

require 'json'

module Blog
  # Functions for working with site context.
  module Context
    # Generates all data files from global context.
    def self.generate_all
      Files.generate(Files.target('api/git.json')) { Git.context.to_json }
      Files.generate(Files.target('api/projects.json')) { Projects.context.to_json }
      Files.generate(Files.target('api/nav.json')) { Nav.pages.to_json }
      Files.generate(Files.target('api/stats.json')) { Stats.context.to_json }
    end

    # Returns global context for all templates.
    def self.global
      @global ||= {
        'entries' => Files.entries.reverse,
        'git' => Git,
        'info' => Info,
        'latest' => Files.entries.reverse.first,
        'nav' => Nav.pages,
        'projects' => Projects.context,
        'stats' => Stats.context
      }
    end
  end
end
