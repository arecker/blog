# frozen_string_literal: true

require 'twitter'

module Blog
  # Twitter
  module Twitter
    def self.post(entry, creds)
      client = ::Twitter::REST::Client.new do |settings|
        settings.consumer_key = creds['consumer_api_key']
        settings.consumer_secret = creds['consumer_api_secret']
        settings.access_token = creds['access_token']
        settings.access_token_secret = creds['access_token_secret']
      end
      message = "#{entry.excerpt}\n#{entry.title}\n#{entry.permalink}"
      Blog.logger.info "tweeting #{entry.excerpt}"
      client.update(message)
    end
  end
end
