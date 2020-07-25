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
end
