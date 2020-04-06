# frozen_string_literal: true

module Jekyll
  module Recker
    # Commands
    module Commands
      # Share
      class Share < Jekyll::Command
        include Mixins::Logging

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

      # Slack
      class Slack < Jekyll::Command
        include Mixins::Logging
        def self.init_with_program(prog)
          prog.command(:slack) do |c|
            c.syntax 'slack'
            c.description 'slack latest post'
            c.option 'dry', '-d', '--dry', 'print message instead of posting'
            c.action { |args, opts| action(args, opts) }
          end
        end

        def self.action(_args, options)
          Recker::Slack.each_in_config(dry: options['dry']) do |client|
            logger.info "#{client.key}: discovering webhook"
            client.discover_webhook!
            logger.info "#{client.key}: posting #{client.latest.data['title']}"
            client.post_latest!
          end
        rescue ReckerError => e
          logger.abort_with e.message
        end
      end

      # Tweet
      class Tweet < Jekyll::Command
        include Mixins::Logging

        def self.init_with_program(prog)
          prog.command(:tweet) do |c|
            c.syntax 'tweet'
            c.description 'tweet latest post'
            c.option 'dry', '-d', '--dry', 'print message instead of tweeting'
            c.action { |args, opts| action(args, opts) }
          end
        end

        def self.action(_args, options)
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
