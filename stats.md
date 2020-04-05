---
title: Stats
layout: page
description: Some interesting writing statistics
permalink: stats.html
slug: stats.html
active: stats
---

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
