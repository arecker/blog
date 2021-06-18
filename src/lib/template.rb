# frozen_string_literal: true

require 'date'
require 'erb'
require 'ostruct'
require 'time'

ATOM_LIMIT = 20

# Functions for working with templates
module Template
  def self.template(name)
    ERB.new(File.read(Files.join('src/templates/', "#{name}.erb")))
  end

  # Renders template specificed by name with the provided context.
  def self.render(name, context)
    namespace = OpenStruct.new(context)
    template(name).result(namespace.instance_eval { binding })
  end
end
