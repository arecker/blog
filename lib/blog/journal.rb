# frozen_string_literal: true

require 'org-ruby'

module Blog
  # Journal
  class Journal
    def self.from_file(path)
      new(Orgmode::Parser.load(path))
    end

    def logger
      Blog::Log.logger
    end

    def initialize(parser)
      @parser = parser
    end

    def public_entries
      @public_entries ||= all_entries.select(&:public?).sort_by(&:date).reverse
    end

    def private_entries
      @private_entries ||= all_entries.reject(&:public?).sort_by(&:date).reverse
    end

    def write_public_entries!(dir)
      public_entries.each do |entry|
        target = File.join(dir, entry.filename)
        logger.debug "writing #{entry.title} to #{target.pretty_path}"
        File.open(target, 'w+') { |f| f.write(entry.to_html) }
      end
    end

    def all_entries
      entry_headlines.map { |h| Entry.new(h) }
    end

    private

    def entry_headlines
      @parser.headlines.select { |h| h.level == 3 }
    end
  end
end
