# frozen_string_literal: true

require 'slack-notifier'

module Jekyll
  # Recker
  module Recker
    # Slack
    class Slack
      include Jekyll::Recker::Mixins::Logging

      def self.each_in_config(dry: false)
        Configuration.slack.map do |key, body|
          yield new(key, body, dry: dry)
        end
      end

      attr_reader :key

      def initialize(config_key, config_body, dry: false)
        @key = config_key
        @data = config_body
        @webhook = nil
        @dry = dry
      end

      def discover_webhook!
        @webhook = ENV["SLACK_#{@key.upcase}_WEBHOOK"] || extract_from_config
        raise ReckerError, 'cannot find slack credentials!' if @webhook.nil?
      end

      def latest
        @latest ||= Configuration.latest_post
      end

      def post_latest!
        if @dry
          logger.info('postign in dry mode, printing message')
          logger.info("BEGIN MESSAGE\n#{message_body.strip}\nEND MESSAGE")
        else
          ::Slack::Notifier.new(
            @webhook.strip,
            channel: @data.fetch('channel'),
            username: @data.fetch('username'),
            icon_emoji: @data.fetch('emoji')
          ).post(text: message_body)
        end
      end

      private

      def message_body
        url = File.join Configuration.jekyll['url'], latest.url
        body = <<~MSG
          #{latest.data['date'].strftime('%A, %B %-d %Y')}
          #{latest.data['title']}
          #{url}
        MSG
        ::Slack::Notifier::Util::LinkFormatter.format(body)
      end

      def extract_from_config
        cmd = @data['webhook_cmd']
        return nil if cmd.nil?

        Recker.shell(cmd)
      end
    end
  end
end
