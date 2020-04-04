# frozen_string_literal: true

module Jekyll
  module Recker
    module Commands
      # Share
      class Share < Jekyll::Command
        include Jekyll::Recker::LoggingMixin

        def self.init_with_program(prog)
          prog.command(:share) do |c|
            c.syntax 'share'
            c.description 'Share latest post with each configured backend'
            c.option 'dry', '-d', '--dry', 'perform dry run'
            c.action do |_args, _options|
              logger.info 'normally I\'d share here'
            rescue ReckerError => e
              logger.abort_with e.message
            end
          end
        end
      end
    end
  end
end
