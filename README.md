# Richyys-discord-bot
A discord bot that does some random stuff.

# First feature is random image scraper.
When typing ?random in your discord text channel the bot will try and look for a random valid image URL on https://prnt.sc and https://imgur.com. Back in the days these websites used to have easy guessable URLS. The bot will download these images and save them to the Images folder in the root of the project (you might have to make this folder yourself) and send them back as response in the text channel.

# Second feature is random IMDb. (CURRENTLY BROKEN)
When typing ?movie in the text channel the bot will try and look for a random IMDb movie, series or talkshow by once again guessing the URL. When it found a valid URL it will return the title, episode, story line, and picture (some of these will not always be sent as for example movies don't have episodes.)

# Third feature is marktplaats search.
When typing ?search {query} the bot will look for a random advertisment on marktplaats based on the query (marktplaats is the dutch ebay) and send back the picture, advertisment name and price.

All these features are web scrapers and are built to run on the firefox geckodriver.

# Installation

First do pip install -r .\requirements.txt

Create an .env file and add DISCORD_TOKEN = your_discord_token

Finally type: python3 main.py in terminal to run the bot.
