<!--Obsessed with Computers | Blog by Alex Recker-->
<!--A reflection on how four different, admittedly embarrassing, pursuits derailed my education and got me a job in computers.-->
<!--/obsessed-with-computers-->
<!--Obsessed with Computers-->

I just got home from work, where I write software. I walked in, stuffed a chicken sandwich in my mouth, and headed straight upstairs to work on… well… a different computer. While coming home from working on a computer all day to relax on a computer all night may sound ridiculous to some, it got me thinking about where this all began. When did computers begin to be such a big thing for me?

Because it’s such a long story, I’ve only told a few people, and I usually do it in snippets. I decided to get it all down on e-paper. Lists are much easier to read then enormous walls of unbroken text. In this spirit, I’ve organized the story around four trivial, admittedly embarrassing motivations that ultimately turned me into a pretentious neckbearded unix-thumper.

<br>

### 1. A Pretty Desktop
<div class="row">
    <div class="col-centered col-lg-6">
        <div class="thumbnail">
            <img src="/static/img/geektool.png">
            <div class="caption">
                <small></small>
            </div>
        </div>
    </div>
</div>

The last time I remember being a normal person was January of 2012. I had a Macbook Pro loaded with all kinds of pedestrian tools. I looked like I new what I was doing most of the time, but I knew just enough to get by. I could right click, run my Time Machine backups, and throw together a pretty decent spreadsheet with Excel. I would say that I could also manage an iTunes library, but earlier that semester I corrupted my iTunes library, erasing all my music. The way I remember it, I was “cleaning up” files I didn’t use. These files happened to be metadata used by iTunes to organize my music. Let’s face it… I was a bafoon.

I was still always into the asthetics of my computer. I didn’t like how my Macbook looked like everyone else’s, so I was always looking for ways to get ahead of the pedestrian masses. These were very small changes, like the black menu bar pictured below (which is achieved with this addon, by the way).

<div class="row">
    <div class="col-centered col-lg-6">
        <div class="thumbnail">
            <img src="/static/img/blackmenubar.png">
            <div class="caption">
                <small>Lookout, everyone. We have a real genius on our hands.</small>
            </div>
        </div>
    </div>
</div>

In my quest for the perfect, pretty desktop, I discovered something called Geektool. Geektool was a little application that displayed cool info on your desktop – anything from the time, date, IP addressed, calendars… even totally random numbers (which I was especially fond of). I downloaded Geektool expecting to prime a hayday of computer primping, only to discover something awful: it required programming.

I was furious. Who would have thought you would need to program to make your desktop look like you know how to program? Ridiculous.

I persevered anyway. After all, it was really important that I get random numbers on my desktop. I managed to just blindly copy and paste the commands I needed. Here is some of the work I conjured up from this scrappy method. This was a real blast from the past finding these… 

<div class="row">
    <div class="col-centered col-lg-6">
        <div class="thumbnail">
            <img src="/static/img/attempt1.png">
            <div class="caption">
            	<p>Attempt 1</p>
                <small>That’s right. I put all those words there myself.</small>
            </div>
        </div>
    </div>
</div>
<div class="row">
    <div class="col-centered col-lg-6">
        <div class="thumbnail">
            <img src="/static/img/attempt2.png">
            <div class="caption">
            	<p>Attempt 2</p>
                <small>More words… just avante-garde.</small>
            </div>
        </div>
    </div>
</div>

At some point, I got tired of googling these “scripts” and decided to pull out some wires myself. I was a little bored with the same old thing. Some very light research told me all of these “geeklets” were using a language called “Bash”. Furthermore, this wasn’t just a desktop customizing tool (believe-it-or-not). This was actually the default language loaded in the system terminal – or as I knew it, Terminal.app.

<br>

### 2. Night Class Boredom
I first opened up the Macbook Terminal in the back row of a night class. I would have never even bothered if there was internet access (or if I had remembered to load more comic books on my thumb drive). I was greeted by a blank white box.

<div class="row">
    <div class="col-centered col-lg-6">
        <div class="thumbnail">
            <img src="/static/img/macterminal.jpg">
            <div class="caption">
                <small>I wish I could tell you this was my “red pill / blue pill” moment, but I was already bored at this point.</small>
            </div>
        </div>
    </div>
</div>

I would have closed it if we were talking about something interesting, but “feminism in Israel” wasn’t cutting it for me. I started hammering away at the keyboard.

	hello
	bash: command not found
	program
	bash: command not found
	hack
	bash: seriously?

I tried every command I remember seeing from The Matrix, but it wasn’t until I entered a simple “help” that I was given something different to read from the command line. Almost rewarding me for my humility, I was given a full scrollable page of information. Somewhere in the manual page, I read that you could tap the TAB key to display commands.

I double tapped the key, and it did indeed display possible commands I could type – all 3000 of them. In perfectly moronic fashion, I tried every single command. They were in alphabetical order, and most of them didn’t do anything. But I was delighted to recognize a couple of commands from my Geektool experience. I further read that every command had its own manual page, accessible by “man [command]“. Holy canole – it was like Christmas… you know… for someone stuck in a night class without Internet.

Next came my first program. This masterpiece I had in mind was a little doozy that could open my mail app, my web browser, and say “Hello Alex”. Here is what it looked like:

	open /Applications/Safari.app
	open /Applications/Mail.app
	say "Hello, Alex"

A real work of genius, isn’t it? This dizzying algorithm took me three hours working in the science center. But that little greeting at the end of my program was the sweetest thing I have ever heard.

Shortly after, I contracted mono just before the last leg of the semester. My finals week consisted of whimpering in bed, sleeping for 13 hours a night, driving to school to bomb whatever final I was supposed to take, and returning home. During this time, my choice comfort was lying in bed scrolling through the manual pages I discovered during night class. I wasn’t even particularly thrilled with this activity, but I enjoyed the simple act of skimming a bunch of code documentation. It was just something to take my mind of the headaches and nausea during my bout with “kissing disease” (although I am pretty sure I got my case from eating pizza crust out of a garbage can).

<br>
### 3. Unixporn
<div class="row">
    <div class="col-centered col-lg-6">
        <div class="thumbnail">
            <img src="/static/img/unixporn.jpg">
            <div class="caption">
                <small></small>
            </div>
        </div>
    </div>
</div>

Previously, I was really into desktop customization. When I made something I liked, I submitted it to the /r/desktops subreddit and wait for my blue ribbons. While on reddit, I found a different subreddit for the same purpose, only these desktops looked a little more hardcore. The group was called [unixporn](http://reddit.com/r/unixporn) (pardon the crass comparison). It was a place where programmers posted screenshots of their workstations. Looking for the approval of these mysterious people, I started to post desktops that focused on my terminal a little more. I wanted to make it look like I actually did what they did. Here are some more of my entries – all part of a more mature motif.

<div class="row">
    <div class="col-centered col-lg-6">
        <div class="thumbnail">
            <img src="/static/img/attempt3.png">
            <div class="caption">
            	<p>Attempt 3</p>
            </div>
        </div>
    </div>
</div>
<div class="row">
    <div class="col-centered col-lg-6">
        <div class="thumbnail">
            <img src="/static/img/attempt4.png">
            <div class="caption">
            	<p>Attempt 4</p>
            </div>
        </div>
    </div>
</div><div class="row">
    <div class="col-centered col-lg-6">
        <div class="thumbnail">
            <img src="/static/img/attempt5.png">
            <div class="caption">
            	<p>Attempt 5</p>
            </div>
        </div>
    </div>
</div>
<div class="row">
    <div class="col-centered col-lg-6">
        <div class="thumbnail">
            <img src="/static/img/attempt6.png">
            <div class="caption">
            	<p>Attempt 6</p>
                <small></small>
            </div>
        </div>
    </div>
</div>

That last one I actually still kind of like. That’s probably the best it has ever looked. But my peer-pressure overlords weren’t so impressed. Every post received the same criticism. Another Mac user. Another dumb Mac user.

I was really frustrated. What was wrong with my computer? What couldn’t I do that they could? After crawling around on the bottom of forums and bothering enough elite users, I learned that they used something called “Linux”. I had never heard of it before, and I had no idea where to start. Thinking it was just another customization tool I could install on my Macbook, I consulted an apple support group. They snidely informed me that Linux was not an application – it was a whole different operating system. If I were to switch to the cool system that the programmers were using, I could not keep iTunes, Word, or anything that made up my comfort zone at the time. I regret that I couldn’t find the original thread – because it’s hilarious. I type something along the lines of,

> It’s probably not worth it to learn a whole new set of apps. I don’t think I could live without iTunes. I think I’ll just stick with OS X.

Anyone who knows me know that was the lie of the century. That summer, I gutted an old Dell Dimension PC and set it up on my desk. I wanted to be like the hackers on the subreddit I worshiped, so I started with the most difficult version of Linux I could find: Arch Linux. This is what my desk looked like all summer.

<div class="row">
    <div class="col-centered col-lg-6">
        <div class="thumbnail">
            <img src="/static/img/desk.jpg">
            <div class="caption">
                <small></small>
            </div>
        </div>
    </div>
</div>

That summer, my daily routine was a Starbucks shift from 3:00 pm to 1:30 am, then “hacking” until about 5:00 am. I usually went to sleep when the sun started to go up. Unhealthy, yes, but this was where I put in all the honest work I was masquerading under all this time. By the time the summer was over, I was fully committed to Linux. The system that formerly was a hell of tinkering and petty research slowly became the freedom I was craving. Strangely, I grew addicted to the constant breaking and fixing and breaking and fixing… it was an endless cycle that made me feel more and more powerful every lap around the command line

You could imagine my satisfaction upon learning that I really was a hacker. A hacker didn’t have to brute into private servers, decrypt hashes, or even know what they are doing. A hacker is something who works on a computer obsessively. In the documentary Hackers: Wizards of the Electronic Age, several patriarchs of the hacking culture describe the role of a hacker simply as someone who works obsessively on making something better (oftentimes never stopping to completely understand everything that is happening). Now that I think of it, it may not even have that much to do with the computer itself. I imagine you can be a hacker at anything, really… so long as the spirit is to keep moving forward (the spirit that often carries these type of people into less comfortable hours of the night).

<br>
<iframe width="420" height="315" src="//www.youtube.com/embed/bl_1OybdteY" frameborder="0" allowfullscreen></iframe><br>

### 4. Minecraft
<div class="row">
    <div class="col-centered col-lg-6">
        <div class="thumbnail">
            <img src="/static/img/minecraftbanner.jpg">
            <div class="caption">
                <small></small>
            </div>
        </div>
    </div>
</div>

The last push into a full blown obsession with technology was Minecraft. It wasn’t exactly the game itself that pushed me over the edge, but the game server. With the simple goal of getting people to play on the same world remotely, I was invigorated with a sense of purpose. What was a simple LAN server, turned into a fixed address off campus, which later turned into a domain redirection… Minecraft was the gateway drug into IT. And I couldn’t recommend it more highly. What a ride. What. A. Ride.

And I know for a fact that Minecraft helped get me the job I have today. Later talking to my manger, I was shocked to hear that he was mostly uninterested with my education and my references. What “gave me a shot” evidently was a minor footnote that mentioned my involvement with a java-based game server. There you go – never underestimate how well your hobbies can communicate what really motivates you. What seemed like a warmup question answered with a footnote on my resume really represented a desire to learn and be useful. Thank you, video games.

So that’s the whole story, along with my 4-piece secret recipe for success. I guess the moral of this story is that obsessions aren’t always to be feared. They can be dangerous if they get out of hand, but they are always valuable in what they reveal about your motivation. This is why I have always been an advocate of working a late night every now and then. While some will scold me for not getting enough sleep, I am just grateful there are still things that, when I think about them, make me too excited to fall asleep.

Don’t get me wrong – I’m by no measure an expert in technology yet. I just better understand where I am going.

Thanks for reading. If it was uplifting or it related to you in anyway, please let me know.

Keep “hacking”,

Alex
