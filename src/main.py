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
import time
import utils
import locale

from threading import Thread

class TweetStream():
	def __init__(self, tweets):
		self.ut = utils.Utils()
		self.tweets = tweets
		locale.setlocale(locale.LC_ALL, '')
		self.code = locale.getpreferredencoding()
	
	def disp(self):
		for tweet in self.tweets:
			print self.ut.bold(tweet.user.name.encode(self.code)),
			print '@{}'.format(tweet.user.screen_name.encode(self.code)),
			print '({})'.format(self.ut.human_date(tweet.created_at))
			print '  {}'.format(tweet.text.encode(self.code))
	
	def update(self, tweet):
		self.tweets.insert(0, tweet)
		self.tweets = self.tweets[:-1]
		self.disp()

class TweetRc():
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
	def on_status(self, status):
		try:
			TS.update(status)
		except Exception, e:
			print e

def main():
	global TS
	rc = TweetRc()

	auth = tweepy.OAuthHandler(rc.GetConsumerKey(), rc.GetConsumerSecret())
	auth.set_access_token(rc.GetAccessKey(), rc.GetAccessSecret())

	api = tweepy.API(auth)
	os.system('clear')
	TS = TweetStream(api.home_timeline())
	TS.disp()

	stream = StreamListener()
	streamer = tweepy.Stream(auth, stream, secure=True)
	streamer.userstream()

if __name__ == '__main__':
	TS = None
	try:
		main()
	except KeyboardInterrupt:
		pass
	
