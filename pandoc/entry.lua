function EntryIterator ()
   local convertFilename = function (mdFile)
      return mdFile:match("^(.+).md$") .. ".html"
   end

   local splitString = function (inputstr)
      local t = {}
      for str in string.gmatch(inputstr, "([^%s]+)") do
	 table.insert(t, str)
      end
      return t
   end

   local output = splitString(pandoc.pipe("ls", { "../entries/" }, ""), " ")
   local max = #output

   local atIndex = function (i)
      if i >= max then
	 return nil
      else
	 return convertFilename(output[i])
      end
   end

   local public = {}

   public.index = 1

   public.advance = function ()
      if public.index == max then
	 return nil
      else
	 public.index = public.index + 1
	 return convertFilename(output[public.index - 1])
      end
   end

   public.next = function ()
      return atIndex(public.index + 1)
   end

   public.previous = function ()
      return atIndex(public.index - 1)
   end

   return public
end

function Paginate(m)
   local iter = EntryIterator()
   local thisOne = iter.advance()

   while thisOne do
      if thisOne == PANDOC_STATE.output_file then
	 break
      else
	 thisOne = iter.advance()
      end
   end

   if thisOne then
      local previousOne, nextOne = iter.previous(), iter.next()
      if previousOne then m.previous = previousOne end
      if nextOne then m.next = nextOne end
   end

   return m
end

function Meta (m)
   m.subtitle = m.title
   m.title = os.date("%A, %B %d %Y")
   return Paginate(m)
end
