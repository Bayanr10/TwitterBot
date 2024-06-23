from aiohttp import ClientSession
import requests
import os
import time

async def update(message):
    if message.attachments:
                img = message.attachments[0]
                if img.filename.endswith(('.jpg', '.png', '.jpeg', '.gif')):
                    img_url = img.url
                    async with ClientSession() as session:
                        await message.channel.send('updating server profile...')
                        async with session.get(img_url) as response:
                            if response.status == 200:
                                img_data = await response.read()
                            
                        await message.guild.edit(icon=img_data)
                        await message.channel.send('server pic updated!')
                else:
                    await message.channel.send('incorrect file type, please use a jpg, jpeg, or png file')

async def add_react(message):
    await message.add_reaction('✅')
    await message.add_reaction('❌')

async def count_reactions(message):
    yes = 0
    no = 0
    message = await message.channel.fetch_message(message.id)
    for reaction in message.reactions:
        if (reaction.emoji == '✅'):
            yes = reaction.count
        elif (reaction.emoji == '❌'):
            no = reaction.count
    return yes, no

async def monitor_reacts(message):
    yes, no = await count_reactions(message)
    limit = 0
    while (limit != 20):
        if (limit == 19 and yes >= no):
            return 1
        elif (yes > 2):
            return 1
        print(f"{3 * limit} seconds")
        time.sleep(3)
        yes, no = await count_reactions(message)
        limit += 1
        if ((yes == 1 and no == 1) and limit == 20):
            return 1
    return 0


async def handle_tweet(message, twit_client, api):
    tweet_content = message.content[len('!tweet'):]
    try:
        await add_react(message)
        if message.attachments:
            img = message.attachments[0]
            if img.filename.endswith(('.jpg', '.png', '.jpeg', '.gif')):
                response = requests.get(img.url)
                file_path = f'tmp_{img.filename}'
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                    media = api.media_upload(file_path)
                    media_id = media.media_id_string
                    if (await monitor_reacts(message) == 1):
                        twit_client.create_tweet(text=tweet_content, media_ids=[media_id])
                        await message.channel.send('tweet posted')
                        print(f"Tweet Successful: {tweet_content}")
                    else:
                        await message.channel.send('tweet not posted') 
                        print("tweet not posted")
            os.remove(file_path)
        else:
            if (await monitor_reacts(message) == 1):
                twit_client.create_tweet(text=tweet_content)
                print(f"Tweet Successful -> {tweet_content}")
                await message.channel.send('tweet posted')
            else:
                await message.channel.send('tweet not posted')    


    except Exception as e:
        await message.channel.send(f'Error: {e}')
        print(f"Error: {e}")
