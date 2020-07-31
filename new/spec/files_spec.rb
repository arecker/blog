# frozen_string_literal: true

require 'spec_helper'

describe Blog::Files do
  let(:k) { Class.new { extend ::Blog::Files } }
  let(:root) { File.expand_path(File.join(File.dirname(__FILE__), '../')) }

  describe '#path' do
    it 'should join paths to the repo root' do
      expect(k.path('pages', 'index.html')).to eq(File.join(root, 'pages/index.html'))
    end

    it 'should join directories to the repo root' do
      expect(k.path('site')).to eq(File.join(root, 'site'))
    end
  end

  describe '#relpath' do
    it 'should calculate a relative path from an absolulte path' do
      expected = 'old/index.html'
      actual = k.relpath('/code/repo/', '/code/repo/old/index.html')
      expect(actual).to eq(expected)
    end
  end

  describe '#webpath' do
    it 'should add a / to the beginning of the path' do
      expect(k.webpath(k.path('assets/site.css'))).to eq('/assets/site.css')
    end

    it 'should subtract special dirs from the path' do
      expect(k.webpath(k.path('pages/index.html'))).to eq('/index.html')
    end
  end
end
