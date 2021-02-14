function Meta(m)
   m.description = m.title
   m.title = os.date("%A, %B %d %Y")
   return m
end
