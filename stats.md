---
title: Stats
description: Some interesting writing statistics
layout: page
active: stats
permalink: /stats.html
---

``` text
WORDCOUNT
=========
total: {{ site.data.stats.words.total | pretty }}
average: {{ site.data.stats.words.average | pretty }}

ENTRIES
=======
total: {{ site.data.stats.posts | pretty }}
consecutive: {{ site.data.stats.days.days | pretty }}

DATA
====
characters: {{ site.data.stats.memory.chars | pretty }}
spaces: {{ site.data.stats.memory.spaces | pretty }}
total size: {{ site.data.stats.memory.size }} mb

BAD WORDS
=========
{%- for swear in site.data.stats.swears %}
{{ swear.first }}: {{ swear.last | pretty }}
{%- endfor %}
```
