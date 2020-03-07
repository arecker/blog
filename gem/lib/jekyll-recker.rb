module Jekyll
  module Recker
    class Tweet < Jekyll::Command
      class << self
        def init_with_program(prog)
          prog.command(:tweet) do |c|
            c.syntax "tweet"
            c.description 'tweet latest post'
            c.action do |args, options|
              Jekyll.logger.info 'I would normally tweet here'
            end
          end
        end
      end
    end
  end
end
