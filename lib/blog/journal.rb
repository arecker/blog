# frozen_string_literal: true

require 'org-ruby'

module Blog
  # Journal
  class Journal
    def self.from_file(path)
      Blog.logger.info "loading journal from #{path.pretty_path}"
      new(Orgmode::Parser.load(path))
    end

    def initialize(parser)
      @parser = parser
    end

    def entries
      @entries ||= all_entries.select(&:public?).sort_by(&:date).reverse
    end

    private

    def all_entries
      entry_headlines.map { |h| Entry.new(h) }
    end

    def entry_headlines
      @parser.headlines.select { |h| h.level == 3 }
    end
  end
end
