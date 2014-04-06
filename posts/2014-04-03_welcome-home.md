<!--Welcome Home | Blog by Alex Recker -->
<!--Wordpress has served me well, but my soul longs for the wilderness.  Retreat with me into the backwoods of the Internet.-->
<!--/welcome-home -->
<!--Welcome Home -->

![](http://www.agaritacreek.com/_Images/content/cabin-banner.jpg)

### My New Corner of the Internet
I'm sure you have noticed by now that things are a little different.  The awkward layout alone should be enought to tip you off to the fact that I've jumped ship to something a little more home brewed.

I present to you my pet project.  It's a ghetto little markdown driven CMS I've hacked together - and it's the most organic thing to leave my kitchen since that spinache calzone (*aside* - brown spinach is bad spinach.  There - I've spared you the night long retching I endured to learn the same lesson just last weekend).

The new diggs are part of an effor to be more minimal.  I'm kind of trying to do the transcendentalism thing, retreating to the Internet equivalent of a cabin in the woods with no electricity.

### Goodbye, Wordpress
I have been using Wordpress from the beginning, and my experience with it has been awesome.  Computer people love Wordpress because it is basically a one-click setup.  You really just dump a bunch of code into a folder, enter your database password, and you are good to go.

This is why Wordpress, in my book, still reigns supreme as the number one roll-a-new-website-for-your-uncle-over-the-weekend content management system.


<div class="row">
    <div class="col-md-4 col-md-offset-4">
        <div class="thumbnail">
            <img src="http://2.bp.blogspot.com/-0Xm6_Mhp16I/TcenBY6X2vI/AAAAAAAAAJg/tZuwBK1RiWE/s1600/pedo-smile.png" height=200>
            <div class="caption">
                <small>Not your shady uncle.  Don't get involved with his website.</small>
            </div>
        </div>
    </div>
</div>



But I was growing dissatisfied.  Wordpress is written entirely in PHP, so whenever a plugin broke, I basically just had to sit around and wait for it to get fixed.  I don't know PHP, and I certainly don't want to learn it by fixing Wordpress plugins.

Secondly, since it was written for non-programming folk, all the editing and site management is built right into the website.  It's convenient, but this puts a lot of pressure on your authentication for the site.  I was getting at least eight notifications on my phone daily alerting me that someone else was trying to crack my password.  I don't think anyone succeeded, because I don't remember a time where my blog looked like the *Amazon* of male enhancement pills.

Lastly, the database was really bumming me out.  It's really easy to set up, but a database is still a database.  They have to be rebooted, backed up, optimized, and occasionally they puke on your couch when they eat something bad out of the garbage (whatever the linux server equivalent of that is).


### For the Nerds
*Warning: incoming nerd talk*

Throughout all these shortcomings, the *Markdown* bandwagon started to look more and more appealing.

What is markdown?  It's the new craze, and it's hard to find a web developer these days who is not gushing over it.

Markdown is basically a text file that gets converted into a web page.  Through basic syntax rules, you can quickly create nice little formatting touches that would take a litle more time to do by hand (taking you out of the creative process of blogging - apparently).

For example, a markdown file would look something like this:
<hr>

	# Everybody Poops

	### Welcome to my weird poop blog.

	Hi there!  My name is Poop Smith.  Here are my hobbies:

	* Blogging
	* NASDAQ
	* Escrow

	> Toy Story 2 was ok.

	![](http://www.thepetcollective.tv/wp-content/uploads/2013/11/corgi-puppies.gif "Corgi Attack")


<hr>
Pretty simple to write.  Here is where the magic lies.  By the time it makes it to the web browser, it looks like this:

<hr>

# Everybody Poops

### Welcome to my weird poop blog.
Hi there!  My name is Poop Smith.  Here are my hobbies:

* Blogging
* NASDAQ
* Escrow

> Toy Story 2 was ok.

![](http://www.thepetcollective.tv/wp-content/uploads/2013/11/corgi-puppies.gif "Corgi Attack")

<hr>

So all of my posts are written in markdown now.  I don't have to back them up because they are just pushed to GitHub like a regular source file.  It's all [here](http://github.com/arecker/Blog).  If you are weird enough, I guess, you could deploy your very own version of my Blog on your own website and it would stay up to date.

The posts are written in Markdown, but the engine is built on a framework called *Django*.


<div class="row">
    <div class="col-md-4 col-md-offset-4">
        <div class="thumbnail">
            <img src="http://content.internetvideoarchive.com/content/photos/7244/645091_149.jpg" height="150">
            <div class="caption">
                <small>The <em>Django</em> Framework - Completely ungoogleable since 2012</small>
            </div>
        </div>
    </div>
</div>


My one beef with Django is that it is kind of bloaty.  It's meant for really big data entry websites.  My site is a hacked down version of Django.  I basically created a project, then moved everything to a single file appropriately named ```everything.py```.  I starved the project until it scratched my minimalist itch.


### Changelog
Ok ok ok - nerd talk over.  Here is what has changed about the site:

* **New Domain**: My blog is now located at [alexrecker.com](http://alexrecker.com).  But you knew that already.  You *are* reading this after all.  I will be setting up a site redirect from the old blog and porting over all the posts that weren't total garbage over to this one.  So you don't have to worry your pretty little head about fixing your bookmarks.
* **Facebook Comments Only**: I appreciate the comments - especially when they get zesty.  I just don't want to have to store them anymore.  Additionally, the old blog supported comments from Google+ too.  I accompany my decision to drop support for Google+ with a sincere apology to the only person who has ever used Google+ to comment on my Blog.  *Drew - I hope we can still be friends.*
* **RSS is not working (yet)**: RSS is not supported right now because of a small hang-up - and that is... I'm not smart enough right now to write a RSS generator.  I'm going to throw a few more monkeys and typewriters at it and see what kind of progress I can make.  Again, I offer my sincere apologies to my *one* RSS subscriber.  *Drew - it's not you... it's me.*


### Brave New World
That being said, welcome to my new site.  There's a lot of stuff still broken, but I'm going to do what I can.  We can take this journey together - blogger and reader marching lock-step, hand-in-hand, making our way through this brave new world of embarassing markdown parsing glitches and catastrophic runtime errors.

And please be noisy!  Beat the hell out of this thing.  You can't battle test a website without thowing some grenades.  Go ahead and load it up on your tablet, iPhone, Wii, and tamagotchi (if you still have one laying around).

Thanks for reading my test post.  You can go back to living your life now.
