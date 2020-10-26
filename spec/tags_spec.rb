# frozen_string_literal: true

require 'spec_helper'

describe Blog::Tags do
  describe 'Link' do
    it 'should link to the permalink if it is specified' do
      metadata = { 'permalink' => '/our-new-sid-meiers-civilization-inspired-budget/' }
      expect_any_instance_of(::Blog::Tags::Link).to receive(:metadata).and_return(metadata)
      actual = Liquid::Template.parse('{% link old/civ-budget.html %}').render.strip
      expect(actual).to eq('/our-new-sid-meiers-civilization-inspired-budget/')
    end

    it 'should return the webpath of the page by default' do
      metadata = { }
      expect_any_instance_of(::Blog::Tags::Link).to receive(:metadata).and_return(metadata)
      actual = Liquid::Template.parse('{% link archives.html %}').render.strip
      expect(actual).to eq('/archives.html')
    end
  end

  describe 'Image' do
    it 'should render the web path to the image' do
      actual = Liquid::Template.parse('{% image banners/thing.png %}').render.strip
      expect(actual).to eq '/images/banners/thing.png'
    end
  end
end
