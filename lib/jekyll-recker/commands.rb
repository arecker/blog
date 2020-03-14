module Jekyll
  module Recker
    module Commands
      # Tweet
      class Tweet < Jekyll::Command
        class << self
          def init_with_program(prog)
            prog.command(:tweet) do |c|
              c.syntax "tweet"
              c.description 'tweet latest post'
              c.action do |args, options|
                client = Jekyll::Recker::Twitter.new
                Jekyll.logger.info 'discovering credentials'
                client.discover_credentials!
                Jekyll.logger.info "tweeting #{client.latest.data['title']}"
                client.post_latest!
              rescue => e
                Jekyll.logger.abort_with e.message
              end
            end
          end
        end
      end
    end
  end
end
