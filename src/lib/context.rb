# frozen_string_literal: true

require 'json'

module Blog
  # Functions for working with site context.
  module Context
    # Returns global context for all templates.
    def self.global
      @global ||= {
        'entries' => Files.entries.reverse,
        'git' => Git,
        'info' => Info,
        'latest' => Files.entries.reverse.first,
        'nav' => Nav.pages,
        'projects' => Projects.context
      }
    end
  end
end
