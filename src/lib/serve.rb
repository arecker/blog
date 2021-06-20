# frozen_string_literal: true

require 'webrick'

module Blog
  # Functions for working with the local web server.
  module Serve
    def self.start
      log "serving #{Files.shorten(root)} via HTTP on port #{port}"
      trap 'INT' do
        shutdown
      end
      server.start
    end

    # Returns instance of HTTP server.
    def self.server
      @server ||= WEBrick::HTTPServer.new(Port: port, DocumentRoot: root)
    end

    # Shuts down the server gracefully.
    def self.shutdown
      log 'shutting down webserver'
      server.shutdown
    end

    # Returns web server port
    def self.port
      5000
    end

    # Returns web server root
    def self.root
      Files.target
    end
  end
end
