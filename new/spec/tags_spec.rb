# frozen_string_literal: true

require 'spec_helper'
describe Blog::Tags do
  describe 'Include' do
    it 'should just goddamn work' do
      TEMPLATE = <<~BOOYAH
        {% include figure.html filename='wip-blog.png' caption="Work in
        progress.  In lack of a more creative name, I'm just calling it 'blog'
        for now." %}
      BOOYAH

      actual = Liquid::Template.parse(TEMPLATE.strip).render.gsub(/\s+/, ' ')

      expected = <<~GROSS
        <figure>
          <a href="/images/wip-blog.png">
            <img alt="wip blog" src="/images/wip-blog.png" />
          </a>
          <figcaption>
            <p>Work in
              progress.  In lack of a more creative name, I'm just calling it 'blog'
              for now.</p>
          </figcaption>
        </figure>
      GROSS

      expect(actual).to eq(expected.gsub(/\s+/, ' '))
    end
  end
end
