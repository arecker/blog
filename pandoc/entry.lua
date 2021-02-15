function filenameToDate(filename)
   local _, _, y, m, d = string.find(filename, "www/(%d+)-(%d+)-(%d+).html")
   local asDate = os.time { day=d, month=m, year=y }
   return os.date("%A, %B %d %Y", asDate)
end

function Meta(m)
   m.description = m.title
   m.title = filenameToDate(PANDOC_STATE.output_file)
   return m
end
