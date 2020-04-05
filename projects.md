---
layout: page
title: Projects
description: Things I've made
permalink: projects.html
slug: projects.html
active: projects
---

{% for project in site.data.projects %}
## [{{ project.name }}]

{{ project.description }}

![{{ project.name }} Image]
{% endfor %}

{% for project in site.data.projects %}
[{{ project.name }} Image]: {{ site.baseurl }}assets/images/{{ project.image }}
[{{ project.name }}]: {{ project.link }}
{% endfor %}
