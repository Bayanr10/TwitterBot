import discord
import tweepy
from commands import handle_tweet, update
#import requests
#import time
import json

intents = discord.Intents.all()
client = discord.Client(intents=intents)



def run_discord_bot(twit_client):

    @client.event
    async def on_ready():
        print(f'{client.user} is running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        
        def check(msg):
            return msg.author == message.author and msg.channel == message.channel

        print(f"{username} said: '{user_message}' ({channel})")
        #updating server icon
        if '!updateserver' in user_message:
            await update(message)
        elif '!help' in user_message:
            await message.channel.send("use !updateserver with an attached .jpg, .png, or .jpeg to have me update the server icon!\n!safetyprotocol is a fun command to mess with friends")
        #text reply
        elif '!tweet' in user_message:
            await handle_tweet(message, twit_client)
    client.run(disc_tok)

def grab_keys():
    with open("keys.json") as infile:
        json_obj = json.load(infile)
        api_key = json_obj["api_key"]
        api_secret = json_obj["api_secret"]
        access_key = json_obj["access_token"]
        access_secret = json_obj["access_secret"]
        disc_tok = json_obj["discord_token"]
        bear_token = json_obj["bearer_token"]
        return api_key, api_secret, access_key, access_secret, disc_tok, bear_token

if __name__ == '__main__':  
    api_key, api_secret, access_key, access_secret, disc_tok, bear_token = grab_keys()
    twit_client = tweepy.Client(bearer_token=bear_token, consumer_key=api_key, consumer_secret=api_secret, 
                            access_token=access_key, access_token_secret=access_secret)
    run_discord_bot(twit_client)