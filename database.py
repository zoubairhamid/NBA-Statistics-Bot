import nextcord
from nextcord.ext import commands
import sqlite3

database = sqlite3.connect('list.db')
cursor = database.cursor()
database.execute("CREATE TABLE IF NOT EXISTS items(item STRING, message_id INT)")


class db(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Add item to list", guild_ids=[1152819463805218866])
    async def add(self, interaction: nextcord.Interaction, message: str):

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (message, interaction.id))
        database.commit()

        await interaction.response.send_message("Message written to database!")

    @nextcord.slash_command(description="Delete item from list", guild_ids=[1152819463805218866])
    async def delete(self, interaction: nextcord.Interaction, message: str):

        query = "DELETE FROM items WHERE item = ?"
        cursor.execute(query, (message,))
        database.commit()

        await interaction.response.send_message("Message deleted from list!")

    @nextcord.slash_command(description="Read current list", guild_ids=[1152819463805218866])
    async def read(self, interaction: nextcord.Interaction):

        query = "SELECT * FROM items"
        data = cursor.execute(query).fetchall()
        string = ''
        for x in range(len(data)):
            string += str(x + 1) + ".) " + str(data[x][0]) + '\n'

        await interaction.response.send_message(string)

    @nextcord.slash_command(description="Edit an item on the list", guild_ids=[1152819463805218866])
    async def edit(self, interaction: nextcord.Interaction, message: str, new_message: str):

        query = "UPDATE items SET item = ? WHERE item = ?"
        cursor.execute(query, (new_message, message))
        database.commit()

        await interaction.response.send_message("Message edited in list!")


def setup(bot):
    bot.add_cog(db(bot))
