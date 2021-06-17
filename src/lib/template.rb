# frozen_string_literal: true

require 'date'
require 'erb'
require 'time'

ATOM_LIMIT = 20

# Functions for working with templates
module Template
  def self.sitemap
    ERB.new template('sitemap.xml.erb')
  end

  def self.feed
    ERB.new template('feed.xml.erb')
  end

  def self.template(name)
    File.read(join('src/templates/', name))
  end
end
