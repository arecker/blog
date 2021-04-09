# frozen_string_literal: true

require 'date'

module Blog
  # Page Mixin for working with entries.
  module PageEntry
    def entry?
      File.expand_path('..', source) == Blog::Files.join('_posts')
    end

    def entry_date_title
      return nil unless entry?

      entry_date.strftime('%A, %B %-d %Y')
    end

    def entry_date_slug
      return nil unless entry?

      File.basename(source).sub(/-entry.md$/, '')
    end

    def entry_date
      return nil unless entry?

      Date.strptime(entry_date_slug, '%Y-%m-%d')
    end
  end

  # Mixin for injecting build information into pages.
  module PageBuild
    def build_year
      Time.new.year
    end

    def build_updated
      Time.new.to_s
    end

    def build_head
      `git rev-parse HEAD`.chomp
    end

    def build_short_head
      `git rev-parse --short HEAD`.chomp
    end

    def build_summary
      `git log -1 --pretty=format:"%s" HEAD`.chomp
    end
  end

  # Mixin for working with page navigation
  module PageNav
    def index?
      target_filename == 'index.html'
    end
  end

  # Wrapper object for working with pages.
  class Page
    include Blog::PageBuild
    include Blog::PageEntry
    include Blog::PageNav

    attr_reader :source

    def initialize(source='')
      @source = source
    end

    def markdown?
      ['.md', '.markdown'].include? File.extname(source)
    end

    def frontmatter
      YAML.load_file source
    end

    def content_literal
      Blog::Markup.strip_frontmatter(File.read(source))
    end

    def content
      if markdown?
        Blog::Markup.markdown_to_html(content_literal)
      else
        content_literal
      end
    end

    def target_filename
      if entry?
        "#{entry_date_slug}.html"
      else
        "#{File.basename(source, '.*')}.html"
      end
    end

    def title
      if entry?
        entry_date_title
      else
        frontmatter.fetch('title')
      end
    end

    def description
      if entry?
        frontmatter.fetch('title')
      else
        frontmatter.fetch('description')
      end
    end

    def banner
      return nil unless frontmatter.key?('banner')

      "/images/banners/#{frontmatter['banner']}"
    end

    def url
      "https://www.alexrecker.com/#{target_filename}"
    end
  end
end
