# frozen_string_literal: true

require 'erb'
require 'htmlbeautifier'

module Blog
  # Site Object
  class Site
    def initialize(output_dir, entries, template_path)
      @output_dir = output_dir
      @entries = entries
      @template = File.read(template_path)
    end

    def build!
      File.open(index_path, 'w') { |file| file.write(render_index) }
    end

    def index_path
      File.join(@output_dir, 'index.html')
    end

    def render_index
      HtmlBeautifier.beautify(ERB.new(@template).result(binding))
    end
  end
end
