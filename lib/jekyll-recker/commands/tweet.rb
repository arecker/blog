# frozen_string_literal: true

module Jekyll
  module Recker
    module Commands
      # Tweet
      class Tweet < Jekyll::Command
        include LoggingMixin

        class << self
          def init_with_program(prog)
            prog.command(:tweet) do |c|
              c.syntax 'tweet'
              c.description 'tweet latest post'
              c.option 'dry', '-d', '--dry', 'print message instead of tweeting'
              c.action do |_args, options|
                client = Jekyll::Recker::Twitter.new(dry: options['dry'])
                logger.info 'discovering credentials'
                client.discover_credentials!
                logger.info "tweeting #{client.latest.data['title']}"
                client.post_latest!
              rescue ReckerError => e
                logger.abort_with e.message
              end
            end
          end
        end
      end
    end
  end
end
