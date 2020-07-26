# frozen_string_literal: true

require_relative 'spec_helper.rb'

class Dog
  include JekyllRecker::Logging
end

describe JekyllRecker::Logging do
  describe '.logger' do
    it 'should return logger' do
      expect(Dog.logger).to be_a(::Jekyll::LogAdapter)
    end
  end

  describe '#logger' do
    it 'should return logger' do
      expect(Dog.new.logger).to be_a(::Jekyll::LogAdapter)
    end
  end

  describe '#info' do
    it 'should pass through to Jekyll Logger info' do
      expect(::Jekyll.logger).to receive(:info).with('jekyll-recker:', 'testing!')
      Dog.new.info 'testing!'
    end
  end
end
