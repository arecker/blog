# frozen_string_literal: true

module Blog
  # Functions that deal with logging and output.
  module Log
    # Logs an informateive message for the user.
    def self.info(msg)
      puts "blog :: #{msg}"
    end
  end
end
