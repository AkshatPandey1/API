import os
import discord
from Emotions import Emotions
from dotenv import load_dotenv
load_dotenv()


def returnMood(text):
    elems = Emotions(text)
    try:
        if text.lower().endswith('.stats'):
            elems = Emotions(text[:-6])
            d = elems.getAllEmotions()
            d = sorted(d.items(), key=lambda x: x[1], reverse=True)
            embed = discord.Embed(title=elems.getMaxEmotion().capitalize(),
                                  description="\n".join([("{}: {}".format(elem[0], elem[1]))
                                                         for elem in d]) + '\n' +
                                              '\nText analyzed: {}'.format(elems.getText()))
            return embed

        else:
            embed = discord.Embed(title=text, description="Max emotion: {}\n".format(elems.getMaxEmotion()))
            return embed

    except:
        return discord.Embed(title="Input too short", description="Input length was too short to detect for emotions, "
                                                                  "enter a longer input")


def main():
    TOKEN = os.getenv('DSC_TKN')

    client = discord.Client()

    @client.event
    async def on_ready():
        print("{0.user} is online!".format(client))

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        if message.content.lower().startswith("e.help"):
            embed = discord.Embed(title="You need help",
                                  description="Damn, you guys are really dumb huh. Never listening to AP. \n\n"
                                              "Anyway,\n\n"
                                              "Do E.{line} to get max emotion of the line\n\n"
                                              "Do E.{line}.stats to get all emotion stats of the line\n\n"
                                              "Do E.{line}.sentiment to know if the sentence has a positive or negative"
                                              "sentiment\n\n")
            await message.channel.send(embed=embed)

        elif message.content.lower().startswith("e.last"):
            messages = await message.channel.history(limit=100).flatten()
            messages.reverse()
            text = ". ".join([elem.content for elem in messages
                             if elem.author.id == message.author.id
                             and elem.content.lower()[:2] != "e."][-5:]) + '.'
            await message.channel.send(embed=returnMood(text + '.stats'))

        elif message.content.lower().endswith('.sentiment'):
            text = message.content[:-10]
            sentiment = Emotions(text).getSentiment()

            if sentiment > 0:
                text = 'Positive'
            elif sentiment == 0:
                text = 'Neutral'
            else:
                text = 'Negative'

            embed = discord.Embed(title=text, description='Score: ' + str(sentiment) + '\n')
            await message.channel.send(embed=embed)

        elif message.content.lower().startswith("e."):
            await message.channel.send(embed=returnMood(message.content[2:]))

    client.run(TOKEN)


if __name__ == "__main__":
    main()
