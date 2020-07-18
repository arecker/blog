# frozen_string_literal: true

require_relative 'spec_helper.rb'

class Dog
  include JekyllRecker::Mixins::Logging
end

describe JekyllRecker::Mixins::Logging do
  describe '.logger' do
    it 'should return logger' do
      expect(Dog.logger).to be_a(Logger)
    end
  end

  describe '#logger' do
    it 'should return logger' do
      expect(Dog.new.logger).to be_a(Logger)
    end
  end
end
