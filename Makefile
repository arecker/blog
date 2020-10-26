$(wildcard "output/*.html"):
	mkdir -p $(@D)
	pandoc -s -o $@ $(addsuffix ".md", $(addprefix "entries/", $(notdir $(basename $@))))
