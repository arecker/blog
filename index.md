---
slug: index.html
layout: home
active: index
---

{% assign latest = site.posts.first %}

## Today's Post

{% if latest.image %}
{% capture caption %}{{ latest.date | uyd_date }} | {{ latest.title }}{% endcapture %}
{% include figure.html url=latest.url filename=latest.image alt=latest.title caption=caption %}
{% else %}
[{{ caption }}]({{ latest.url }})
{% endif %}

## Entries

{% for post in site.posts %}
- {{ post.date | date: '%Y-%m-%d' }} - [{{ post.title }}]({{ post.url }})
{%- endfor %}

---

## Other Writings

- [Anxiety] - Hoping to inspire a new attitude toward medication and
  mental health, my wife bravely shares her personal journey of
  discovering her anxiety disorder.
- [Our New Sid Meier's Civilization Inspired Budget] - My wife and I
  were inspired by Sid Meier's Civilization to look at our finances
  differently. Here is our new system.  Featured in [lifehacker].
- [Clockwork Orange] - My wife and I review the movie _Clockwork
  Orange_.
- [Eyes Wide Shut] - My wife and I review the movie _Eyes Wide Shut_.
- [Full Metal Jacket] - My wife and I review the movie _Full Metal
  Jacket_.
- [Jane] - I interview my mother, Jane Recker.
- [Linux] - Let's talk about Linux.  Where did it come from?  What can
  it do for you?  How long does your beard need to grow before you can
  get it to work?
- [Noah] - A tender look back on the life of the best little brother
  I've ever had - my dog Noah.
- [Rockford] - Farewell, Rockford.  It was a pleasure being your
  citizen for two years.
- [San Francisco] - My company sent me on a trip to San Francisco.
- [Seinfeld] - The early seasons of Seinfeld - are these episodes
  evidence of a Sitcom finding its stride, or a prologue to the lives of
  the four people that surrendered to a life about nothing?
- [The Selenium Bus Pass] - A brief tutorial of my new favorite
  Selenium script.
- [My Corgi] - My wife takes the blogging soapbox from me this week as
  my very first guest writer.  She reflects on the top five lessons
  she has learned in owning a dog.
- [Uhh Yeah Dude] - A long overdue written tribute to my favorite
  podcast.

[Anxiety]: {% link old/anxiety.html %}
[Clockwork Orange]: {% link old/clockwork-orange.html %}
[Eyes Wide Shut]: {% link old/eyes-wide-shut.html %}
[Full Metal Jacket]: {% link old/full-metal-jacket.html %}
[Jane]: {% link old/jane.html %}
[Linux]: {% link old/linux.html %}
[My Corgi]: {% link old/the-top-5-ways-that-my-corgi-has-taught-me-how-to-be-a-better-person.html %}
[Noah]: {% link old/noah.html %}
[Our New Sid Meier's Civilization Inspired Budget]: {% link old/civ-budget.html %}
[Rockford]: {% link old/rockford.html %}
[San Francisco]: {% link old/san-francisco.html %}
[Seinfeld]: {% link old/seinfeld.html %}
[The Selenium Bus Pass]: {% link old/selenium-bus-pass.html %}
[Uhh Yeah Dude]: {% link old/uhh-yeah-dude.html %}
[lifehacker]: https://lifehacker.com/the-civilization-inspired-budget-gives-you-instant-feed-1742835068
