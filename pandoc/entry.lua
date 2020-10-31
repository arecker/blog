function SplitString (input)
   local t = {}
   for str in string.gmatch(input, "([^%s]+)") do
      table.insert(t, str)
   end
   return t
end

function EntryFiles ()
   local output = pandoc.pipe("ls", { "../entries/" }, "")
   local entries = {}
   for _, md in pairs(SplitString(output)) do
      table.insert(entries, md:match("^(.+).md$") .. ".html")
   end
   return entries
end

function FindIndex (tbl, item)
   local indexes = {}

   for k, v in pairs(tbl) do
      indexes[v] = k
   end

   return indexes[item]
end

function Paginate (m)
   local pages = {}
   local entries = EntryFiles()
   local index = FindIndex(entries, PANDOC_STATE.output_file)
   
   if index > 1        then m.next = entries[index - 1] end
   if index < #entries then m.previous = entries[index + 1] end

   return m
end

function DateTitle (filename)
   local year, month, day = filename:match("^([0-9]+)-([0-9]+)-([0-9]+).html")
   local time = os.time {year=year, month=month, day=day}
   return os.date("%A, %B %d %Y", time)
end

function Meta (m)
   m.subtitle = m.title
   m.title = DateTitle(PANDOC_STATE.output_file)
   return Paginate(m)
end
