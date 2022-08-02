"""
Python discord sport counter bot v3
@author: Thibaut de Saivre
"""
import discord
import dotenv
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
    work_channel = DEBUG_CONV_ID
    SUMMARY_MSG_ID = 0

    bot = commands.Bot(command_prefix='!')

    # Trackers
    sport_tracker = Tracker(channel_ids=[work_channel], data_file_path="sport_tracker_data.json",
                            keywords_to_values=multi_key_dict(sports))


    @bot.event
    async def on_message(message: discord.Message):
        await bot.process_commands(message)  # on_message overrides all @bot.command()

        update = False
        update = update or await sport_tracker.on_message(message)

        if update:
            channel: discord.GroupChannel = bot.get_channel(work_channel)
            message = await channel.fetch_message(SUMMARY_MSG_ID)
            await message.edit(content='edited!')


    @bot.event
    async def on_ready():
        global SUMMARY_MSG_ID
        print("bot ready")

        # Create summary comment
        if str(work_channel) not in os.environ:
            # TODO : create comment and get ID -> set the id to the env.
            message = await bot.get_channel(work_channel).send("message originel")
            dotenv.set_key('config', str(work_channel), str(message.id))

        SUMMARY_MSG_ID = int(os.getenv(str(work_channel)))
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

            await bot.close()  # throws a RuntimeError, this is normal


    bot.run(os.getenv("TOKEN"))  # Start bot with secret token
