"""
Python discord sport counter bot v3
@author: Thibaut de Saivre
"""
import discord
import dotenv  # Get secret unique bot token from config file
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


HEADER = "**Résultats :**\n"

BOTTOM = (
    "**Quelques infos sur mon fonctionnement :**\n"
    "   ⦁ Tant que je suis connecté, ce message sera mis à jour à chaque nouveau message\n"
    "   ⦁ Pour que je compte ton choix, il suffit que tu mette '1' suivi de ton sport "
    "n'importe où dans un message.\n"
    "   ⦁ Je reconnais plusieurs mots-clés pour chaque sport\n"
    "   ⦁ La capitalisation n'a pas d'importance\n"
    "   ⦁ Je retiens uniquement les derniers choix pour chaque personne\n"
    "*Exemple : '1) badminton', 'azerty 1 - bad', 'j'aime le 1 bad' sont valides*"
)

if __name__ == '__main__':

    dotenv.load_dotenv(dotenv_path='config')  # Loading config file data
    DEBUG_CONV_ID = int(os.getenv("DEBUG_CONV"))
    AUTHOR_ID = int(os.getenv("AUTHOR_ID"))
    work_channel = int(os.getenv("CHANNEL"))
    SUMMARY_MSG_ID = 0

    bot = commands.Bot(command_prefix='!')

    # Trackers
    sport_tracker = Tracker(channel_ids=[work_channel], data_file_path="sport_tracker_data.json",
                            keywords_to_values=multi_key_dict(sports))


    async def update_message():
        """Update the bot pinned message"""
        channel: discord.GroupChannel = bot.get_channel(work_channel)
        message = await channel.fetch_message(SUMMARY_MSG_ID)

        new_content = HEADER + '\n' + sport_tracker.summary_msg() + '\n' + BOTTOM
        await message.edit(content=new_content)


    @bot.event  # Called each time someone comments (on the specific channel)
    async def on_message(message: discord.Message):
        await bot.process_commands(message)  # on_message overrides all @bot.command()

        update = False
        update = update or await sport_tracker.on_message(message)

        if update:
            await update_message()


    @bot.event  # Called when the bot is connected and ready
    async def on_ready():
        global SUMMARY_MSG_ID
        print("bot ready")

        # Create summary comment
        if str(work_channel) not in os.environ:
            message = await bot.get_channel(work_channel).send("message originel")
            dotenv.set_key('config', str(work_channel), str(message.id))

        SUMMARY_MSG_ID = int(os.getenv(str(work_channel)))
        await sport_tracker.on_startup(bot)

        await update_message()


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
