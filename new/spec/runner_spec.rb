# frozen_string_literal: true

require 'spec_helper'

describe Blog::Runner do
  describe '#subcommand' do
    it 'should return the subcommand' do
      expect(Blog::Runner.new(['build']).subcommand).to eq('build')
    end

    it 'should return nil if nothing was passed' do
      expect(Blog::Runner.new([]).subcommand).to eq(nil)
    end
  end

  describe '#verbose?' do
    it 'should true if -v was passed first' do
      expect(Blog::Runner.new(['-v', 'build']).verbose?).to eq true
    end

    it 'should true if -v or --verbose was passed last' do
      expect(Blog::Runner.new(['build', '-v']).verbose?).to eq true
      expect(Blog::Runner.new(['build', '--verbose']).verbose?).to eq true
    end

    it 'should default to false' do
      expect(Blog::Runner.new(['build']).verbose?).to eq false
    end
  end

  describe '#valid?' do
    it 'should return true when a valid subcommand is used' do
      expect(Blog::Runner.new(['build']).valid?).to eq true
    end

    it 'should return false when an invalid subcommand is used' do
      expect(Blog::Runner.new(['boop']).valid?).to eq false
    end

    it 'should return false no subcommand is used' do
      expect(Blog::Runner.new([]).valid?).to eq false
    end
  end
end
