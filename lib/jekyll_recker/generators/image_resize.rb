# frozen_string_literal: true

module JekyllRecker
  module Generators
    # Image Resize Generator
    class ImageResize < Jekyll::Generator
      include BaseGenerator

      def generate(site)
        @site = site
        if production?
          logger.info 'production detected, skipping images'
          return
        else
          logger.info 'loading image resizing deps'
          require 'fastimage'
          require 'mini_magick'          
        end
        logger.info 'checking images'
        resizeable_images.each do |f, d|
          logger.info "resizing #{f} to fit #{d}"
          image = MiniMagick::Image.new(f)
          image.resize d
        end
      end

      def image?(file)
        ['.jpg', 'jpeg', '.png', '.svg'].include? File.extname(file)
      end

      def too_big?(width, height)
        width > 800 || height > 800
      end

      def graph?(file)
        file.include?('/graphs/')
      end

      def images
        @site.static_files.collect(&:path).select { |f| image?(f) }
      end

      def resizeable_images
        without_graphs = images.reject { |i| graph?(i) }
        with_sizes = without_graphs.map { |f| [f, FastImage.size(f)].flatten }
        with_sizes.select! { |f| too_big?(f[1], f[2]) }
        with_sizes.map do |f, w, h|
          dimensions = if w > h
                         '800x600'
                       else
                         '600x800'
                       end
          [f, dimensions]
        end
      end
    end
  end
end
