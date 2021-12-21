import discord
import shutil
import re

from discord.ext import commands
from Tools.utils import getConfig, getGuildPrefix, guild_owner_only, updateConfig


class onRemove(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_remove(self, member):

        if member.bot:
            return

        ID = member.id
        folderPath = f"captchaFolder/{member.guild.id}/captcha_{ID}"
        try:
            os.mkdir(folderPath)
        except:
            if os.path.isdir(f"captchaFolder/{member.guild.id}") is False:
                os.mkdir(f"captchaFolder/{member.guild.id}")
            if os.path.isdir(folderPath) is True:
                shutil.rmtree(folderPath)
            os.mkdir(folderPath)


def setup(client):
    client.add_cog(onRemove(client))