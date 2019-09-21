# frozen_string_literal: true

# Blog
module Blog
  require_relative 'blog/config'
  require_relative 'blog/entry'
  require_relative 'blog/journal'
  require_relative 'blog/log'
  require_relative 'blog/words'

  def self.logger
    Blog::Log.logger
  end

  def self.go_go_gadget_publish!
    logger.info 'starting publisher'
    config = Blog::Config.load_from_file || exit(1)

    logger.info 'validating config'
    config.validate!

    journal = Blog::Journal.from_file(config.journal_path)

    logger.info "writing #{journal.entries.count.pretty} entries"
    journal.entries.each do |entry|
      target = File.join(config.posts_dir, entry.filename)
      logger.debug "writing #{entry.title} to #{target.pretty_path}"
      File.open(target, 'w+') { |f| f.write(entry.to_html) }
    end
  end
end
