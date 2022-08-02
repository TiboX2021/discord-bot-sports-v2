"""
Python discord sport counter bot v3
@author: Thibaut de Saivre
"""
from datetime import datetime
import discord
from dotenv import load_dotenv  # Get secret unique bot token from config file
from discord.ext import commands  # discord.py API
import json  # read/write in data files
from typing import TypedDict  # better type hints
import os

date_format = '%d/%m/%Y %H:%M:%S'  # jj/mm/yyy hh:mm:ss


# data format of data files
class Data(TypedDict):
    date: str  # Data of last processed comment
    history: dict[str, int]  # [user_id, choice_index] pairs


class Tracker:

    def __init__(self, channel_ids: list[int], data_file_path: str):
        self.channel_ids = channel_ids  # channels to monitor

        # Loading data
        self.data_file_path = data_file_path
        self.last_comment_date = datetime(2022, 1, 1)  # default date
        self.history: dict[str, int] = {}
        self.read_data()

    def __del__(self):
        """Destructor: write data collected in data file"""
        new_data = {'history': self.history, 'data': self.last_comment_date.strftime(date_format)}

        file = open(self.data_file_path, 'w')
        file.write(json.dumps(new_data))
        file.close()

    def read_data(self):
        """Reading data from data file"""

        try:
            file = open(self.data_file_path, 'r')
            data: Data = json.loads(file.read())
            file.close()

            self.history = data['history']
            self.last_comment_date = datetime.strptime(data['date'], date_format)

        except IOError:
            print("Error while opening data file")
            # A new data file will be created on destruction

    async def on_startup(self):
        """Called when the bot is ready"""
        pass
        # TODO : scanning channels

    async def on_message(self, message: discord.Message):
        """Called each time a message is posted"""
        if message.channel.id not in self.channel_ids:
            return

        # TODO


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
        await sport_tracker.on_startup()


    # Bot commands

    @bot.command()
    async def debug(context: commands.Context):
        print(context.channel.id)
        if context.channel.id == int(os.getenv("DEBUG_CONV")):
            await context.channel.send("debug")


    bot.run(os.getenv("TOKEN"))  # Start bot with secret token
