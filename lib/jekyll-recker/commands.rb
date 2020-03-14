module Jekyll
  module Recker
    module Commands
      # Tweet
      class Tweet < Jekyll::Command
        class << self
          def init_with_program(prog)
            prog.command(:tweet) do |c|
              c.syntax 'tweet'
              c.description 'tweet latest post'
              c.action do |args, options|
                client = Jekyll::Recker::Twitter.new
                Recker.info 'discovering credentials'
                client.discover_credentials!
                Recker.info "tweeting #{client.latest.data['title']}"
                client.post_latest!
              rescue => e
                abort_with e.message
              end
            end
          end
        end
      end
      
      # Slack
      class Slack < Jekyll::Command
        class << self
          def init_with_program(prog)
            prog.command(:slack) do |c|
              c.syntax 'slack'
              c.description 'slack latest post'
              c.action do |args, options|
                Recker.info 'normally I would slack here'
              end
            end
          end
        end
      end
    end
  end
end
