wheel-of-food.py

Welcome to the Wheel of Food!  Can't decide what you want to eat? Why not give this a spin? It'll then trawl through Yelp and return some food for you and your fickle heart.

To run, you'll need a developer's account at Yelp (https://api.yelp.com). Copy config.default.json to config.json and put in your needed stuff (consumer key/secret, token and token secret.) You'll also want to consider making this file chmod 600 as well. There's probably a better way to distribute this properly, but this is my first real app so I'll figure that part out later.

The requirements are in requirements.txt.  You'll need:

requests
argparse
oauth2

To install the requirements, run pip install -r requirements.txt.
