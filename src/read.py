import argparse
import subprocess
from card import cards
from config import create_config
import random
import time
import os


def get_wait_time():
	#returns float which is the waiting time between poems being read
	#gives you time to get back to your board after user input
	return random.random() + 3.0

def play_sound(sound_directory, card_num, verse=1):
	"""This assumes your poem filename is in the format

	CARD ZERO = NANIWA

	poems_dir/I-###V.mp4
	where ### is the poem number (with leading zeros: 001, 023, 100)
	and V is either A (first verse) or B (second verse)

	Edit this fn if this isn't the case

	Use utils.py/ogg_to_mp4.py to set up mp4 files.
	Or edit this fn to play ogg, I'm not your dad

	"""
	assert verse in [1, 2]
	assert card_num >= 0 and card_num <= 100

	poem_num = str(card_num)
	if card_num < 10:
		poem_num = "00" + poem_num
	elif card_num < 100:
		poem_num = "0" + poem_num

	if verse == 1:
		poem_num = poem_num + "A"
	else:
		poem_num = poem_num + "B"

	poem_file = "I-{}.mp4".format(poem_num)

	subprocess.call(["afplay", os.path.join(sound_directory, poem_file)])


def filter_deck(config):
	"""
	Config params:
		optional exclusion arguments

		exclude_syllable_counts: syllable counts to exclude.
			i.e. exclude_syllables = 1 means you'll play with 2,3,4,5,6
		exclude_syllable_beginnings: syllable beginnings to exclude.
			e.g. "mo" will exclude the "mo mo" and "mo ro" cards from your deck
		exclude_cards: card names to exclude. not space sensitive
			e.g. writing "akino" will exclude KarutaCard("a ki no", 1) from your deck

		WARNING: setting any of the below args will mean anything you don't mention will be excluded

		include_syllable_counts: syllable counts to include.
			i.e. include_syllables = 1,2,3,5,6 includes all but 4-syllable cards
		include_syllable_beginnings: syllable beginnings to include. not space sensitive
			e.g. "mo" will include the "mo mo" and "mo ro" cards in your deck
		include_cards: card names to include. not space sensitive
			e.g. writing "akino" will include KarutaCard("a ki no", 1) in your deck
	"""
	filtered_cards = []

	if all([config.get(keyword, None) == None \
				for keyword in \
				["include_syllable_counts", "include_syllable_beginnings", "include_cards"]]):
		filtered_cards = cards
	else:
		for card in cards:
			if card.syllable_count in config.get("include_syllable_counts", []):
				filtered_cards.append(card)
			elif card.name.replace(" ", "") in config.get("include_cards", []) or card.name in config.get("include_cards", []):
				filtered_cards.append(card)
			else:
				for syllables in config.get("include_syllable_beginnings", []):
					shortened_syllable_keyword = syllables.replace(" ", "")
					if card.name.replace(" ", "")[:len(shortened_syllable_keyword)] == shortened_syllable_keyword:
						filtered_cards.append(card)
						break

	filtered_cards_2 = filtered_cards
	if not all([config.get(keyword, None) == None \
				for keyword in \
				["exclude_syllable_counts", "exclude_syllable_beginnings", "exclude_cards"]]):
		for card in filtered_cards:
			if card.syllable_count in config.get("exclude_syllable_counts", []):
				filtered_cards_2.remove(card)
			elif card.name.replace(" ", "") in config.get("exclude_cards", []) or card.name in config.get("exclude_cards", []):
				filtered_cards_2.remove(card)
			else:
				for syllables in config.get("exclude_syllable_beginnings", []):
					shortened_syllable_keyword = syllables.replace(" ", "")
					if card.name.replace(" ", "")[:len(shortened_syllable_keyword)] == shortened_syllable_keyword:
						filtered_cards_2.remove(card)
						break
	return filtered_cards_2

def deck_generator(deck, endless = False):
	if endless == True:
		while True:
			yield random.choice(deck)
	else:
		for card in deck:
			yield card


def main(config):
	"""
	Config params:
		seed: set the random seed for your game. not recommended

		optional exclusion arguments

		exclude_syllable_counts: syllable counts to exclude.
			i.e. exclude_syllables = 1 means you'll play with 2,3,4,5,6
		exclude_syllable_beginnings: syllable beginnings to exclude.
			e.g. "mo" will exclude the "mo mo" and "mo ro" cards from your deck
		exclude_cards: card names to exclude. not space sensitive
			e.g. writing "akino" will exclude KarutaCard("a ki no", 1) from your deck

		WARNING: setting any of the below args will mean anything you don't mention will be excluded

		include_syllable_counts: syllable counts to include.
			i.e. include_syllables = 1,2,3,5,6 includes all but 4-syllable cards
		include_syllable_beginnings: syllable beginnings to include. not space sensitive
			e.g. "mo" will include the "mo mo" and "mo ro" cards in your deck
		include_cards: card names to include. not space sensitive
			e.g. writing "akino" will include KarutaCard("a ki no", 1) in your deck
	"""
	deck = filter_deck(config)

	if config.get("seed", None) is not None:
		random.seed(config.seed)
	print("shuffling deck... ({} cards in deck)".format(len(deck)))
	random.shuffle(deck)

	user_inp = input("Ready to start?")

	print("naniwa...")

	#play opening poem part 1
	play_sound(config["poems_dir"], 0, 1)

	#time between poems
	time.sleep(1)

	#play opening poem part 2
	play_sound(config["poems_dir"], 0, 2)

	#time between poems
	time.sleep(1)

	for card in deck_generator(deck, config.get("endless", False)):
		#play card part 1
		play_sound(config["poems_dir"], card.number, 1)

		print(card)
		#user input

		if config.get("wait_for_user_input", True) == True:
			user_inp = input("Ready for the next card?")
			if user_inp == "end":
				print("ending current match")
				break

			#time for the player
			time.sleep(get_wait_time())
		else:
			time.sleep(1)

		#play card part 2
		play_sound(config["poems_dir"], card.number, 2)

		#time between poems
		time.sleep(1)
	print("match is over!")





if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--config_file", type=str, default=None)
	args = parser.parse_args()

	if args.config_file is None:
		karuta_config = {}
	else:
		karuta_config = create_config(args.config_file)

	if karuta_config.get("poems_dir", None) is None:
		print("No poems directory specified. Can't play sounds. Set `poems_dir` in your config")


	#Preprocessing of config so that everything with 1 arg is recognized as a list.

	for keyword in ["include_syllable_counts", "include_syllable_beginnings", "include_cards",
					"exclude_syllable_counts", "exclude_syllable_beginnings", "exclude_cards"]:
		if karuta_config.get(keyword, None) is not None and type(karuta_config[keyword]) is not list:
			karuta_config[keyword] = [karuta_config[keyword]]

	for i in range(karuta_config.get("num_games", 1)):
		print("starting new game...")
		main(karuta_config)
