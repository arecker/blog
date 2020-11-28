# frozen_string_literal: true

module Blog
  # Files
  module Files
    def root
      File.expand_path(File.join(__dir__, '../../'))
    end

    def join(*subpaths)
      File.join(*subpaths)
    end
  end
end
