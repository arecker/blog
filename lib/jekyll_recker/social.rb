# frozen_string_literal: true

require 'slack-notifier'
require 'twitter'

module JekyllRecker
  module Social
    def self.action(site, args, options)
      args += %w[slack twitter] if args.empty?
      Slack.share(site, dry: options['dry']) if args.include?('slack')
      Twitter.share(site, dry: options['dry']) if args.include?('twitter')
    end

    # Backend
    #
    # Backend base class for social sharing backends.
    # @abstract
    class Share
      include Mixins::Logging

      def self.share(site, dry: false)
        backend = new(site, dry: dry)
        logger.info "#{backend.name} - building configuration"
        backend.configure!

        logger.info "#{backend.name} - sharing \"#{backend.latest_title}\""
        backend.post!
      end

      def initialize(site, dry: false)
        @site = site
        @dry = dry
      end

      def dry?
        @dry
      end

      def config
        @site.config.fetch('recker', {}).fetch(config_key, {})
      end

      def config_key
        self.class.const_get(:KEY)
      end
      alias name :config_key

      def post_body
        url = File.join @site.config['url'], latest.url
        <<~BODY
          #{latest.data['date'].strftime('%A, %B %-d %Y')}
          #{latest.data['title']}
          #{url}
        BODY
      end

      def latest
        @latest ||= @site.posts.docs.last
      end

      def latest_title
        latest.data['title']
      end

      def configure!
        raise NotImplementedError
      end

      def post!
        raise NotImplementedError
      end
    end

    # Slack
    #
    # Slack social sharing backend
    class Slack < Share
      KEY = 'slack'

      def configure!
        @creds = {}
        workspaces.each do |key, data|
          webhook = ENV["SLACK_#{key.upcase}_WEBHOOK"] || extract_from_config(data)
          if webhook.nil?
            raise "cannot find slack webhook for #{key} workspace!"
          end

          @creds[key] = webhook
        end
      end

      def post!
        message_body = ::Slack::Notifier::Util::LinkFormatter.format(post_body)
        workspaces.each do |key, config|
          logger.info "posting to #{key} workspace"
          if @dry
            logger.info("BEGIN MESSAGE\n#{message_body.strip}\nEND MESSAGE")
          else
            ::Slack::Notifier.new(
              @creds[key].strip,
              channel: config.fetch('channel'),
              username: config.fetch('username'),
              icon_emoji: config.fetch('emoji')
            ).post(text: message_body)
          end
        end
      end

      private

      def extract_from_config(data)
        cmd = data['webhook_cmd']
        return nil if cmd.nil?

        Shell.run(cmd)
      end

      def workspaces
        config.each
      end
    end

    # Twitter
    #
    # Twitter social sharing backend
    class Twitter < Share
      KEY = 'twitter'

      def configure!
        creds = extract_from_env || extract_from_config
        raise 'cannot find twitter credentials!' if creds.nil?

        @client = ::Twitter::REST::Client.new do |settings|
          settings.consumer_key = creds['consumer_api_key']
          settings.consumer_secret = creds['consumer_api_secret']
          settings.access_token = creds['access_token']
          settings.access_token_secret = creds['access_token_secret']
        end
      end

      def post!
        if dry?
          logger.info('tweeting in dry mode, printing message')
          logger.info("BEGIN TWEET\n#{post_body}END TWEET")
        else
          @client.update(post_body)
        end
      end

      private

      def extract_from_env
        values = cred_fieldnames.map { |k| ENV["TWITTER_#{k.upcase}"] }

        return nil if values.any? { |v| v.nil? || v.empty? }

        Hash[cred_fieldnames.zip(values)]
      end

      def extract_from_config
        values = cred_fieldnames.map do |k|
          Shell.run(config["#{k}_cmd"]).strip
        end

        return nil if values.any? { |v| v.nil? || v.empty? }

        Hash[cred_fieldnames.zip(values)]
      end

      def cred_fieldnames
        %w[
          access_token_secret
          access_token
          consumer_api_key
          consumer_api_secret
        ]
      end
    end
  end
end
