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

BAD WORDS
=========
{%- for swear in site.data.stats.swears %}
{{ swear.first }}: {{ swear.last | pretty }}
{%- endfor %}
```
