# frozen_string_literal: true

module Jekyll
  module Recker
    module Commands
      # Slack
      class Slack < Jekyll::Command
        class << self
          def init_with_program(prog)
            prog.command(:slack) do |c|
              c.syntax 'slack'
              c.description 'slack latest post'
              c.option 'dry', '-d', '--dry', 'print message instead of posting'
              c.action do |_args, options|
                Recker::Slack.each_in_config(dry: options['dry']) do |client|
                  Recker.info "#{client.key}: discovering webhook"
                  client.discover_webhook!
                  Recker.info "#{client.key}: posting #{client.latest.data['title']}"
                  client.post_latest!
                end
              rescue ReckerError => e
                Recker.abort_with e.message
              end
            end
          end
        end
      end
    end
  end
end
