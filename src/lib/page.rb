# frozen_string_literal: true

# Object for working with pages.
class Page
  attr_reader :source

  def initialize(source)
    @source = source
  end

  def frontmatter
    @frontmatter ||= YAML.load_file(source)
  end

  def permalink
    File.basename(source)
  end

  def title
    frontmatter.fetch('title').to_s
  end

  def description
    frontmatter.fetch('description').to_s
  end

  def banner
    frontmatter['banner']
  end

  def info
    Info.context
  end

  def pagination
    nil
  end
end
