# frozen_string_literal: true

require 'spec_helper.rb'

describe JekyllRecker::Tags::Version do
  it 'should render the gem version' do
    rendered = Liquid::Template.parse('{% version %}').render
    expect(rendered).to eq "v#{JekyllRecker::VERSION}"
  end
end
