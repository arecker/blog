function RenderVersion()
   local major = pandoc.pipe("cat", { "../revision/major" }, ""):gsub("%s+", "")
   local minor = pandoc.pipe("cat", { "../revision/minor" }, ""):gsub("%s+", "")
   local patch = pandoc.pipe("cat", { "../revision/patch" }, ""):gsub("%s+", "")
   return "v" .. major .. "." .. minor .. "." .. patch
end

function Meta (m)
   m.revision = RenderVersion()
   return m
end
