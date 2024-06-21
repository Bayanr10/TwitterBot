from aiohttp import ClientSession
import requests
import os

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


async def handle_tweet(message, twit_client, api):
    tweet_content = message.content[len('!tweet'):]
    try:
        if message.attachments:
            img = message.attachments[0]
            if img.filename.endswith(('.jpg', '.png', '.jpeg', '.gif')):
                response = requests.get(img.url)
                file_path = f'tmp_{img.filename}'
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                try:
                    media = api.media_upload(file_path)
                    media_id = media.media_id_string
                    twit_client.create_tweet(text=tweet_content, media_ids=[media_id])
                    await message.channel.send('Tweet posted!')
                    print(f"Tweet Successful: {tweet_content}")
                except Exception as e:
                    await message.channel.send(f'Error: {e}')
                    print(f"Error Occured: {e}")
        else:    
            twit_client.create_tweet(text=tweet_content)
            await message.channel.send('Tweet posted!')
            print(f"Tweet Successful: {tweet_content}")


    except Exception as e:
        await message.channel.send(f'Error: {e}')
        print(f"Error Occured: {e}")
    
    finally:
         os.remove(file_path)
