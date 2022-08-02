"""
Version 3 du bot python : un seul commentaire qui s'auto actualise lorsque le bot est connecté

"""
from dotenv import load_dotenv  # Récupération du token secret du bot dans le fichier config
from discord.ext import commands
import os


if __name__ == '__main__':

    load_dotenv(dotenv_path='config')

    bot = commands.Bot(command_prefix='!')

    @bot.event
    async def on_ready():
        print("bot ready")

    @bot.command()
    async def debug(context: commands.Context):

        await context.channel.send("debug")


    bot.run(os.getenv("TOKEN"))  # Lancement du bot avec le token secret
