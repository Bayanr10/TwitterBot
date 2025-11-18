import discord
import tweepy
from commands import handle_tweet, update
import json
import os

intents = discord.Intents.all()
client = discord.Client(intents=intents)

#get the users from user.json
def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

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

        #Anonymous DM
        if isinstance(message.channel, discord.DMChannel):
            if user_message.startswith('!send'):
                args = user_message.split(' ')
                if len(args) < 2 or (len(args) < 3 and not message.attachments):

                    #If "help"
                    if len(args) > 1 and args[1] == 'help':
                        user_map = load_users()
                        if user_map:
                            help_msg = "\n".join([f"{name}: {uid}" for name, uid in user_map.items()])
                            await message.channel.send(f"**Available Users:**\n{help_msg}")
                        else:
                            await message.channel.send("No user list found.")
                    else:
                        await message.channel.send("**Usage:** `!send {user_id} {message}` (You can also attach an image)")
                    return

                target_user_id = args[1]
                msg_content = ' '.join(args[2:]) if len(args) > 2 else ""

                #Valid UserID?
                if not target_user_id.isdigit():
                    await message.channel.send("❌ User ID must be used. You can find it by right-clicking a user (with Developer Mode on).")
                    return

                try:
                    #Get UserID
                    target_user = await client.fetch_user(int(target_user_id))

                    #Prep content
                    send_content = f"Anonymous said: '{msg_content}'" if msg_content else "Anonymous sent you this:"
                    file_to_send = None
                    if message.attachments:
                        #Get only the first attachment
                        attachment = message.attachments[0]
                        file_to_send = await attachment.to_file()

                    #Send message
                    await target_user.send(content=send_content, file=file_to_send)
                    await message.channel.send("Message Sent!")
            
                except discord.NotFound:
                    await message.channel.send("User not found. Check the ID and try again")
                except discord.Forbidden:
                    await message.channel.send("Message blocked. User has DMs disabled or blocked the bot")
                except Exception as e:
                    await message.channel.send(f"Error: {str(e)}")
        
        
        def check(msg):
            return msg.author == message.author and msg.channel == message.channel

        print(f"{username} said: '{user_message}' ({channel})")
        #Updating server icon
        if user_message.lower().startswith('!updateserver'):
            await update(message)
        elif user_message.lower().startswith('!help'):
            await message.channel.send("use !updateserver with an attached .jpg, .png, or .jpeg to have me update the server icon!\n!tweet can be used to post a tweet to @disgustingloner")
        elif user_message.lower().startswith('!twitter'):
            await message.channel.send("You can find all posted tweets at https://x.com/DisgustingLoner")    
        #Text reply
        elif user_message.lower().startswith('!tweet'):
            await handle_tweet(message, twit_client, api)
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
    
def init_auth():
    api_key, api_secret, access_key, access_secret, disc_tok, bear_token = grab_keys()
    twit_client = tweepy.Client(bearer_token=bear_token, consumer_key=api_key, consumer_secret=api_secret, 
                            access_token=access_key, access_token_secret=access_secret)
    auth = tweepy.OAuthHandler(consumer_key=api_key, consumer_secret=api_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    return twit_client, api, disc_tok

if __name__ == '__main__':  
    twit_client, api, disc_tok = init_auth()
    run_discord_bot(twit_client)