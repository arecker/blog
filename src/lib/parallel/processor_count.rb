# frozen_string_literal: true

# https://github.com/grosser/parallel/blob/master/MIT-LICENSE.txt

# Copyright (C) 2013 Michael Grosser <michael@grosser.it>

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

require 'etc'

module Parallel
  # TODO: inline this method into parallel.rb and kill physical_processor_count in next major release
  module ProcessorCount
    # Number of processors seen by the OS, used for process scheduling
    def processor_count
      @processor_count ||= Integer(ENV['PARALLEL_PROCESSOR_COUNT'] || Etc.nprocessors)
    end

    # Number of physical processor cores on the current system.
    def physical_processor_count
      @physical_processor_count ||= begin
        ppc = case RbConfig::CONFIG["target_os"]
        when /darwin1/
          IO.popen("/usr/sbin/sysctl -n hw.physicalcpu").read.to_i
        when /linux/
          cores = {}  # unique physical ID / core ID combinations
          phy = 0
          IO.read("/proc/cpuinfo").scan(/^physical id.*|^core id.*/) do |ln|
            if ln.start_with?("physical")
              phy = ln[/\d+/]
            elsif ln.start_with?("core")
              cid = phy + ":" + ln[/\d+/]
              cores[cid] = true if not cores[cid]
            end
          end
          cores.count
        when /mswin|mingw/
          require 'win32ole'
          result_set = WIN32OLE.connect("winmgmts://").ExecQuery(
            "select NumberOfCores from Win32_Processor")
          result_set.to_enum.collect(&:NumberOfCores).reduce(:+)
        else
          processor_count
        end
        # fall back to logical count if physical info is invalid
        ppc > 0 ? ppc : processor_count
      end
    end
  end
end
