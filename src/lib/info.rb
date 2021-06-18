# frozen_string_literal: true

require 'date'
require 'time'

# Functions for getting basic build info.
module Info
  # Returns full info context.
  def self.context
    build.merge(nav).merge(Git.context)
  end

  # Returns build info context.
  def self.build
    {
      'build_year' => Date.today.year,
      'build_time' => Time.now
    }
  end

  # Returns nav context.
  def self.nav
    {
      'nav' => Nav.pages
    }
  end
end
