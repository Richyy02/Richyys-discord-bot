import discord
import scraper
import marktplaats_product
import imdb_random
import random
import os
from dotenv import load_dotenv

load_dotenv()

async def random_image(message, user_message, is_private):
    retries = 0

    searching_message = await message.channel.send("```Searching for a picture...```")

    while retries < 50:
        if retries == 3:
            await searching_message.delete()
            taking_long_message = await message.channel.send("```This can take some time depending on how fast the bot guesses a valid URL...```")
        try:
            response = scraper.handle_response(user_message)           
            if response is not None:
                print(f"Message is: {response}")
                file_path = f'Images\\{response}'
                if retries >= 3:
                    await taking_long_message.delete()
                else:
                    await searching_message.delete()
                await message.author.send(response) if is_private else await message.channel.send(file=discord.File(file_path))
                return
        except Exception as e:
            print(f"Error bot: {e}")

        retries += 1
        print(f"Try: {retries}")
        

    print("Max retries reached. Unable to find a valid link.")


async def marktplaats_search(message, user_query, is_private):
    search_message = await message.channel.send('```Searching for a random advertisement on marktplaats based on your search query```')
    try:
        response = marktplaats_product.handle_response(user_query)
        await search_message.delete()
        await message.channel.send(response["src"])
        await message.channel.send("```" + response["title"] + "```")
        await message.channel.send("```" + response["description"] + "...```")
        await message.channel.send("```" + response["price"] + "```")
    except Exception as e:
        await search_message.delete()
        await message.channel.send("```Het is niet gelukt. Probeer het opnieuw.```")
        print(f"Error: {e}")


async def random_movie(message, user_message):
    retries = 0
    search_message = await message.channel.send("```Searching for random movies, series, talkshows etc...```")
    
    while retries < 15:
        try:
            url = imdb_random.handle_response(user_message)
            if url is not None:
                if url.startswith("https://www.imdb.com/title/tt"):
                    await search_message.delete()
                    processing_message = await message.channel.send("```Found a movie/serie/talkshow! Processing data... ```")
                    response = imdb_random.main(url)
                    await processing_message.delete()
                    if response[0]["src"] == "":
                        await message.channel.send("```NO MOVIE/SERIES PICTURE PROVIDED ON IMDB ```")
                    else:
                        await message.channel.send(response[0]["src"])
                    if response[0]["title"] == "":
                        await message.channel.send("```NO TITLE PROVIDED ON IMDB ```")
                    else:
                        await message.channel.send("```Title: " + response[0]["title"] + "```")
                    if response[0]["episode"] != "":
                        await message.channel.send("```Episode: " + response[0]["episode"] + "```")
                    if response[0]["story_line"] == "":
                        await message.channel.send("```NO STORYLINE PROVIDED ON IMDB ```")
                    else:
                        await message.channel.send("```Story Line: " + response[0]["story_line"] + "```")
                    return
        except Exception as e:
            print(f"Error {e}")
    
        retries += 1
        print(f"Try: {retries}")

    print("Max retries reached. Unable to find a valid link.")


def run_discord_bot():
    print(os.getenv("DISCORD_TOKEN"))
    TOKEN = os.getenv("DISCORD_TOKEN")
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')


    @client.event
    async def on_message(message):
        if message.author == client.user or message.author.bot:
            return
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} said: '{user_message.encode('utf-8')}' ({channel})")

        if user_message.startswith("?"):
            user_message = user_message[1:]
            if user_message == 'random':
                await random_image(message, user_message, is_private=False)
            if user_message.startswith("search"):
                search_query = message.content[len("?search"):].strip()
                formatted_search_query = search_query.replace(" ", "+")
                await marktplaats_search(message, formatted_search_query, is_private=False)
            if user_message == 'movie':
                await random_movie(message, user_message)

    client.run(TOKEN)