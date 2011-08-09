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

import twitter
import datetime
import rfc822
import ConfigParser
import os

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

def bold(x):
	return '\x1b[1m' + x + '\x1b[0m'

def prettydate(d):
	diff = datetime.datetime.utcnow() - d
	s = diff.seconds

	if diff.days > 7 or diff.days < 0:
		return d.strftime('%d %b %y')
	elif diff.days == 1:
		return '1 day ago'
	elif diff.days > 1:
		return '{} days ago'.format(diff.days)
	elif s <= 1:
		return 'just now'
	elif s < 60:
		return '{} seconds ago'.format(s)
	elif s < 120:
		return '1 minute ago'
	elif s < 3600:
		return '{} minutes ago'.format(s/60)
	elif s < 7200:
		return '1 hour ago'
	else:
		return '{} hours ago'.format(s/3600)

def main():
	rc = TweetRc()
	api = twitter.Api(consumer_key=rc.GetConsumerKey(),
					  consumer_secret=rc.GetConsumerSecret(),
					  access_token_key=rc.GetAccessKey(),
					  access_token_secret=rc.GetAccessSecret())
	home_timeline = api.GetHomeTimeline()

	for tweet in home_timeline:
		created_at = datetime.datetime(*rfc822.parsedate(tweet.created_at)[:-2])
		print bold(tweet.user.name), '@{0}'.format(tweet.user.screen_name), 
		print '({0})'.format(prettydate(created_at))
		print '  ', tweet.text

if __name__ == '__main__':
	main()
