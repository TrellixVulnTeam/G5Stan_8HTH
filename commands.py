import requests
import sys
import random
import os
from utility import botMessage, invalidSearch

GIF_LIMIT = 1

def getImage(searchTerm, bot_id):
	"""
	Stan searches the GIFY API for a gif that matches the search 
	term.
	"""
	url = "http://api.giphy.com/v1/gifs/search"

	id = bot_id
	key = os.environ.get('GIPHY_KEY')
	payload = {
		'q':searchTerm,
		'limit': GIF_LIMIT,
		'api_key':key
	}
	try:
		request = requests.get(url, params=payload)
		# lets grab a random gif from the returned images.
		gif = random.choice(request.json()['data'])
		message = gif['images']['downsized']['url']
		botMessage(message, id)
	except:
		# If we failed to find something from our search,
		# we send back an error message. Stan style.
		invalidSearch(id)
	
def cheerUp(bot_id):
	"""
	Stan sends a message that will cheer up the members of the group
	chat.
	"""
	with open('compliments.txt') as compliments:
		message = random.choice(compliments.readlines())
		botMessage(message, bot_id)

def helpMeStan(bot_id):
	"""
	Will detail what stan can do and will use the README
	to grab all the information about the different functions
	"""
	function_lines = []
	with open('README.md') as readme:
		for line in readme:
			# We're checking to see if we hit the string that
			# shows when we're talking about commands
			if 'commands:' in line:
				for line in readme:
					"""
					 if we ever get to the point where commands
					 aren't last in the README, this is where
					 we'd break.
					"""
					function_lines.append(line)
		
		message = ''.join(function_lines)
		botMessage(message, bot_id)


#def atGroup(bot_id):

	