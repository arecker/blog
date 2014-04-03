* The Unibomber of Blogging | Blog by Alex Recker
* Wordpress is easy and effortless - which is why I am retreating into the back woods of the Internet.
* http://alexrecker.com/unibomber-blogging
* The Unibomber of Blogging

[go]

![](http://www.agaritacreek.com/_Images/content/cabin-banner.jpg)

### My New Corner of the Internet
If this site is giving off that crappy high school computer class project vibe, that's because it's totally homemade.

Yep - it's the latest home-made meal to leave my apartment kitchen (not counting the reheated - possibly
iradiated calzone that left me retching in my toilet last weekend).

I don't have a lot to bring you this week.  Truth be told, I have been so preoccupied with my new corner of the Internet
that I haven't gotten a chance to think about the usual stupid things I churn for you.

It's probably better that way.  I wouldn't want to test drive my baby with a post that I actually felt strongly about.

Here's what is changed about the site:

* **New Domain**: I'm now at [](http://alexrecker.com).  I will eventually be moving all my old posts over here and setting up a redirect...
So you don't have to worry your pretty little head about it.
* **Facebook-only comments**: Sorry brave Google+'ers.   I just can't keep up with all the crossfire.  Some discussion on Facebook, some on Wordpress,
Some on G+... I'm just moving it all over to Facebook.  Don't get me wrong, I love it when comments get spicy - I'm just tired of storing them on my database.
I'm going to let Facebook do what it does best (and I don't mean [virtual reality gaming](https://www.facebook.com/zuck/posts/10101319050523971))
* **RSS is broken**: For my single RSS reader out there (talking to you Drew), I regret to report that it's not working yet.
The one hangup is that I'm just not smart enought to figure out how to do that.  It will be back up soon, you.


### Goodbye, Wordpress
Since I started blogging last Summer, I had been using Wordpress.  Wordpress is fantastic.  Not only is it user friendly, but it is also server admin
friendly.  Web developers love Wordpress.  All you have to do to deploy it is basically dump out a bunch of code into a folder, type in your database password,
and off you go.  In my book, Wordpress is still the uncontested choice roll-a-website-for-your-uncle-over-the-weekend content management sytstem.

<br/>
<div class="row text-center">
<img src="http://2.bp.blogspot.com/-0Xm6_Mhp16I/TcenBY6X2vI/AAAAAAAAAJg/tZuwBK1RiWE/s1600/pedo-smile.png" height="200"/>
<br>
<small>Not your shady uncle.  Don't get involved with his website.</small>
<br/><br/>
</div>


But I chose to do the blogging equivalent of refuting electricity and retreating into a homemade cabin in the middle of the woods, where
I will pen my erratic manifesto - hence, the "Unibomber of Blogging".

### For the Nerds
So Worpdress was great, but my main concern was that it was getting a little bloaty.  After a few months of writing, I finally discovered what
kind of blogger I am.  I really just need a wall of text, links, basic headings, and a few of those *Cracked* style silly image/caption to break the tension.
I don't get a lot of comments, and those who usually do just comment through Facebook.

Plugins were breaking, taking a while to load, and I was getting an incessant number of break-in attempts.  And though databases are great, they are still databases.
They get big, they have to be backed up and restarted...

Looking at only my needs, I rolled my own Markdown driven CMS.  Nothing needs to be backed up because it's all deployed through git.  Every post and page in its
Markdown format is just another file in the source code.

The site is a hacked down monstrocity that started with django.  I wrote a project, deleted the built-in database backend, then just combined the entire project
into one file appropriately named "everything.py".  It's not as grand as it sounds - even the markdown parsing barely exceeded a dozen lines of code thanks to the
```BeautifulSoup``` and ```Markdown2``` libraries.

If any of you nerds are interested, all the code is [out on GitHub](http://github.com/arecker/Blog).  I guess if you are a huge weirdo, you could technically even
deploy your own version of my blog.

### Welcome Home
That being said, welcome to my new site.  There's a lot of stuff still broken, but that doesn't make it less mine.
We'll take this journey together - blogger and reader lock-step, hand-in-hand, making our way through this brave new world
of bugs and web errors.

Please be noisy!  Beat the hell out of this thing.  Go ahead an load it up on your tablets, iPhones, and tamagotchis.  Feel free to lampoon my sense of space, color, 
and spelling.  I will be making improvements over time.

Thanks for reading my test post.  You can go back to your lives now.
