"""
Python discord sport counter bot v3
@author: Thibaut de Saivre

todo : il faut un objet parser. A créer (on pourrait mettre cet objet en paramètre du tracker, par exemple)
todo : mettre le tracker dans un fichier qui lui est propre
"""
import discord
from dotenv import load_dotenv  # Get secret unique bot token from config file
from discord.ext import commands  # discord.py API
import os
from tracker import Tracker

if __name__ == '__main__':

    load_dotenv(dotenv_path='config')  # Loading config file data
    DEBUG_CONV_ID = int(os.getenv("DEBUG_CONV"))
    DEUX_SPORTS_PREFERES_ID = int(os.getenv("DEUX_SPORTS_PREFERES"))

    bot = commands.Bot(command_prefix='!')

    # Trackers
    sport_tracker = Tracker(channel_ids=[DEBUG_CONV_ID], data_file_path="sport_tracker_data.json")


    @bot.event
    async def on_message(message: discord.Message):
        await sport_tracker.on_message(message)


    @bot.event
    async def on_ready():
        print("bot ready")
        await sport_tracker.on_startup(bot)


    # Bot commands

    @bot.command()
    async def debug(context: commands.Context):
        print(context.channel.id)
        if context.channel.id == int(os.getenv("DEBUG_CONV")):
            await context.channel.send("debug")


    bot.run(os.getenv("TOKEN"))  # Start bot with secret token
