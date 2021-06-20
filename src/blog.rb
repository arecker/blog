# frozen_string_literal: true

$LOAD_PATH.unshift File.dirname(__FILE__)

##
# Blog
# The greatest static journal generator ever written.
module Blog
  autoload :Context, 'lib/context'
  autoload :Entry, 'lib/entry'
  autoload :Feeds, 'lib/feeds'
  autoload :Files, 'lib/files'
  autoload :Git, 'lib/git'
  autoload :Info, 'lib/info'
  autoload :Lists, 'lib/lists'
  autoload :Log, 'lib/log'
  autoload :Markdown, 'lib/markdown'
  autoload :Nav, 'lib/nav'
  autoload :Page, 'lib/page'
  autoload :Projects, 'lib/projects'
  autoload :Run, 'lib/run'
  autoload :Serve, 'lib/serve'
  autoload :Shell, 'lib/shell'
  autoload :Stats, 'lib/stats'
  autoload :Template, 'lib/template'

  # Runs the main blog routine.
  def self.main
    Run.greeting

    time = Run.time_it do
      Run.data
      Run.feeds
      Run.pages
      Run.entries
    end

    Run.section('build report') do
      Log.info "total time: #{time.round(2)}s"
    end
  end
end
