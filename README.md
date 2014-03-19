[OPENSPACE WILDERNESS] v1.0
Andrew T. Lyman 2014 - andrewtlyman@gmail.com

[made with a comission from turbulence.org]


----------------------------------------------------------[welcome]

Hello visitor, and welcome to the [openspace] wilderness - a preserve of virtual space encompassing [68 square MB] of abandoned social-network profiles as well a dynamic population of wildlife and visitors. The abandoned profiles which account for the bulk of the park's area have been created by gathering the posts of long-neglected blogs. The names have been changed to protect the innocent, however the content of the abandoned profiles in the park is directly pulled from the posts of the recovered blogs. Visitors to the park are welcome to view, [tag], like - [+], and [comment] the forgotten posts and profiles they encounter while exploring the site on - [@] or off - [–] [trails].

Additionally, Visitors may opt to experience the park as either a [predator] or a [forager] which entreats them to certain abilities and actions - [predators] may [eat] prey they encounter, whereas [foragers] may [graze] post content. As one of these active profiles, your [energy] will be depleted and you may eventually die of starvation if you don't consume a foodsource while you explore the park. As profiles die, the site will become littered with the virtual bodies of the dead explorers, opportunists, and colonizers that have wandered into its bounds.

The wilderness is a finite and consumable resource. You are among the first human eyes to gaze upon much of this content in many years. Your actions effect the whole of the park and it may be preserved and mapped or overrun and overgrazed based on the behavior of those who choose to visit.

------------[key]

[@] - select trail
[-] - deselect trail
[f] - add profile as friend
[+] - add interest
[tag] - add tag(s)
[comment] - add comment

-----[definitions]

[trail] - an explorable area of the park linked by a [tag]
[predator] - consumes active profiles for energy
[forager] - grazes the content of posts for energy
[energy] - the consumable resource of active profiles


--------------------------------[instructions]

Welcome, Visitor, to the [openspace] wilderness. This site is a virtual nature preserve for a small section of the abandoned internet. This is a quick primer to navigating the wilderness so that you may be well prepared to explore the site happily and safely on your own.

To start, no one is required to create an account in the [ openspace ] wilderness. Upon entry each guest is admitted as an [Anonymous Visitor]. As a visitor most of the functionality of the site is already available to you. Your will notice your [session display] on the top left of the page. You may view your session's [profile] at any time by simply clicking your icon. Underneath your profile is your [session activity]. This is simply a small feed of your most recent posts and actions. On the top right are your [navigation options]. You may simply move forward - [next], back - [previous], or jump to a [random] profile. Profiles comprise the explorable space of the site. Each profile has a host of attributes and there are a number of ways that you may interact with each profiles such as: liking them - [+], making friends - [f], or [commenting]. In addition to these you may also [tag] a profile or post. Tagging objects in the wilderness creates [trails] which allow you and other visitors to navigate along paths of like profiles and posts. Note that if you tag a post, its profile will also inherit the tag. Hopping on - [@] and off - [–] trails is simple, and the trails page displays a list of all the available trails and the profiles along each one. You may also use the [search] button at the top to discover posts containing words or phrases of your choosing.

Another aspect to the [openspace] wilderness is its dynamic population. You will notice under your session icon a tab that says [select species]. Clicking this will drop-down the two available active species options: [predator] and [forager]. Both of these active species can engage in any of the activities a visitor can, however they each posses special actions that may be used while exploring the park. If you choose to create one of the active profiles you will be taken to the page of your new session profile. You session display will look similar, however you will now notice a large number that says [energy] - this is your active profile's life-force. Now as you navigate the park your energy will be depleted. Each active species must consume a foodsource as they move about or they will eventually [die of starvation]. [Predators] consume other active profiles for sustenance and [foragers] graze the content of posts. If you select a predator, you may eventually happen upon some [prey]. You will notice a red [eat] button pops up on a consumable profile. Active profiles are generally invisible to regular visitors, but eaten prey will now be left to rot out in the open, and other guests may happen upon it as they explore.

If you select a [forager] you will see a green [graze] button on profiles and posts that you are able to consume. You will receive less nutrients the more foragers there are currently living in the site. By grazing you remove the actual content of posts and the bites you take will be re-posted on the wall of your profile. Grazing is an irreversible process that affects the whole system. Your actions have consequences that impact the content and structure of the park.

To this effect, there is a [protected] tag available that will prevent a post being grazed by a forager. Use it sparingly to mark some of the truly unique discoveries you make as you wander.

There are a number of other things to discover, but, most of all, you should enjoy exploring the sheer unknown and undocumented breadth of the park itself. You should be well prepared to go exploring on your own now. Have fun, be safe, and ask the [Ranger] if you have any questions. Thank you for visitng the [openspace] wilderness.


-----------------------------------[abstract]

The boom and bust cycle of global capital creates many orphans and islands. A concrete Detroit or Pripyat - when the industry folds, the wells run dry, the air becomes poison, or the focus simply shifts, is left to sit empty and forlorn as a young and haunted human wilderness.

This same boom and bust cycle is active in the virtual cities of the world - the tone shifts, the shark is jumped, the money evaporates, and the people move on. What sorts of shells are left behind on an abandoned internet? Unnumbered and innumerable sites, profiles, comments, and media - remote, forgotten, and estranged from their architects - sit silent and random. Since the year 2000, the number of internet users has grown over 7 times (from 361 to 2,749 million). This rapid/rabid rate of expansion necessarily leaves many ghost-towns in its drag. Whereas the empty places of the concrete world may be re-wilded and re-purposed, what utility or ability is there for scavengers, foragers, and opportunists to re-colonize and re-inhabit the abandoned sites of the virtual wild?


---------------------------------------[vernacular]

The [openspace] wilderness was created during the Fall / Winter of 2013 / 2014 on a commission for [turbulence.org].

It is built on [django v1.5] utilizing: python, jquery, html, and css. Every line of program code was written from scratch by me, building upon the indispensable, [django-skel]. In addition to the primary site there is a mutant host of helper scripts and utility functions for retrieving, indexing, and logging the recovered blogs and processing images.

Assembling the whole collection was possible due to a feature of [Blogger] blogs created prior to 1999 wherein each blog was assigned a 9-digit incremental ID that can be used to query the blog via the google Blogger API and retrieve specified elements. After 1999 the blogs were created with a randomized 15-digit ID and are therefore not searchable in a straightforward manner. With a crawler script written to provide some light filtering and logging, I simply selected various insert points and let it go off collecting. I have, for-instance, deliberately chosen to filter non-english blogs (mostly), and blogs that contain less than 2 posts. You are only able to retrieve the 5 most recent posts querying a blog in this manner, so many of the blogs collected in the wilderness have or may have had many many more posts than are present here. There are, however, thousands upon millions that only have some version of: "my first blog post!" and were subsequently forgotten. Also of amusing note are the many many blogs which appear to spend their whole run apologizing for not updating - posts getting incrementally wider and wider apart until finally hitting some threshold and never logging-in again. This has been a fascinating project to build and I am sitting here, just prior to launch, wondering what will become of this wilderness once it is released into the wild. Funny that the contents of this site are currently as unknown to me as to anyone else.

Always happy to answer any questions you may have. Cheers,
- Andy [march 18.2014]
