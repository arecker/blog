# frozen_string_literal: true

require 'yaml'

module Blog
  # Config
  class Config
    attr_reader :data

    def self.config_path
      File.expand_path('~/.publisher.yml')
    end

    def self.load_from_file
      if File.file? config_path
        Blog.logger.info "loading config from #{config_path.pretty_path}"
        new(YAML.load_file(config_path) || {})
      else
        Blog.logger.error "#{config_path.pretty_path} not found!"
        nil
      end
    end

    def required_keys
      %w[journal_path stats_path posts_dir blog_repo bucket aws_access_key_id_cmd aws_secret_access_key_cmd]
    end

    def initialize(data)
      @data = data
    end

    def validate!
      missing = missing_fields

      if missing.any?
        Blog.logger.error "missing configuration: #{missing_fields.to_and_list}"
        false
      else
        Blog.logger.info 'configuration is valid'
        true
      end
    end

    def journal_path
      File.expand_path(@data.fetch('journal_path'))
    end

    def posts_dir
      File.expand_path(@data.fetch('posts_dir'))
    end

    def site_dir
      File.join(File.expand_path(blog_repo), '_site')
    end

    def blog_repo
      File.expand_path(@data.fetch('blog_repo'))
    end

    def stats_path
      File.expand_path(@data.fetch('stats_path'))
    end

    def log_level
      @data.fetch('log_level', 'INFO').upcase
    end

    def use_git?
      @data.fetch('use_git', 'true').to_s.downcase == 'true'
    end

    def bucket
      @bucket ||= @data.fetch('bucket')
    end

    def aws_creds
      @aws_creds ||= {
        's3_id' => `#{s3_id_cmd}`.strip,
        's3_secret' => `#{s3_secret_cmd}`.strip
      }
    end

    def slacks
      @data.fetch('slacks', [])
    end

    private

    def s3_id_cmd
      @data.fetch('aws_access_key_id_cmd')
    end

    def s3_secret_cmd
      @data.fetch('aws_secret_access_key_cmd')
    end

    def missing_fields
      required_keys.reject { |k| @data.key? k }
    end
  end
end
