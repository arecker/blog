# frozen_string_literal: true

require 'blog/version'
require 'blog/entry'
require 'blog/site'

# Blog
module Blog
  def self.build!(journal_path, output_directory, template_path)
    entries = Entry.last_five_from_file(journal_path)
    Site.new(output_directory, entries, template_path).build!
  end
end
