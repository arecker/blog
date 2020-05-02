---
slug: index.html
layout: home
active: index
---

<figure class="float-left hide-on-mobile">
  <img src="{{ site.baseurl }}assets/images/me.jpg" alt="I'm Alex Recker">
</figure>

## Hi!  I'm Alex Recker

Welcome to my online public journal.  I write **1000 words** every
morning, topics ranging from computers, cooking, raising kids, living
in Madison, being Dutch, and everything else I come across in my daily
life.  I love chatting with people, especially over email.

Do statistics get you going?  I track my word count and consecutive
daily entries over on the [archive] page.  I'm particularly proud of
that one.

Like to read code?  Check out my jekyll plugin [jekyll-recker].  It's
got twitter and slack integration, custom generators, and a bunch of
other custom crap that - let's be honest - are probably only useful to
me.  Other projects are featured on my [projects] page.

Thanks for stopping by, and I hope to see you tomorrow morning!

## Recent Entries

<ul class="unstyled">
  {%- for post in site.posts limit:10 %}
  <li>{{ post.date | date: '%Y-%m-%d' }} - <a href="{{ post.url }}">{{ post.title }}</a></li>
  {%- endfor %}
</ul>

[jekyll-recker]: https://github.com/arecker/jekyll-recker/
[projects]: {% link projects.md %}
[archive]: {% link archive.md %}
