# frozen_string_literal: true

require_relative 'spec_helper.rb'

class Dog
  include Jekyll::Recker::DescendantsMixin
  include Jekyll::Recker::LoggingMixin
end

class PembrokeWelshCorgi < Dog; end
class CardiganWelshCorgi < Dog; end
class GoldenRetriever < Dog; end

describe Jekyll::Recker::DescendantsMixin do
  describe '.descendants' do
    it 'should iterate over each child class' do
      expected = [PembrokeWelshCorgi, CardiganWelshCorgi, GoldenRetriever]
      expect(Dog.descendants).to match_array(expected)
    end
  end
end

describe Jekyll::Recker::LoggingMixin do
  describe '.logger' do
    it 'should return logger' do
      expect(Dog.logger).to equal(Jekyll::Recker.logger)
    end
  end

  describe '#logger' do
    it 'should return logger' do
      expect(Dog.new.logger).to equal(Jekyll::Recker.logger)
    end
  end
end
