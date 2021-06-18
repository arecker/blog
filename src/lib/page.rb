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

  def content
    Markdown.strip_frontmatter(File.read(source))
  end

  def render
    padded = content.lines.map { |l| "    #{l}" }.join
    Template.render('page.html', padded, context)
  end

  def context
    {
      'banner' => banner,
      'description' => description,
      'info' => info,
      'pagination' => pagination,
      'permalink' => permalink,
      'title' => title
    }
  end

  def info
    Info.context
  end

  def pagination
    nil
  end
end
