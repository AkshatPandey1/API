import json
import os
import time

import discord
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('DSC_TKN')
client = discord.Client()
excluded = [734875168370983014, 367630872066654209]
messagesChannel = dict()

@client.event
async def on_ready():
    print("{0.user} is online!".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    elif message.content.lower().startswith(".csnipe"):
        if message.channel not in messagesChannel:
            await message.channel.send("No recently deleted messages")
            return

        past = await message.channel.history(limit=30).flatten()
        deleted = [(elem.author.name + '#' + str(elem.author.discriminator), elem.content)
                   for elem in messagesChannel[message.channel] if elem not in past]

        if len(deleted) == 0:
            await message.channel.send("No recently deleted messages")
            return

        userMessages = dict()
        for elem in deleted:
            if elem[0] in userMessages:
                userMessages[elem[0]].append(elem[1])
            else:
                userMessages[elem[0]] = [elem[1]]

        for elem in userMessages:
            embed = discord.Embed(title=elem,
                                  description='➤' + "\n➤".join(userMessages[elem]))
            await message.channel.send(embed=embed)
            time.sleep(0.5)

    elif message.author.id != 734875168370983014:
        if message.channel not in messagesChannel:
            messagesChannel[message.channel] = []
        if len(messagesChannel[message.channel]) > 10:
            messagesChannel[message.channel].pop()
        messagesChannel[message.channel].append(message)

client.run(TOKEN)




