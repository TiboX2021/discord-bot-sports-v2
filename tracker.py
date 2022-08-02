from typing import TypedDict
from datetime import datetime
import json
import discord
from discord.ext import commands

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

    async def on_startup(self, bot: commands.Bot):
        """Called when the bot is ready"""
        new_comment_date = self.last_comment_date  # Update last comment date after processing

        new_votes: dict[str, int] = {}

        for channel_id in self.channel_ids:
            channel = bot.get_channel(channel_id)

            messages: list[discord.Message] = channel.history(after=self.last_comment_date).flatten()
            for message in messages:
                # TODO : check all first votes in the history.
                # TODO : then merge with old votes. (use another function?)
                pass

            if messages[0].created_at > new_comment_date:
                new_comment_date = messages[0].created_at

        self.history = new_votes | self.history  # merge votes. new_votes overwrite old votes
        self.last_comment_date = new_comment_date

    async def on_message(self, message: discord.Message):
        """Called each time a message is posted"""
        if message.channel.id not in self.channel_ids:
            return

        # TODO

        # Update last date
        self.last_comment_date = message.created_at
