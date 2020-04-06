# frozen_string_literal: true

require 'twitter'

module Jekyll
  module Recker
    # Twitter Client
    class Twitter
      include Mixins::Logging

      def initialize(dry: false)
        @dry = dry
      end

      def discover_credentials!
        @creds = extract_from_env || extract_from_config
        raise ReckerError, 'cannot find twitter credentials!' if @creds.nil?

        set_credentials!
      end

      def post_latest!
        if @dry
          logger.info('tweeting in dry mode, printing message')
          logger.info("BEGIN TWEET\n#{tweet_body.strip}\nEND TWEET")
        else
          @client.update(tweet_body)
        end
      end

      def latest
        Configuration.latest_post
      end

      private

      def tweet_body
        url = File.join Configuration.jekyll['url'], latest.url
        <<~TWEET
          #{latest.data['date'].strftime('%A, %B %-d %Y')}
          #{latest.data['title']}
          #{url}
        TWEET
      end

      def set_credentials!
        @client ||= ::Twitter::REST::Client.new do |settings|
          settings.consumer_key = @creds['consumer_api_key']
          settings.consumer_secret = @creds['consumer_api_secret']
          settings.access_token = @creds['access_token']
          settings.access_token_secret = @creds['access_token_secret']
        end
      end

      def extract_from_env
        values = cred_fieldnames.map { |k| ENV[k.upcase] }

        return nil if values.any? { |v| v.nil? || v.empty? }

        Hash[cred_fieldnames.zip(values)]
      end

      def extract_from_config
        values = cred_fieldnames.map do |k|
          Recker.shell(Configuration.twitter["#{k}_cmd"]).strip
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
