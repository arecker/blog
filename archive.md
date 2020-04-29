---
layout: page
title: Archive
description: Archive of journal entries
slug: archive.html
permalink: archive.html
active: archive
---

## Stats

```yaml
words:
  total: {{ site.data.stats.words.total }} # total number of words
  average: {{ site.data.stats.words.average }} # average words per entry

entries:
  total: {{ site.data.stats.posts }} # total number of entries
  consecutive:
    days: {{ site.data.stats.days.days }} # number of consecutive, daily entries
    start: {{ site.data.stats.days.start }} # first day of streak
    end: {{ site.data.stats.days.end }} # last day of streak
```

## Posts

<ul class="unstyled">
  {%- for post in site.posts %}
  {%- capture datestring %}{{ post.date | date: '%Y-%m-%d' }}{% endcapture %}
  <li>{{ datestring }} - <a href="{{ post.url }}">{{ post.title }}</a></li>
  {%- endfor %}
</ul>
