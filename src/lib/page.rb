# frozen_string_literal: true

module Blog
  # Object for working with pages.
  class Page
    attr_reader :source

    # Generates all site pages.
    def self.generate_all
      Files.pages.each do |page|
        target = Files.target(page.permalink)
        Files.generate(target) { page.render }
      end
    end

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
      Context.global.merge(
        {
          'banner' => banner,
          'description' => description,
          'permalink' => permalink,
          'title' => title
        }
      )
    end
  end
end
