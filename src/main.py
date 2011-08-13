#!/usr/bin/python2.7

# Copyright 2011 Ajay Roopakalu
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import tweepy
import ConfigParser
import os
import sys
import utils

_NAME = 'COMMANDER TWEET'
_VERSION = '0.1'

class TweetStream():
	def __init__(self, tweets, ut):
		import locale
		self.ut = ut
		self.tweets = tweets
		locale.setlocale(locale.LC_ALL, '')
		self.code = locale.getpreferredencoding()

	def refresh(self):
		os.system('clear')
		print self.ut.bold('\n   ' + _NAME)
		print self.ut.bold('     Version ' + _VERSION + '\n')
		for tweet in self.tweets:
			print '  ', self.ut.bold(tweet.user.name.encode(self.code)),
			print '@{}'.format(tweet.user.screen_name.encode(self.code)),
			print '({})'.format(self.ut.human_date(tweet.created_at))
			print '    {}'.format(tweet.text.encode(self.code))
	
	def update(self, tweet):
		self.tweets.insert(0, tweet)
		self.tweets = self.tweets[:-1]
		self.refresh()

class TweetRC():
	def __init__(self):
		self._config = None

	def GetConsumerKey(self):
		return self._GetOption('consumer_key')

	def GetConsumerSecret(self):
		return self._GetOption('consumer_secret')

	def GetAccessKey(self):
		return self._GetOption('access_token_key')

	def GetAccessSecret(self):
		return self._GetOption('access_token_secret')

	def _GetOption(self, option):
		try:
			return self._GetConfig().get('CommanderTweet', option)
		except:
			return None

	def _GetConfig(self):
		if not self._config:
		 	self._config = ConfigParser.ConfigParser()
		 	self._config.read(os.path.expanduser('~/.ctweetrc'))
		return self._config

class StreamListener(tweepy.StreamListener):
	def __init__(self, TS):
		super(StreamListener, self).__init__()
		self.TS = TS
	def on_status(self, status):
		try:
			self.TS.update(status)
			print_prompt()
		except Exception, e:
			print e

def print_prompt(newline=True):
	if newline:
		print ''
	print '[r]efresh, [q]uit:',
	sys.stdout.flush()

def authenticate():
	rc = TweetRC()
	auth = tweepy.OAuthHandler(rc.GetConsumerKey(), rc.GetConsumerSecret())
	auth.set_access_token(rc.GetAccessKey(), rc.GetAccessSecret())
	return auth
	

def main():
	ut = utils.Utils()
	auth = authenticate()
	api = tweepy.API(auth)
	TS = TweetStream(api.home_timeline(), ut)

	TS.refresh()
	print_prompt()

	stream = StreamListener(TS)
	streamer = tweepy.Stream(auth, stream, secure=True)
	streamer.userstream(async=True)

	while True:
		char = raw_input()
		if char is 'q':
			break
		elif char is 'r':
			TS.refresh()
			print_prompt()
		else:
			TS.refresh()
			print ut.bold('Error: could not interpret input.')
			print_prompt(newline=False)

if __name__ == '__main__':
	try:
		main()
	except Exception, e:
		''' Break on any error '''
		print e
	
