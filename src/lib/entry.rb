# frozen_string_literal: true

# Special type of Page object for working with journal entries.
class Entry < Page
  attr_reader :source
  attr_accessor :page_previous, :page_next

  def self.build_list
    Dir.glob(Files.join('_posts/*.md')).sort.map { |f| new f }
  end

  # Build paginated list of entries
  def self.build_paginated_list
    results = build_list
    Lists.each_previous_next(results) do |prv, cur, nxt|
      cur.page_next = nxt.permalink unless nxt.nil?
      cur.page_previous = prv.permalink unless prv.nil?
    end
    results
  end

  def permalink
    "#{File.basename(source, '-entry.md')}.html"
  end

  def date
    slug = File.basename(source, '-entry.md')
    Date.strptime(slug, '%Y-%m-%d')
  end

  def title
    date.strftime('%A, %B %-d %Y')
  end

  def description
    frontmatter.fetch('title').to_s
  end
end
