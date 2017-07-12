import requests
import sys
import os
import random
import re
from reminder.py import Reminder
from utility import botMessage, invalidSearch, obtainHotSubmissions, \
					stringToSeconds

GIF_LIMIT = 1

def getImage(searchTerm):
	"""
	Stan searches the GIFY API for a gif that matches the search 
	term.
	"""
	url = "http://api.giphy.com/v1/gifs/search"
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
		botMessage(message)
	except:
		# If we failed to find something from our search,
		# we send back an error message. Stan style.
		invalidSearch()
	
def cheerUp():
	"""
	Stan sends a message that will cheer up the members of the group
	chat.
	"""
	with open('compliments.txt') as compliments:
		message = random.choice(compliments.readlines())
		botMessage(message)

def helpMeStan():
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
		botMessage(message)

def eyeBleach():
	"""
	Will send 3 gifs/images that will be of adorable things that
	should cover up the current conversation screen. We'll just
	scrape from r/eyebleach
	"""
	# we're going to grab the top five incase one of the submissions
	# is a reddit text post, then we can filter it out.
	submissions = obtainHotSubmissions('eyebleach', num_of_sub=5)

	sub_count = 0

	for submission in submissions:
		if 'reddit.com' not in submission.url and sub_count < 3:
			botMessage(submission.url)
			sub_count += 1

def remind(user_id, user_name, parse_message):
	"""
	Will create a reminder for the specified user that will fire after
	the specified amount of time.

	user_id: the groupme user id that matches the uid of the person who
			 asked for the reminder.
	user_name: The actual string name of the user who asked for the reminder
	parse_message: This contains the actual message that the user typed in to
				   the groupme chat. Is the 'in [time] to [message]', does
				   not include the command used to get here.
	"""	
	time = re.search('in(.*)to', parse_message).group(1).strip()
	message = re.search('to(.*)', parse_message).group(1).strip()
	seconds = stringToSeconds(time)
	if seconds > 0:
		# we don't need to check if the message follows the desired format
		# since it would fail in the stringToSeconds.
		reminder = new Reminder(user_name, user_id, message, seconds)
		reminder.start_reminder()
	else:
		# Since we don't have the format we need, we gotta let the user know
		# the format we do need.
		message = "I didn't quite catch that. Make sure you type it like this: '/remindme in [time] to [message]"	
		botMessage(message)
