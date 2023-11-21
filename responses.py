import discord as discord
import nextcord
from nextcord.ext import commands
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import SeasonAll
from nba_api.stats.endpoints import playercareerstats
import pandas as pd


class responses(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong")

    @nextcord.slash_command(description="Greeting", guild_ids=[1152819463805218866])
    async def hello(self, interaction: nextcord.Interaction):

        await interaction.send("Hi")

    @nextcord.slash_command(description="Search for players per game averages", guild_ids=[1152819463805218866])
    async def regular_season_per_games(self, interaction: nextcord.Interaction, player_name: str, season: str):

        if not players.find_players_by_full_name(player_name):
            await interaction.send("No data found")
            return

        player_id = players.find_players_by_full_name(player_name)[0]['id']
        career = playercareerstats.PlayerCareerStats(player_id)

        d_career = career.get_dict()

        for key in d_career['resultSets']:
            for x in range(len(key['rowSet'])):
                if key['rowSet'][x][1] == season:
                    picture = "https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/" \
                              + str(player_id) + ".png"
                    ppg = str(round(key['rowSet'][x][26] / key['rowSet'][x][6], 2))
                    apg = str(round(key['rowSet'][x][21] / key['rowSet'][x][6], 2))
                    rpg = str(round(key['rowSet'][x][20] / key['rowSet'][x][6], 2))
                    spg = str(round(key['rowSet'][x][22] / key['rowSet'][x][6], 2))
                    bpg = str(round(key['rowSet'][x][23] / key['rowSet'][x][6], 2))
                    tpg = str(round(key['rowSet'][x][24] / key['rowSet'][x][6], 2))

                    player_info = ("**PPG**: " + ppg + "\n"
                                   + "**APG**: " + apg + "\n"
                                   + "**RPG**: " + rpg + "\n"
                                   + "**SPG**: " + spg + "\n"
                                   + "**BPG**: " + bpg + "\n"
                                   + "**TPG**: " + tpg + "\n")

                    embed = nextcord.Embed(colour=0xe74c3c, color=0xe74c3c, title=(player_name + ": " + season),
                                           type='rich', url=None, description=player_info, timestamp=None)
                    embed.set_image(picture)
                    await interaction.send(embed=embed)
                    return

        await interaction.send("No data found")

    @nextcord.slash_command(description="Search for players totals", guild_ids=[1152819463805218866])
    async def regular_season_totals(self, interaction: nextcord.Interaction, player_name: str, season: str):

        if not players.find_players_by_full_name(player_name):
            await interaction.send("No data found")
            return

        player_id = players.find_players_by_full_name(player_name)[0]['id']
        career = playercareerstats.PlayerCareerStats(player_id)

        d_career = career.get_dict()

        for key in d_career['resultSets']:
            for x in range(len(key['rowSet'])):
                if key['rowSet'][x][1] == season:
                    picture = "https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/" \
                              + str(player_id) + ".png"
                    points = str(round(key['rowSet'][x][26]))
                    assists = str(round(key['rowSet'][x][21]))
                    rebounds = str(round(key['rowSet'][x][20]))
                    steals = str(round(key['rowSet'][x][22]))
                    blocks = str(round(key['rowSet'][x][23]))
                    turnovers = str(round(key['rowSet'][x][24]))

                    player_info = ("**POINTS**: " + points + "\n"
                                   + "**ASSISTS**: " + assists + "\n"
                                   + "**REBOUNDS**: " + rebounds + "\n"
                                   + "**STEALS**: " + steals + "\n"
                                   + "**BLOCKS**: " + blocks + "\n"
                                   + "**TURNOVERS**: " + turnovers + "\n")

                    embed = nextcord.Embed(colour=0xe74c3c, color=0xe74c3c, title=(player_name + ": " + season),
                                           type='rich', url=None, description=player_info, timestamp=None)
                    embed.set_image(picture)
                    await interaction.send(embed=embed)
                    return

        await interaction.send("No data found")


def setup(bot: commands.Bot):
    bot.add_cog(responses(bot))

