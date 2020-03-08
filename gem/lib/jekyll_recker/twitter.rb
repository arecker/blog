# frozen_string_literal: true
require 'twitter'

module Jekyll
  module Recker
    # Twitter Client
    class Twitter
      class CannotFindCreds < StandardError
        def initialize(msg = 'could not find twitter credentials')
          super
        end
      end

      def discover_credentials!
        @creds = extract_from_env || extract_from_config
        raise CannotFindCreds if @creds.nil?
        set_credentials!
      end

      def post_latest!
        @client.update(tweet_body)
      end

      def latest
        @latest ||= site.posts.docs.last
      end

      private

      def tweet_body
        url = File.join Jekyll.configuration['url'], latest.url
        <<~TWEET
          #{latest.data['excerpt']}
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
        Hash[cred_fieldnames.zip(values)] unless values.any? { |v| v.nil? || v.empty? }
      end

      def extract_from_config
        values = cred_fieldnames.map { |k| shell(config["#{k}_cmd"]) }
        Hash[cred_fieldnames.zip(values)] unless values.any? { |v| v.nil? || v.empty? }
      end

      def shell(cmd)
        Jekyll.logger.info "running command: #{cmd}"
        `#{cmd}`.strip
      end

      def cred_fieldnames
        [
          'access_token_secret',
          'access_token',
          'consumer_api_key',
          'consumer_api_secret'
        ]
      end

      def config
        @config ||= Jekyll.configuration.fetch('recker', {}).fetch('twitter', {})
      end

      def site
        @site = Jekyll::Site.new(Jekyll.configuration)
        @site.process
        @site
      end
    end
  end
end
