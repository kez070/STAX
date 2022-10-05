import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True

players = {}
monitored_msg_id = 0
channel_id = 0
stored_msg = ""
running_session = True

bot = commands.Bot(command_prefix='!', intents=intents)


def createSignupList():
    global stored_msg
    temp_msg = stored_msg

    for i in players:
        temp_msg = temp_msg + "\n" + players[i]
    return temp_msg

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# @bot.event
# async def on_message(message):
#     print('received message')
#     if message.author == bot.user:
#         return
#
#     if message.content.startswith('$hello'):
#         print('triggered')
#         await message.channel.send('Hello!')

@bot.command()
async def create(ctx, num='5'):

    def check(reaction, user):  # Our check for the reaction
        return user.name not in players
    print("triggered")

    global stored_msg
    if num == '5':
        stored_msg = 'A new 5s has been created! React below to join the queue! \nCurrent Queue: '
    elif num == '10':
        stored_msg = 'A new 10s has been created! React below to join the queue! \nCurrent Queue: '
    else:
        stored_msg = 'A new ??s has been created! React below to join the queue! \nCurrent Queue: '
    msg = await ctx.channel.send(stored_msg)

    global players
    global monitored_msg_id
    global channel_id
    global running_session

    running_session = False

    players = {}
    monitored_msg_id = msg.id
    channel_id = ctx.channel.id

    emoji = '\N{THUMBS UP SIGN}'
    await msg.add_reaction(emoji)

    # running_session = True
    # while running_session:
    #     reaction, user = await bot.wait_for("reaction_add", check=check)
    #     players[user.id] = user.name
    #     await msg.edit(content=createSignupList())


@bot.event
async def on_raw_reaction_add(payload):
    print('add detected')
    reaction = str(payload.emoji)
    user_id = payload.user_id
    user = await bot.fetch_user(user_id)
    username = user.name
    msg_id = payload.message_id

    if msg_id == monitored_msg_id and username != 'peasants-stax':
        global players
        global channel_id
        players[user_id] = username
        channel = bot.get_channel(channel_id)
        msg = await channel.fetch_message(msg_id)
        await msg.edit(content=createSignupList())
        if len(players.keys()) == 4:
            await channel.send("@here -1")
        elif len(players.keys()) == 3:
            await channel.send("@here -2")


@bot.event
async def on_raw_reaction_remove(payload):
    reaction = str(payload.emoji)
    msg_id = payload.message_id
    print(monitored_msg_id)
    print(msg_id)
    global players
    if msg_id == monitored_msg_id:
        del players[payload.user_id]
        print("removed")

        global channel_id
        channel = bot.get_channel(channel_id)
        msg = await channel.fetch_message(msg_id)
        await msg.edit(content=createSignupList())
        if len(players.keys()) == 4:
            await channel.send("@here -1")
        elif len(players.keys()) == 3:
            await channel.send("@here -2")

bot.run(TOKEN)
