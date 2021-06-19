# frozen_string_literal: true

# Special type of Page object for working with journal entries.
class Entry < Page
  attr_reader :source
  attr_accessor :page_previous, :page_next

  def self.build_list
    Dir.glob(Files.join('entries/*.md')).sort.map { |f| new f }
  end

  # Build paginated list of entries
  def self.build_paginated_list
    results = build_list
    Lists.each_previous_next(results) do |nxt, cur, prv|
      cur.page_next = nxt.permalink unless nxt.nil?
      cur.page_previous = prv.permalink unless prv.nil?
    end
    results
  end

  # Generate all journal entries
  def self.generate_all
    ::Parallel.map(build_paginated_list) do |entry|
      target = Files.target(entry.permalink)
      Files.generate(target) { entry.render }
    end
  end

  def permalink
    "#{File.basename(source, '-entry.md')}.html"
  end

  def content
    stripped = Markdown.strip_frontmatter(File.read(source))
    Markdown.to_html(stripped)
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

  def context
    super.merge({ 'page_next' => page_next, 'page_previous' => page_previous })
  end
end
