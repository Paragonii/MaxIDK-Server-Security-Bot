import discord
import json
import asyncio
import platform
import random
import pytz

from Tools.utils import getConfig, getGuildPrefix, guild_owner_only, updateConfig
from discord.ext import commands
from discord.utils import get
from discord import Client

from datetime import datetime
from datetime import date


class RoleManagement(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["jr"])
    async def joinrole(self, ctx, addORremove=None, role: discord.Role = None):

        data = getConfig(ctx.guild.id)

        if addORremove == "?add":
            if role == None:
                return await ctx.send("Please mention a role!")

            if role.id in data["joinroles"]:
                return await ctx.send("This role is already set as a joinrole!")

            else:
                data["joinrole"] = True
                data["joinroles"].append(role.id)

                updateConfig(ctx.guild.id, data)
                prefix = data["prefix"]
                embed = discord.Embed(title="Join Roles",
                                      description=f"`{prefix}jr ?add <role>` - Adds roles\n"
                                                  f"`{prefix}jr ?remove <role>` - Removes roles",
                                      colour=discord.Colour.blue())
                rolesinjoinroles = data["joinroles"]

                result = ' '
                for i in rolesinjoinroles:
                    role2 = get(ctx.guild.roles, id=i)
                    if role2 == None:
                        role3 = '*Unable to Fetch Name*'
                    else:
                        role3 = role2.mention
                    result += f"{role3} ||`{i}`||\n"

                embed.add_field(name="Roles",
                                value=f"The following roles will be added to every user joining this server: \n"
                                      f"{result}")
                await ctx.send(embed=embed)

        if addORremove == "?remove":
            if role == None:
                return await ctx.send("Please mention a role!")

            if role.id not in data["joinroles"]:
                return await ctx.send("This role is not set as a joinrole!")

            else:
                data["joinroles"].remove(role.id)
                if data["joinroles"] == []:
                    data["joinrole"] = False

                updateConfig(ctx.guild.id, data)
                prefix = data["prefix"]
                embed = discord.Embed(title="Join Roles",
                                      description=f"`{prefix}jr ?add <role>` - Adds roles\n"
                                                  f"`{prefix}jr ?remove <role>` - Removes roles",
                                      colour=discord.Colour.blue())
                rolesinjoinroles = data["joinroles"]

                result = ' '
                for i in rolesinjoinroles:
                    role2 = get(ctx.guild.roles, id=i)
                    if role2 == None:
                        role3 = '*Unable to Fetch Name*'
                    else:
                        role3 = role2.mention
                    result += f"{role3} ||`{i}`||\n"

                embed.add_field(name="Roles",
                                value=f"The following roles will be added to every user joining this server: \n"
                                      f"{result}")

                await ctx.send(embed=embed)

        if addORremove == None:
            data = getConfig(ctx.guild.id)
            prefix = data["prefix"]
            embed = discord.Embed(title="Join Roles",
                                  description=f"`{prefix}jr ?add <role>` - Adds roles\n"
                                              f"`{prefix}jr ?remove <role>` - Removes roles",
                                  colour=discord.Colour.blue())
            rolesinjoinroles = data["joinroles"]
            result = ' '
            for i in rolesinjoinroles:
                role2 = get(ctx.guild.roles, id=i)
                if role2 == None:
                    role3 = '*Unable to Fetch Name*'
                else:
                    role3 = role2.mention
                result += f"{role3} ||`{i}`||\n"

            if data["joinroles"] == []:
                embed.add_field(name="Roles",
                                value=f"The following roles will be added to every user joining this server: \n"
                                      f"*None*")
            else:
                embed.add_field(name="Roles",
                                value=f"The following roles will be added to every user joining this server: \n"
                                      f"{result}")

            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(RoleManagement(client))