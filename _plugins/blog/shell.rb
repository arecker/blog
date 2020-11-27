# frozen_string_literal: true

require 'open3'

module Blog
  # Shell
  module Shell
    # ShellCommand
    class ShellCommand
      include Blog::Logging

      attr_reader :cmd, :stdout, :stderr, :status

      def initialize(cmd)
        @cmd = cmd
      end

      def run!
        @stdout, @err, @status = Open3.capture3(cmd)
        debug(to_s)
      end

      def failed?
        !@status.success?
      end

      def to_s
        msg = "`#{cmd}` returned #{status}"
        msg += "\n--- STDOUT\n#{stdout}" if stdout
        msg += "\n--- STDERR\n#{stderr}" if stderr
        msg
      end
    end

    def shell(cmd, raises: true)
      result = ShellCommand.new(cmd)
      result.run!
      raise result.to_s if raises && result.failed?

      result.stdout
    end
  end
end
