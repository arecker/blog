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

    it 'should resolve bare variables' do
      template = <<~BOOYAH
        {% include figure.html filename=my_filename %}
      BOOYAH

      actual = Liquid::Template.parse(template.strip).render({ 'my_filename' => 'test.png' }).gsub(/\s+/, ' ')

      expected = <<~GROSS
        <figure>
          <a href="/images/test.png">
            <img alt="test" src="/images/test.png" />
          </a>
        </figure>
      GROSS

      expect(actual).to eq(expected.gsub(/\s+/, ' '))
    end

    it 'should resolve nested variables' do
      template = <<~BOOYAH
        {% include figure.html filename=latest.image %}
      BOOYAH

      latest = double('page')
      expect(latest).to receive(:to_liquid).and_return({'image' => 'latest-image.png' })
      
      actual = Liquid::Template.parse(template.strip).render({ 'latest' => latest }).gsub(/\s+/, ' ')

      expected = <<~GROSS
        <figure>
          <a href="/images/latest-image.png">
            <img alt="latest image" src="/images/latest-image.png" />
          </a>
        </figure>
      GROSS

      expect(actual).to eq(expected.gsub(/\s+/, ' '))
    end
  end
end
