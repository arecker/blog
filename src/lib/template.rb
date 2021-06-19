# frozen_string_literal: true

require 'date'
require 'erb'
require 'ostruct'
require 'time'

# Functions for working with templates
module Template
  def self.template(name, content: '')
    body = File.read(Files.join('src/templates/', "#{name}.erb"))
    body.sub!(/\n\$CONTENT\$\n/, content)
    ERB.new(body, trim_mode: '-')
  end

  # Renders template specificed by name with the provided context.
  def self.render(name, content = '', context)
    namespace = OpenStruct.new(context)
    template(name, content: content).result(namespace.instance_eval { binding })
  end
end
