function Meta(m)
   m.subtitle = m.title
   m.date = os.date("%B %e, %Y")
   m.title = os.date("%A, %B %d %Y")
   return m
end
