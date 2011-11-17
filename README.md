
**WARNING** INSIDE JOKES AHEAD
===============================

You'll need:
* App Engine Launcher, at least to run it locally
* Some questionable ability at Python, or Javascript (who **can't** do that?!)
* We actively use IRCDD (IRC Driven Development) - #forrst-chat on fail^H^H^H^Hfreenode

YES THERE IS AN API
====================
It's all JSON. ?callback works. Please don't fill it up with viagra spam or
things from other channels. 

POST /api/add
-------------------
Adds a funnay. 'quote' parameter is the funny. Please don't try to inject things
into the database :(

GET /api/list
-------------------
Downloads all the funny as a big JSON lump. May contain Liam Lynch, or not
actual funny. Does not download pictures of Yorick's cat. For that use:

    wget -nd -r -A jpg http://cat.yorickpeterse.com/images


AND FINALLY, A WORD FROM OUR SPONSOR
====================================

    <squeeks> code or gtfo

Anyone in channel gets collab if they actually contribute something. For
everything else, there's pull requests and patches.
