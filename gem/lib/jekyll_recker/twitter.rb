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
        entry = nil # TODO: get latest entry
        message = "#{entry.excerpt}\n#{entry.title}\n#{entry.permalink}"
        Jekyll.logger.info "tweeting #{entry.title}"
        # client.update(message)
      end

      def latest
      end

      private

      def set_credentials!
        @client ||= ::Twitter::REST::Client.new do |settings|
          settings.consumer_key = creds['consumer_api_key']
          settings.consumer_secret = creds['consumer_api_secret']
          settings.access_token = creds['access_token']
          settings.access_token_secret = creds['access_token_secret']
        end
      end

      def extract_from_env
        values = cred_fieldnames.map { |k| ENV[k.upcase] }
        values unless values.any? { |v| v.nil? || v.empty? }
      end

      def extract_from_config
        values = cred_fieldnames.map { |k| shell(config["#{k}_cmd"]) }
        values unless values.any? { |v| v.nil? || v.empty? }
      end

      def shell(cmd)
        Jekyll.logger.info "running command: #{cmd}"
        `#{cmd}`
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
    end
  end
end
