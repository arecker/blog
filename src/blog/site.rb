# frozen_string_literal: true

module Blog
  # Site
  class Site
    def initialize(site)
      @site = site
    end

    def entries
      @entries ||= build_entries
    end

    def latest
      entries.first
    end

    def pages
      @site.pages
    end

    def production?
      ENV['JEKYLL_ENV'] == 'production'
    end

    def data
      @site.data
    end

    def url
      @site.config['url']
    end

    def word_counts
      entries.collect(&:word_count)
    end

    def words
      entries.collect(&:words).flatten
    end

    def dates
      entries.collect(&:date)
    end

    def images
      exts = ['.jpg', 'jpeg', '.png', '.svg']
      @site.static_files.collect(&:path).select { |f| exts.include? File.extname(f) }
    end

    def root
      File.absolute_path(File.join(__dir__, '../../'))
    end

    def root_join(path)
      File.join(root, path)
    end

    def recker_config
      @site.config.fetch('recker', {})
    end

    def config
      @site.config
    end

    def graphs_dir
      recker_config.fetch('graphs', 'assets/images/graphs/')
    end

    def data_dir
      File.join root, '_data'
    end

    def tmp_join(path)
      File.join root, 'tmp', path
    end

    def graphs_join(path)
      File.join root, 'assets/images/graphs/', path
    end

    def site_join(path)
      File.join(root, '_site', path)
    end

    private

    def build_entries
      @site.posts.docs
           .select(&:published?)
           .sort_by(&:date)
           .reverse
           .map { |p| Entry.new(p) }
    end
  end
end
