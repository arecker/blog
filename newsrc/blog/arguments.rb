# frozen_string_literal: true

require 'optparse'

module Blog
  # For deailing with command line arguments.
  module Arguments
    # Wrapper class around OptionParser arguments.
    class Arg
      attr_reader :symbol, :metavar, :default, :help

      def initialize(symbol, metavar, default, help)
        @symbol = symbol
        @metavar = metavar
        @default = default
        @help = help
      end

      def to_s
        "--#{symbol}=#{metavar}"
      end

      def required?
        default.nil?
      end
    end

    # Wrapper class around optparse.
    class Parser
      class MissingRequired < StandardError; end

      attr_reader :args

      def initialize(args = [])
        @args = args.map { |a| Arg.new(*a) }
      end

      def parse!
        optparser.parse!
        missing = args.select { |a| a.required? && !options.key?(a.symbol) }
        raise MissingRequired, missing.join(' ') if missing.any?
      end

      def options
        @options ||= args.each_with_object({}) do |arg, hash|
          hash[arg.symbol] = arg.default if arg.required?
        end.delete_if { |_k, v| v.nil? }
      end

      def optparser
        @optparser ||= OptionParser.new do |opts|
          args.each do |arg|
            opts.on(arg.to_s, arg.help) { |v| options[arg.symbol] = v unless v.nil? }
          end
        end
      end
    end

    # Parse commandline arguments based on a list of expected args.
    # Args is a list of lists, where one arg in the list is
    # [<key>, <valname>, <default>, <docstring>]
    def self.parse(args)
      parser = Parser.new args
      begin
        parser.parse!
        parser.options
      rescue Parser::MissingRequired => e
        puts "Missing: #{e.message}"
        exit(1)
      end
    end
  end
end
