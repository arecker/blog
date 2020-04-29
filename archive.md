---
layout: page
title: Archive
description: Archive of journal entries
slug: archive.html
permalink: archive.html
active: archive
---

## Stats

Some interesting daily journaling statistics.

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

## Journal Entries

The chronological list of daily journal entries.

<ul class="unstyled">
  {%- for post in site.posts %}
  {%- capture datestring %}{{ post.date | date: '%Y-%m-%d' }}{% endcapture %}
  <li>{{ datestring }} - <a href="{{ post.url }}">{{ post.title }}</a></li>
  {%- endfor %}
</ul>

## Other Writings

Miscellaneous blog posts of old!

---

### [Anxiety]

Hoping to inspire a new attitude toward medication and mental health,
my wife bravely shares her personal journey of discovering her anxiety
disorder.

[Anxiety]: {% link old/anxiety.html %}

---

### [Our New Sid Meier's Civilization Inspired Budget]

My wife and I were inspired by Sid Meier's Civilization to look at our
finances differently. Here is our new system.

Featured in [lifehacker].

[Our New Sid Meier's Civilization Inspired Budget]: {% link old/civ-budget.html %}
[lifehacker]: https://lifehacker.com/the-civilization-inspired-budget-gives-you-instant-feed-1742835068

---

### [Clockwork Orange]

My wife and I review the movie _Clockwork Orange_.

[Clockwork Orange]: {% link old/clockwork-orange.html %}

---

### [Eyes Wide Shut]

My wife and I review the movie _Eyes Wide Shut_.

[Eyes Wide Shut]: {% link old/eyes-wide-shut.html %}

---

### [Full Metal Jacket]

My wife and I review the movie _Full Metal Jacket_.

[Full Metal Jacket]: {% link old/full-metal-jacket.html %}

---

### [Jane]

I interview my mother, Jane Recker.

[Jane]: {% link old/jane.html %}

---

### [Linux]

Let's talk about Linux.  Where did it come from?  What can it do for
you?  How long does your beard need to grow before you can get it to
work?

[Linux]: {% link old/linux.html %}

---

### [Noah]

A tender look back on the life of the best little brother I've ever
had - my dog Noah.

[Noah]: {% link old/noah.html %}

---

### [Rockford]

Farewell, Rockford.  It was a pleasure being your citizen for two
years.

[Rockford]: {% link old/rockford.html %}

---

### [San Francisco]

My company sent me on a trip to San Francisco.

[San Francisco]: {% link old/san-francisco.html %}

---

### [Seinfeld]

The early seasons of Seinfeld - are these episodes evidence of a
Sitcom finding its stride, or a prologue to the lives of the four
people that surrendered to a life about nothing?

[Seinfeld]: {% link old/seinfeld.html %}

---

### [The Selenium Bus Pass]

A brief tutorial of my new favorite Selenium script.

[The Selenium Bus Pass]: {% link old/selenium-bus-pass.html %}

---

### [My Corgi]

My wife takes the blogging soapbox from me this week as my very first
guest writer.  She reflects on the top five lessons she has learned in
owning a dog.

[My Corgi]: {% link old/the-top-5-ways-that-my-corgi-has-taught-me-how-to-be-a-better-person.html %}

---

### [Uhh Yeah Dude]

A long overdue written tribute to my favorite podcast.

[Uhh Yeah Dude]: {% link old/uhh-yeah-dude.html %}
