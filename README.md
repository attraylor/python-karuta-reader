# python-karuta-reader

App for reading karuta cards to you.

My system specs:

* Mac OSX 10.15.5
* python 3.7.7

usage: `python src/read.py --config_file link/to/config`

Here are some things you should do before messing around with this:

* Have all 100 cards separated into their own .mp4 files. The file format isn't 100% neccessary, but it's what I could run with `afplay`. You can find the files [here](http://naniwazu.la.coocan.jp/download/naniwazu_h.zip) or get your own somehow. Install `ffmpeg` (found [here](https://ffmpeg.org/download.html)) and use `utils/ogg_to_mp4.py` to convert to .mp4 files. You can also edit `play_sound()` to run your own files.

* Make your own config. Configs are in the format `field \t value \n`. A couple of example configs are in the `config/` directory and you can play around with them. You can also just get up and go by setting `poems_dir` to be the filepath where your mp4s are in `config/justplay.txt`.

### config arguments

**Important Arguments**

```
poems_dir: where the .mp4 files are. you won't get poems read to you otherwise.

wait_for_user_input: defaults to True. the system will wait for your input in between each card to give you time to reset your board. press enter or something to move on to the next card.  type 'end' to end the current game.

num_games: number of times you want to go through the deck.

seed: defaults to random. set this if you want to shuffle the deck in a particular order. i recommend not setting this argument.

endless: defaults to False. set to True if you want to continuously sample from a pool of cards. You might get the same card twice in a row
```

**Card Exclusions**

```
exclude_syllable_counts: syllable counts to exclude.

	i.e. exclude_syllables = 1 means you'll play with 2,3,4,5,6

exclude_syllable_beginnings: syllable beginnings to exclude.

	e.g. "mo" will exclude the "mo mo" and "mo ro" cards from your deck

exclude_cards: card names to exclude. not space sensitive

	e.g. writing "akino" will exclude KarutaCard("a ki no", 1) from your deck
```


**Card Inclusions**

**WARNING**: setting any of the below args will mean anything you don't mention will be excluded

```include_syllable_counts: syllable counts to include.

	i.e. include_syllables = 1,2,3,5,6 includes all but 4-syllable cards

include_syllable_beginnings: syllable beginnings to include. not space sensitive

	e.g. "mo" will include the "mo mo" and "mo ro" cards in your deck

include_cards: card names to include. not space sensitive

	e.g. writing "akino" will include KarutaCard("a ki no", 1) in your deck```
