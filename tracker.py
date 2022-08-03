from typing import TypedDict
from datetime import datetime
import json
import discord
from discord.ext import commands
from parser import is_X22, summary_msg, parse_keywords

date_format = '%d/%m/%Y %H:%M:%S'  # jj/mm/yyy hh:mm:ss


# data format of data files
class Data(TypedDict):
    date: str  # Data of last processed comment
    history: dict[str, int]  # [user_id, choice_index] pairs


class Tracker:

    def __init__(self, channel_ids: list[int], data_file_path: str, keywords_to_values: dict[str, str]):
        self.channel_ids = channel_ids  # channels to monitor

        # Loading data
        self.data_file_path = data_file_path
        self.last_comment_date = datetime(2022, 1, 1)  # default date
        self.history: dict[str, str] = {}
        self.read_data()

        # keywords
        self.keywords_to_values = keywords_to_values
        self.values = set(self.keywords_to_values.values())

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

        new_votes: dict[str, str] = {}

        for channel_id in self.channel_ids:
            channel = bot.get_channel(channel_id)

            messages: list[discord.Message] = await channel.history(after=self.last_comment_date).flatten()
            for message in messages:

                author_id = str(message.author.id)
                # Latest comment of this author is the first encountered
                if is_X22(message.author) and author_id not in new_votes:

                    # keyword = parse_keyword(message.content, prefix='1')
                    keywords = parse_keywords(message.content, prefix='1', n=3)
                    value = self.first_value(keywords)
                    if value is not None:
                        new_votes[author_id] = value
                    """
                    if keyword is not None:  # at this point, it is not garanteed that the 'keyword' is valid
                       value = self.keywords_to_values.get(keyword)
                       if value is not None:
                            new_votes[author_id] = value
                    """

            if messages[0].created_at > new_comment_date:
                new_comment_date = messages[0].created_at

            print(len(messages), "messages loaded")

        self.history = self.history | new_votes  # merge votes. new_votes overwrite old votes
        self.last_comment_date = new_comment_date

    async def on_message(self, message: discord.Message) -> bool:
        """Called each time a message is posted
        @:returns True if something changed"""

        if message.channel.id not in self.channel_ids or not is_X22(message.author):
            return False

        print("new comment")

        something_changed = False

        # keyword = parse_keyword(message.content, prefix='1')
        keywords = parse_keywords(message.content, prefix='1', n=3)
        value = self.first_value(keywords)
        if value is not None:
            # Add or overwrite value for this user
            something_changed = True
            self.history[str(message.author.id)] = value

        """
        if keyword is not None:
            value = self.keywords_to_values.get(keyword)

            if value is not None:
                # Add or overwrite value for this user
                something_changed = True
                self.history[str(message.author.id)] = value
        """
        # Update last date
        self.last_comment_date = message.created_at
        return something_changed

    async def on_exit(self):
        """Save data and quit"""
        new_data = {'history': self.history, 'date': self.last_comment_date.strftime(date_format)}

        file = open(self.data_file_path, 'w')
        file.write(json.dumps(new_data, sort_keys=True, indent=4))
        file.close()

        print("one tracker exited")

    def summary_msg(self) -> str:
        return summary_msg(self.history, self.values)

    def first_value(self, keywords: list[str]) -> str | None:
        """Find the first valid value in a list of keywords"""

        if len(keywords) == 0:
            return None

        # Find the first valid keyword
        i = 0
        while i < len(keywords) and keywords[i] not in self.keywords_to_values:
            i += 1

        if i == len(keywords):  # No valid value
            return None

        return self.keywords_to_values[keywords[i]]
