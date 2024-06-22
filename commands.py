from aiohttp import ClientSession
import requests
import os
import asyncio

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

def count_reactions(message):
    yes = 0
    no = 0
    for reaction in message.reactions:
        print(f"reaction is {reaction}")
        if (reaction == '✅'):
            yes = reaction.count
        elif (reaction == '❌'):
            no = reaction.count
    return yes, no


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
                    yes, no = count_reactions(message)
                    limit = 0
                    while ((yes < 2 and no < 2) and limit != 20):
                        asyncio.sleep(5)
                        yes, no = count_reactions(message)
                        ++limit
                    if (yes < no):
                        await message.channel.send('tweet not posted')
                    else:
                        #twit_client.create_tweet(text=tweet_content, media_ids=[media_id])
                        #await message.channel.send('Tweet posted!')
                        os.remove(file_path)
                        await message.channel.send('tweet posted')
                    
                    print(f"Tweet Successful: {tweet_content}")
        else:
            yes, no = count_reactions(message)
            limit = 0
            while ((yes < 2 and no < 2) and limit != 20):
                asyncio.sleep(5)
                yes, no = count_reactions(message)
                limit += 1
                print(f"limit is {limit}")
                print(f"yes is {yes}\nno is {no}")
            if (yes < no):
                await message.channel.send('tweet not posted')
            else:
                #twit_client.create_tweet(text=tweet_content)
                print(f"Tweet Successful: {tweet_content}")
                await message.channel.send('tweet posted')    


    except Exception as e:
        await message.channel.send(f'Error: {e}')
        print(f"Error Occured: {e}")
