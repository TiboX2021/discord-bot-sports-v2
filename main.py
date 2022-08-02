"""
Python discord sport counter bot v3
@author: Thibaut de Saivre

todo : il faut associer des keywords à un sport de sortie, un index. voir comment faire ça propremment
"""
import discord
from dotenv import load_dotenv  # Get secret unique bot token from config file
from discord.ext import commands  # discord.py API
import os
from tracker import Tracker

sports = {
    "Handball": ["hand", "handball"],
    "Natation": ["natation"],
    "Badminton": ["bad", "badminton"],
    "Basket": ["basket"],
    "Football": ["foot", "football"],
    "Escalade": ["escalade"],
    "Volley": ["volley"],
    "Raid": ["raid"],
    "Aviron": ["aviron"],
    "Boxe": ["boxe"],
    "Judo": ["judo"],
    "Escrime": ["escrime"],
    "Tennis": ["tennis"],
    "Rugby": ["rugby"],
    "Equitation": ["equitation", "équitation"],
    "Crossfit": ["crossfit"],
}


def multi_key_dict(d: dict) -> dict:
    """dict[key, [value]] -> dict[[value], key]"""
    out = {}

    for key, values in d.items():
        for value in values:
            out[value] = key

    return out


if __name__ == '__main__':

    load_dotenv(dotenv_path='config')  # Loading config file data
    DEBUG_CONV_ID = int(os.getenv("DEBUG_CONV"))
    DEUX_SPORTS_PREFERES_ID = int(os.getenv("DEUX_SPORTS_PREFERES"))
    AUTHOR_ID = int(os.getenv("AUTHOR_ID"))

    bot = commands.Bot(command_prefix='!')

    # Trackers
    sport_tracker = Tracker(channel_ids=[DEBUG_CONV_ID], data_file_path="sport_tracker_data.json",
                            keywords_to_values=multi_key_dict(sports))


    @bot.event
    async def on_message(message: discord.Message):
        await bot.process_commands(message)  # on_message overrides all @bot.command()

        await sport_tracker.on_message(message)


    @bot.event
    async def on_ready():
        print("bot ready")
        await sport_tracker.on_startup(bot)


    @bot.command()
    async def debug(context: commands.Context):
        print("debug test performed on channel of id", context.channel.id)
        if context.channel.id == DEBUG_CONV_ID:
            await context.channel.send("debug")


    @bot.command()
    async def deco_bot(context: commands.Context):
        if context.author.id == AUTHOR_ID:
            await context.channel.send("au revoir!")
            await sport_tracker.on_exit()

            try:
                await bot.logout()
            except RuntimeError:  # always happens on standard exit
                print("bot exited")


    bot.run(os.getenv("TOKEN"))  # Start bot with secret token
