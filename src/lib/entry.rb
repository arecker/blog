# frozen_string_literal: true

# Journal entry object.
class Entry
  attr_reader :source

  def initialize(source)
    @source = source
  end

  def date
    slug = File.basename(source, '-entry.md')
    Date.strptime(slug, '%Y-%m-%d')
  end

  def title
    date.strftime('%A, %B %-d %Y')
  end

  def description
    frontmatter.fetch('title')
  end

  def frontmatter
    @frontmatter ||= YAML.load_file(source)
  end

  def pathname
    "/#{File.basename(source, '-entry.md')}.html"
  end

  def banner?
    frontmatter.key? 'banner'
  end

  def banner
    frontmatter.fetch('banner')
  end
end
