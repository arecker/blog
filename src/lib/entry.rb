# frozen_string_literal: true

# Special type of Page object for working with journal entries.
class Entry < Page
  attr_reader :source

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
