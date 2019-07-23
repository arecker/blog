# frozen_string_literal: true

require 'erb'
require 'htmlbeautifier'
require 'rss'
require 'time'

module Blog
  # Site Object
  class Site
    def initialize(output_dir, entries, template_path)
      @output_dir = output_dir
      @entries = entries
      @template = File.read(template_path)
    end

    def build!
      index_path = File.join(@output_dir, 'index.html')
      File.open(index_path, 'w') { |file| file.write(render_index) }

      feed_path = File.join(@output_dir, 'feed.xml')
      File.open(feed_path, 'w') { |file| file.write(render_feed) }
    end

    def render_index
      HtmlBeautifier.beautify(ERB.new(@template).result(binding))
    end

    def render_feed
      RSS::Maker.make("atom") do |maker|
        maker.channel.author = "Alex Recker"
        maker.channel.updated = Time.parse(@entries[0].date.to_s)
        maker.channel.about = "https://www.alexrecker.com/"
        maker.channel.title = "Alex Recker's Journal"
        @entries.each do |entry|
          maker.items.new_item do |item|
            item.link = "https://www.alexrecker.com/##{entry.slug}"
            item.title = entry.feed_title
            item.updated = Time.parse(entry.date.to_s)
          end
        end
      end
    end
  end
end
