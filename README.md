# **WARNING** INSIDE JOKES AHEAD

You'll need:

* App Engine Launcher, at least to run it locally
* Some questionable ability at Python, or Javascript (who **can't** do that?!)
* We actively use IRCDD (IRC Driven Development) - #forrst-chat on
  fail^H^H^H^Hfreenode

## TODO

* Get the existing funnay out of the bot
* Fix the front end to display, vote, etc
* Extend bot to post quotes to site
* Swallow sadness (LIKE A BOSS)
* Be less original than we already are

## YES THERE IS AN API

It's all JSON. ?callback works. Please don't fill it up with viagra spam or
things from other channels.

### POST /api/quote

Adds a funnay. `quote` parameter is the funny. Please don't try to inject things
into the database :(

### GET /api/quote

Downloads all the funny as a big JSON lump. May contain Liam Lynch, or not
actual funny. Does not download pictures of Yorick's cat. For that use:

    wget -nd -r -A jpg http://cat.yorickpeterse.com/images

Parameters:

* `limit` default 20, max 1000 for heaven's sake
* `offset` starting from zero
* `order_by` can be `created` or `votes` - default `created`
* `order` can be `ASC` or `DESC` - default `DESC`

### GET /api/quote/:id

Returns whatever hopeless quote was found. If it was found.

### POST /api/vote

Get your quote on top of the charts - supply a `quote_id` (that value should be
clear) and `vote` with `-1` or `1` as value to vote (once a day per quote).

## AND FINALLY, A WORD FROM OUR SPONSOR

    <squeeks> code or gtfo

Anyone in channel gets collab if they actually contribute something. For
everything else, there's pull requests and patches.
