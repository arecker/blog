# frozen_string_literal: true

require 'slack-notifier'

module Blog
  # Slack
  module Slacky
    def self.post(entry, url, info)
      notifier = ::Slack::Notifier.new(
        url.strip,
        channel: info['channel'],
        username: info['username'],
        icon_emoji: ':reckerbot:'
      )
      message = "#{entry.title} - #{entry.excerpt}\n#{entry.permalink}"
      Slack::Notifier::Util::LinkFormatter.format(message)
      notifier.post text: message
    end
  end
end
