#! /usr/bin/env python3
import sys

import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

import pytoml as toml


global configFile = 'apis.toml'

class MyListener(StreamListener):

    def __init__(self, outputfile):
        self.filename = outputfile

    def on_data(self, data):
        try:
            with open(self.filename, 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True

def loadConfig(filename):
    with open(filename, 'rb') as fin:
        return toml.load(fin)

def main():
    if len(sys.argv) < 3:
        print("Error! Ussage: %s <outputfile> <keyword [keyword [..]]>" % sys.argv[0])
    else:
        downloadTweets(sys.argv[2:], sys.argv[1]);

def downloadTweets(config, filters, outputFile):
    # Auth and api access

    consumer_key = config.consumer_key
    consumer_secret = config.consumer_secret
    access_token = config.access_token
    access_secret = config.access_secret

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    # Stream the data
    twitter_stream = Stream(auth, MyListener(outputFile))
    twitter_stream.filter(track=filters)

if __name__ == '__main__':
    main()
