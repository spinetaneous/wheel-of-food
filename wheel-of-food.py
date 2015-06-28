#!/bin/bash
# wheel-of-food.py
# Spin the wheel of food and figure out what you want for your next meal!

import requests
import oauth2
import logging
import random
import argparse
import json

logging.basicConfig(level=logging.CRITICAL)

file = open('config.json','r')
config = json.loads(file.read())
file.close()

CONSUMER_KEY = config['CONSUMER_KEY']
CONSUMER_SECRET = config['CONSUMER_SECRET']
TOKEN = config['TOKEN']
TOKEN_SECRET = config['TOKEN_SECRET']

class Wheel():
    def __init__(self,CONSUMER_KEY,CONSUMER_SECRET,TOKEN,TOKEN_SECRET):
        self.CONSUMER_KEY = CONSUMER_KEY
        self.CONSUMER_SECRET = CONSUMER_SECRET
        self.TOKEN = TOKEN
        self.TOKEN_SECRET = TOKEN_SECRET
        self.base_url = 'https://api.yelp.com/v2/search'
        self.food_categories = ['Mexican','Japanese']

    def _gen_signed_url(self, url_params):
        """ Generate a signed URL to call using the token and consumer identifiers and their respective secrets.
        url_params contains extra parameters to pass to Yelp's API URL beyond the authentication stuff;
        In our case, we're using it to pass along the type of food we want and our zip code.
        returns: signed_url_string """
        self.consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
        logging.debug(self.consumer)
        self.request = oauth2.Request(method='GET', url = self.base_url, parameters = url_params)
        logging.debug(self.request)
        self.request.update(
            {
                'oauth_nonce': oauth2.generate_nonce(),
                'oauth_timestamp': oauth2.generate_timestamp(),
                'oauth_token': TOKEN,
                'oauth_consumer_key': CONSUMER_KEY
            }
        )
        logging.debug(self.request)
        self.token = oauth2.Token(TOKEN, TOKEN_SECRET)
        logging.debug(self.token)
        self.request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), self.consumer, self.token)
        return self.request.to_url()

    def _select_food(self):
        """ Selects a random food category from the provided category list.
        Returns: category """
        return random.choice(self.food_categories)

    def spin(self,location,category=None):
        """ Spins the wheel. Hits up Yelp's API for food based on the provided ZIP code and the optional category of food. """
        if category is None:
            self.category = self._select_food()
        else:
            self.category = category
        url_params = {'location': location, 'term': self.category, 'limit': '20', 'category_filter': 'food,restaurants'}
        self.signed_url = self._gen_signed_url(url_params)
        logging.debug(self.signed_url)
        r = requests.get(self.signed_url)
        logging.debug(r.content)
        self.restaurants = r.json()['businesses']
        self.choice = random.choice(self.restaurants)
        return

parser = argparse.ArgumentParser("Hungry and can't decide what to eat? Give the Wheel of Food a spin!")
parser.add_argument('--zipcode', '-z', help="The ZIP code where you want to search. Required.", required=True)
parser.add_argument('--category','-c',help="Specify this option if you feel like you know what you want to eat.")
args = parser.parse_args()

category = args.category
zipcode = args.zipcode
wheel = Wheel(CONSUMER_KEY,CONSUMER_SECRET,TOKEN,TOKEN_SECRET)
wheel.spin(zipcode, category)
choice = wheel.choice['name']
url = wheel.choice['url']
rating = wheel.choice['rating']
category = wheel.category
review_count = wheel.choice['review_count']


print("Hungry for {0}? Try {1}, rated at {2} stars with {3} reviews!".format(category, choice, rating, review_count).decode('utf-8'))
