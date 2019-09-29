# frozen_string_literal: true

require 'slack-notifier'

module Blog
  # Slack
  module Slacky
    def self.post(channel, url)
      notifier = ::Slack::Notifier.new(url, channel: channel, username: 'reckerbot')
      message = <<~MSG
        This is a message.
      MSG
      Slack::Notifier::Util::LinkFormatter.format(message)
      notifier.post text: message
    end
  end
end
