import discord
from discord.ext import commands
import re
from Tools.utils import getConfig, getGuildPrefix, updateConfig
import asyncio
import json
from discord.utils import get


class Setup(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(usage="<kick/ban/none>",
                      name="punishment",
                      description="Sets the Anti-Nuke Punishment")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    @commands.guild_only()
    async def punishment(self, ctx, kickOrBan):
        data = getConfig(ctx.guild.id)
        owner = data["owner"]
        admin = data["administrator"]
        if ctx.author.id == owner or admin:

            kickOrBan = kickOrBan.lower()

            if kickOrBan == "kick":
                data = getConfig(ctx.guild.id)
                data["punishment"] = "kick"

                await ctx.send(f"Punishment: {kickOrBan}")

                updateConfig(ctx.guild.id, data)


            elif kickOrBan == "ban":
                data = getConfig(ctx.guild.id)
                data["punishment"] = "ban"

                await ctx.send(f"Punishment: {kickOrBan}")

                updateConfig(ctx.guild.id, data)


            elif kickOrBan == "none":
                data = getConfig(ctx.guild.id)
                data["punishment"] = "none"

                await ctx.send(f"Punishment: {kickOrBan}")

                updateConfig(ctx.guild.id, data)

        else:
            await ctx.send("Only the owner or a selected administrator can use this command!")

    @commands.command(usage="<member>",
                      name="whitelist",
                      description="Adds member to the server whitelist")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    @commands.guild_only()
    async def whitelist(self, ctx, member: discord.Member = None):
        try:
            data = getConfig(ctx.guild.id)
            owner = data["owner"]
            admin = data["administrator"]
            if ctx.author.id == owner or admin:
                if member == None:
                    return await ctx.send("Please mention a member to whitelist!")
                if member.id == 882901345466724373:
                    return await ctx.send("You can not whitelist me!")
                else:
                    data = getConfig(ctx.guild.id)
                    whitelisted = data["whitelist"]
                    if member.id in whitelisted:
                        return await ctx.send("This user is already whitelisted!")
                    else:
                        data = getConfig(ctx.guild.id)
                        data["whitelist"].append(member.id)
                        await ctx.send(f"Whitelisted: {member.mention}")
                        updateConfig(ctx.guild.id, data)
            else:
                await ctx.send("Only the owner or a selected administrator can use this command!")
        except:
            pass

    @commands.command(usage="<member>",
                      name="unwhitelist",
                      description="Removes member from the server whitelist")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    @commands.guild_only()
    async def unwhitelist(self, ctx, member: discord.Member = None):
        try:
            data = getConfig(ctx.guild.id)
            owner = data["owner"]
            admin = data["administrator"]
            if ctx.author.id == owner or admin:
                if member == None:
                    return await ctx.send("Please mention a member to unwhitelist!")
                if member.id == 882901345466724373:
                    return await ctx.send("You can not whitelist me!")
                else:
                    data = getConfig(ctx.guild.id)
                    whitelisted = data["whitelist"]
                    if member.id not in whitelisted:
                        return await ctx.send("This user is not in whitelisted!")
                    else:
                        data = getConfig(ctx.guild.id)
                        data["whitelist"].remove(member.id)
                        await ctx.send(f"Unwhitelisted: {member.mention}")
                        updateConfig(ctx.guild.id, data)
            else:
                await ctx.send("Only the owner or a selected administrator can use this command!")
        except:
            pass

    @commands.command(name="whitelisted",
                      description="Shows you the current server whitelist")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    @commands.guild_only()
    async def whitelisted(self, ctx):
        prefix = await getGuildPrefix(self.client, ctx)
        try:
            data = getConfig(ctx.guild.id)
            whitelisted = data["whitelist"]
            owner = data["owner"]
            admin = data["administrator"]
            if ctx.author.id in whitelisted or owner or admin:
                loading = await ctx.send("Searching...")
                result = ' '
                data = getConfig(ctx.guild.id)
                userinwhitelist = data["whitelist"]
                for i in userinwhitelist:
                    user2 = self.client.get_user(i)
                    if user2 == None:
                        user = 'Unable to Fetch Name'
                    else:
                        user = user2.mention
                    result += f"{user}: {i}\n"
                await loading.delete()
                if data["whitelist"] == []:
                    return await ctx.send(f"There are no whitelisted users in this server, do `{prefix}whitelist <user>` to whitelist a user of your choice!")
                else:
                    embed = discord.Embed(title=f'Whitelisted users for {ctx.guild.name}', description=result,
                                          color=discord.Colour.blue())
                    await ctx.send(embed=embed)

            else:
                return await ctx.send("Only the server owner or whitelisted user can use this command!")
        except:
            pass

    @commands.command(name="verifiedrole",
                      description="Changes/Sets the Verified Role ")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    @commands.guild_only()
    async def verifiedrole(self, ctx, roleId):
        try:
            data = getConfig(ctx.guild.id)
            owner = data["owner"]
            admin = data["administrator"]
            if ctx.author.id == owner or admin:
                roleId = int(roleId)
                data = getConfig(ctx.guild.id)
                data["roleGivenAfterCaptcha"] = roleId

                updateConfig(ctx.guild.id, data)

                await ctx.send("<@&{0}> will be given after that the captcha be passed.".format(roleId))

            else:
                await ctx.send("Only the owner or a selected administrator can use this command!")

        except Exception:
            pass
            data = getConfig(ctx.guild.id)
            owner = data["owner"]
            admin = data["administrator"]
            if ctx.author.id == owner or admin:
                roleId = roleId.lower()
                if roleId == "off":
                    data = getConfig(ctx.guild.id)
                    roleGivenAfterCaptcha = get(ctx.guild.roles, id=data["roleGivenAfterCaptcha"])
                    await roleGivenAfterCaptcha.delete()
                    data["roleGivenAfterCaptcha"] = False

                    updateConfig(ctx.guild.id, data)
                    await ctx.send("The captcha role has been successfully reset")

            else:
                await ctx.send("Only the owner or a selected administrator can use this command!")

    @commands.group(invoke_without_command=True,
                    description="Shows you the setup modules")
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx):

        perms = ctx.me.guild_permissions
        if not (perms.administrator):
            return await ctx.send("Sorry but I would need the administrator permissions to continue!")

        emote = ("<:rightArrow:904016483108143115>")
        alarm = ("🚨")
        shild = ("🛡️")
        filter = ("🚫")
        verify = ("📝")
        auto = ("🤖")
        raid = ("🔒")
        data = getConfig(ctx.guild.id)
        prefix = data["prefix"]
        embed = discord.Embed(title=f"Setup {self.client.user.name}",
                              description=f"With some powerful features, Server Security will be able to protect your server from being nuked, raided, malicous users, spammer etc. and still it gives you additional features, such as some moderation commands. Make sure the bot has the highest possible role on your server. Don't give it a higher role! Move the role it created higher! Also the bot won't function without having the Administrator permission.\nFor more information about Server Security's features `{prefix}features`",
                              colour=discord.Colour.blue())
        embed.add_field(name=f"{verify} Setup Captcha-Verification", value=f"{emote} `{prefix}setup captcha`")
        embed.add_field(name=f"{shild} Setup Anti-Nuke", value=f"{emote} `{prefix}setup antinuke`")
        embed.add_field(name=f"{filter} Setup Join-Filter", value=f"{emote} `{prefix}setup joinfilter`")
        embed.add_field(name=f"{auto} Setup Auto-Moderation", value=f"{emote} `{prefix}automoderation`")
        embed.add_field(name=f"{alarm} Enable Panic-Mode", value=f"{emote} `{prefix}panicmode <on>`")
        embed.add_field(name=f"{raid} Enable Raid-Mode", value=f"{emote} `{prefix}raidmode <on>`")
        await ctx.send(embed=embed)

    @setup.command()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def captcha(self, ctx):

        perms = ctx.me.guild_permissions
        if not (perms.administrator):
            return await ctx.send("Sorry but I would need the administrator permissions to continue!")

        data = getConfig(ctx.guild.id)
        owner = data["owner"]
        administrator = data["administrator"]
        if ctx.author.id == owner or administrator:
            loading = await ctx.channel.send("Setting up Captcha-Verification...")

            # Data
            data = getConfig(ctx.guild.id)

            # Create role
            temporaryRole = await ctx.guild.create_role(name="unverified")
            # Hide all channels
            for channel in ctx.guild.channels:
                if isinstance(channel, discord.TextChannel):

                    perms = channel.overwrites_for(temporaryRole)
                    perms.read_messages = False
                    await channel.set_permissions(temporaryRole, overwrite=perms)

                elif isinstance(channel, discord.VoiceChannel):

                    perms = channel.overwrites_for(temporaryRole)
                    perms.read_messages = False
                    perms.connect = False
                    await channel.set_permissions(temporaryRole, overwrite=perms)

            # Create Role after Captcha
            if data["roleGivenAfterCaptcha"] is False:
                roleGivenAfterCaptcha = await ctx.guild.create_role(name="Verified", colour=discord.Colour.blue())
            else:
                pass

            # Create captcha channel
            captchaChannel = await ctx.guild.create_text_channel('verify-here')

            perms = captchaChannel.overwrites_for(temporaryRole)
            perms.read_messages = True
            perms.send_messages = True
            await captchaChannel.set_permissions(temporaryRole, overwrite=perms)

            perms = captchaChannel.overwrites_for(ctx.guild.default_role)
            perms.read_messages = False
            await captchaChannel.set_permissions(ctx.guild.default_role, overwrite=perms)
            prefix = await getGuildPrefix(self.client, ctx)
            embed = discord.Embed(title=f"Welcome to {ctx.guild.name}", colour=discord.Colour.blue())
            embed.add_field(name="Verify",
                            value=f"If you want to verify yourself on this server write `{prefix}verify`", inline=False)
            embed.add_field(name="Why?",
                            value="This is to protect our server from malicious raids using automoated bots and malicious users!")
            embed.set_thumbnail(url=ctx.guild.icon_url)
            await captchaChannel.send(embed=embed)

            if data["captchaLog"] is False:
                captchaLog = await ctx.guild.create_text_channel('captcha-logs')

                perms = captchaLog.overwrites_for(ctx.guild.default_role)
                perms.read_messages = False
                await captchaLog.set_permissions(ctx.guild.default_role, overwrite=perms)

                data["captchaLog"] = captchaLog.id

            # Edit configuration.json
            # Add modifications
            data["captcha"] = True
            data["temporaryRole"] = temporaryRole.id
            data["roleGivenAfterCaptcha"] = roleGivenAfterCaptcha.id
            data["captchaChannel"] = captchaChannel.id

            updateConfig(ctx.guild.id, data)

            await loading.delete()
            embed = discord.Embed(title="Setup successfully", description=f"I have successfully setup the Captcha-Verification feature.", colour=discord.Colour.blue())
            await ctx.send(embed=embed)

        else:
            await ctx.send("Only the owner or a selected administrator can use this command!")


    @commands.command(name="captcha",
                      description="Disables the Captcha-Verification feature")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def _captcha(self, ctx, off):
        data = getConfig(ctx.guild.id)
        owner = data["owner"]
        administrator = data["administrator"]
        if ctx.author.id == owner or administrator:
            if off == "off":
                loading = await ctx.channel.send("Deletion of captcha protection...")
                data = getConfig(ctx.guild.id)
                data["captcha"] = False

                noDeleted = []

                try:
                    temporaryRole = get(ctx.guild.roles, id=data["temporaryRole"])
                    await temporaryRole.delete()

                except:
                    noDeleted.append("temporaryRole")
                try:
                    captchaChannel = self.client.get_channel(data["captchaChannel"])
                    await captchaChannel.delete()
                except:
                    noDeleted.append("captchaChannel")
                try:
                    captchaLog = self.client.get_channel(data["captchaLog"])
                    await captchaLog.delete()
                except:
                    noDeleted.append("captchaLog")
                try:
                    roleGivenAfterCaptcha = get(ctx.guild.roles, id=data["roleGivenAfterCaptcha"])
                    await roleGivenAfterCaptcha.delete()
                except:
                    noDeleted.append("roleGivenAfterCaptcha")

                # Add modifications
                data["captchaChannel"] = False
                data["captchaLog"] = False
                data['temporaryRole'] = False
                data["roleGivenAfterCaptcha"] = False

                # Edit configuration.json
                updateConfig(ctx.guild.id, data)

                await loading.delete()
                await ctx.send("The captcha was deleted with success.")

                if len(noDeleted) > 0:
                    await ctx.send("Error(s) detected during the deletion of the `{0}`.".format(errors))

        else:
            await ctx.send("Only the owner or a selected administrator can use this command!")

    @setup.command()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def antinuke(self, ctx):

        perms = ctx.me.guild_permissions
        if not (perms.administrator):
            return await ctx.send("Sorry but I would need the administrator permissions to continue!")

        data = getConfig(ctx.guild.id)
        owner = data["owner"]
        administrator = data["administrator"]
        if ctx.author.id == owner or administrator:
            loading = await ctx.send("Setting up Anti-Nuke protection...")
            data = getConfig(ctx.guild.id)
            data["antinuke"] = True

            if data["logChannel"] is False:
                logChannel = await ctx.guild.create_text_channel(f"{self.client.user.name}-logs")

                perms = logChannel.overwrites_for(ctx.guild.default_role)
                perms.read_messages = False
                await logChannel.set_permissions(ctx.guild.default_role, overwrite=perms)

                data["logChannel"] = logChannel.id

                updateConfig(ctx.guild.id, data)
                await loading.delete()

                prefix = await getGuildPrefix(self.client, ctx)
                embed = discord.Embed(title=f"Setup successfully", description=f"I have successfully setup the Anti-Nuke feature.\n\n"
                                                                               f"**Whitelist:**\nYou should whitelist some members, do `{prefix}whitelist <user>`", colour=discord.Colour.blue())
                await ctx.send(embed=embed)

        else:
            await ctx.send("Only the owner or a selected administrator can use this command!")

    @commands.command(name="antinuke",
                      description="Disables the Anti-Nuke feature")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def _antinuke(self, ctx, off):
        data = getConfig(ctx.guild.id)
        owner = data["owner"]
        administrator = data["administrator"]

        if ctx.author.id == owner or administrator:
            if off == "off":
                loading = await ctx.channel.send("Deletion of the Anti-Nuke protection...")
                data = getConfig(ctx.guild.id)
                data["antinuke"] = False
                if data["joinfilter"] is False:
                    if data["panicmode"] is False:
                        if data["panicmode"] is False:
                            logChannel = self.client.get_channel(data["logChannel"])
                            await logChannel.delete()

                            data["logChannel"] = False

                updateConfig(ctx.guild.id, data)
                await loading.delete()
                await ctx.send("Anti-Nuke protection disabled!")

        else:
            await ctx.send("Only the owner or a selected administrator can use this command!")

    @setup.command()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def joinfilter(self, ctx):

        perms = ctx.me.guild_permissions
        if not (perms.administrator):
            return await ctx.send("Sorry but I would need the administrator permissions to continue!")

        data = getConfig(ctx.guild.id)
        owner = data["owner"]
        administrator = data["administrator"]

        if ctx.author.id == owner or administrator:
            loading = await ctx.send("Setting up the Join-Filter...")

            data = getConfig(ctx.guild.id)
            data["joinfilter"] = True
            data["botfilter"] = True
            data["avatarfilter"] = True
            data["checknew"] = True

            if data["logChannel"] is False:
                logChannel = await ctx.guild.create_text_channel(f"{self.client.user.name}-logs")

                perms = logChannel.overwrites_for(ctx.guild.default_role)
                perms.read_messages = False
                await logChannel.set_permissions(ctx.guild.default_role, overwrite=perms)

                data["logChannel"] = logChannel.id


            updateConfig(ctx.guild.id, data)
            await loading.delete()

            embed = discord.Embed(title="Setup successfully", description=f"I have successfully setup the Join-Filter feature.\n\n"
                                                                          f"**Note:**\nThe maximum points are standard set to 25", colour=discord.Colour.blue())
            await ctx.send(embed=embed)
        else:
            await ctx.send("Only the owner or a selected administrator can use this command!")

    @commands.command(name="joinfilter",
                      description="Disables the Join-Filter feature")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def _joinfilter(self, ctx, off):
        data = getConfig(ctx.guild.id)
        owner = data["owner"]
        administrator = data["administrator"]

        if ctx.author.id == owner or administrator:
            if off == "off":
                loading = await ctx.send("Deletion of the Join-Filter...")

                data = getConfig(ctx.guild.id)
                data["joinfilter"] = False
                data["botfilter"] = False
                data["avatarfilter"] = False
                data["checknew"] = False

                if data["antinuke"] is False:
                    if data["panicmode"] is False:
                        if data["panicmode"] is False:
                            logChannel = self.client.get_channel(data["logChannel"])
                            await logChannel.delete()

                            data["logChannel"] = False

                updateConfig(ctx.guild.id, data)

                await loading.delete()
                await ctx.send("Join-Filter disabled!")

        else:
            await ctx.send("Only the owner or a selected administrator can use this command!")

    @setup.command()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def automoderation(self, ctx):

        perms = ctx.me.guild_permissions
        if not (perms.administrator):
            return await ctx.send("Sorry but I would need the administrator permissions to continue!")

        data = getConfig(ctx.guild.id)
        owner = data["owner"]
        administrator = data["administrator"]

        if ctx.author.id == owner or administrator:
            loading = await ctx.send("Setting up Auto-Moderation...")
            data = getConfig(ctx.guild.id)
            data["automoderation"] = True
            data["antiSpam"] = True
            data["antiWord"] = True
            data["antiLink"] = True
            data["antighost"] = True

            updateConfig(ctx.guild.id, data)
            await loading.delete()

            embed = discord.Embed(title=f"Setup successfully", description=f"I have successfully setup the Auto-Moderation feature.", colour=discord.Colour.blue())
            await ctx.send(embed=embed)

        else:
            await ctx.send("Only the owner or a selected administrator can use this command!")

    @commands.command(name="automoderation",
                      description="Disables the Auto-Moderation feature")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def _automoderation(self, ctx, off):
        data = getConfig(ctx.guild.id)
        owner = data["owner"]
        administrator = data["administrator"]

        if ctx.author.id == owner or administrator:
            if off == "off":
                loading = await ctx.send("Deletion of the Auto-Moderation System...")
                data = getConfig(ctx.guild.id)
                data["automoderation"] = False
                data["antiSpam"] = False
                data["antiWord"] = False
                data["antiLink"] = False
                data["antighost"] = False

                await loading.delete()
                await ctx.send("Auto-Moderation disabled!")
                updateConfig(ctx.guild.id, data)

        else:
            await ctx.send("Only the owner or a selected administrator can use this command!")

    @commands.command(description="Enables or disable the Bot-Filter Module")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def botfilter(self, ctx, onOroff):
        data = getConfig(ctx.guild.id)
        owner = data["owner"]
        administrator = data["administrator"]

        if ctx.author.id == owner or administrator:

            onOroff = onOroff.lower()

            if onOroff == "on":
                if data["botfilter"] == True:
                    await ctx.send("Bot-Filter already enabled!")
                    data = getConfig(ctx.guild.id)
                    data["botfilter"] = True
                else:
                    data["botfilter"] = True
                    if data["joinfilter"] is not True:
                        data["joinfilter"] = True

                await ctx.send(f"Bot-Filter enabled!")

                updateConfig(ctx.guild.id, data)


            elif onOroff == "off":
                data = getConfig(ctx.guild.id)
                data["botfilter"] = False
                if data["avatarfilter"] is False:
                    if data["autoban"] is False:
                        if data["checknew"] is False:
                            data["joinfilter"] = False

                await ctx.send(f"Bot-Filter disabled!")

                updateConfig(ctx.guild.id, data)

        else:
            await ctx.send("Only the owner or a selected administrator can use this command!")

    @commands.command(description="Enables or disable the Avatar-Filter Module")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def avatarfilter(self, ctx, onOroff):
        data = getConfig(ctx.guild.id)
        owner = data["owner"]
        administrator = data["administrator"]

        if ctx.author.id == owner or administrator:

            onOroff = onOroff.lower()

            if onOroff == "on":
                if data["avatarfilter"] == True:
                    await ctx.send("Avatar-Filter already enabled!")
                    data = getConfig(ctx.guild.id)
                    data["avatarfilter"] = True
                else:
                    data["avatarfilter"] = True
                    if data["joinfilter"] is not True:
                        data["joinfilter"] = True

                await ctx.send(f"Avatar-Filter enabled!")

                updateConfig(ctx.guild.id, data)


            elif onOroff == "off":
                data = getConfig(ctx.guild.id)
                data["avatarfilter"] = False
                if data["botfilter"] is False:
                    if data["autoban"] is False:
                        if data["checknew"] is False:
                            data["joinfilter"] = False

                await ctx.send(f"Avatar-Filter disabled!")

                updateConfig(ctx.guild.id, data)

        else:
            await ctx.send("Only the owner or a selected administrator can use this command!")

    @commands.command(description="Sets the punishment when someone does not pass the captcha")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def captchapunishment(self, ctx, kickOrban):
        data = getConfig(ctx.guild.id)
        owner = data["owner"]
        administrator = data["administrator"]

        if ctx.author.id == owner or administrator:
            kickOrban = kickOrban.lower()

            if kickOrban == "kick":
                data = getConfig(ctx.guild.id)
                data["captchapunishment"] = "kick"

                await ctx.send(f"New Captcha-Punishment: {kickOrban}")

                updateConfig(ctx.guild.id, data)

            if kickOrban == "ban":
                data = getConfig(ctx.guild.id)
                data["captchapunishment"] = "ban"

                await ctx.send(f"New Captcha-Punishment: {kickOrban}")

                updateConfig(ctx.guild.id, data)

            if kickOrban == "none":
                kickOrban = "None"
                data = getConfig(ctx.guild.id)
                data["captchapunishment"] = False

                await ctx.send(f"New Captcha-Punishment: {kickOrban}")

                updateConfig(ctx.guild.id, data)

        else:
            await ctx.send("Only the owner or a selected administrator can use this command!")

    @commands.command(name="antispam",
                      description="Enables or disable the Anti-Spam Module")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def antispam(self, ctx, onOroff):

        onOroff = onOroff.lower()

        data = getConfig(ctx.guild.id)
        owner = data["owner"]
        administrator = data["administrator"]

        if ctx.author.id == owner or administrator:
            if onOroff == "on":
                if data["antiSpam"] is True:
                    await ctx.send("Anti-Spam already enabled!")
                else:
                    data["antiSpam"] = True
                    if data["automoderation"] is not True:
                        data["automoderation"] = True

                    updateConfig(ctx.guild.id, data)
                    await ctx.send("Anti-Spam enabled!")

            if onOroff == "off":
                data = getConfig(ctx.guild.id)
                data["antiSpam"] = False
                if data["antiWord"] is False:
                    if data["antiLink"] is False:
                        if data["antighost"] is False:
                            data["automoderation"] = False

                updateConfig(ctx.guild.id, data)
                await ctx.send("Anti-Spam disabled!")

        else:
            await ctx.send("Only the owner or a selected administrator can use this command!")

    @commands.command(name="antiword",
                      description="Enables or disable the Anti-Word Module")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def antiword(self, ctx, onOroff):

        onOroff = onOroff.lower()

        data = getConfig(ctx.guild.id)
        owner = data["owner"]
        administrator = data["administrator"]

        if ctx.author.id == owner or administrator:
            if onOroff == "on":
                if data["antiWord"] is True:
                    await ctx.send("Anti-Word already enabled!")
                else:
                    data["antiWord"] = True
                    if data["automoderation"] is not True:
                        data["automoderation"] = True

                    updateConfig(ctx.guild.id, data)
                    await ctx.send("Anti-Word enabled!")

            if onOroff == "off":
                data = getConfig(ctx.guild.id)
                data["antiWord"] = False
                if data["antiSpam"] is False:
                    if data["antiLink"] is False:
                        if data["antighost"] is False:
                            data["automoderation"] = False

                updateConfig(ctx.guild.id, data)
                await ctx.send("Anti-Word disabled!")

        else:
            await ctx.send("Only the owner or a selected administrator can use this command!")

    @commands.command(name="antilink",
                      description="Enables or disable the Anti-Link Module")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def antilink(self, ctx, onOroff):

        onOroff = onOroff.lower()

        data = getConfig(ctx.guild.id)
        owner = data["owner"]
        administrator = data["administrator"]

        if ctx.author.id == owner or administrator:
            if onOroff == "on":
                if data["antiLink"] is True:
                    await ctx.send("Anti-Link already enabled!")
                else:
                    data["antiLink"] = True
                    if data["automoderation"] is not True:
                        data["automoderation"] = True

                updateConfig(ctx.guild.id, data)
                await ctx.send("Anti-Link enabled!")

            if onOroff == "off":
                data = getConfig(ctx.guild.id)
                data["antiLink"] = False
                if data["antiSpam"] is False:
                    if data["antiWord"] is False:
                        if data["antighost"] is False:
                            data["automoderation"] = False

                updateConfig(ctx.guild.id, data)
                await ctx.send("Anti-Link disabled!")

        else:
            await ctx.send("Only the owner or a selected administrator can use this command!")

    @commands.command(name="antighost",
                      description="Enables or disable the Anti-Ghost Module")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def antighost(self, ctx, onOroff):

        onOroff = onOroff.lower()

        data = getConfig(ctx.guild.id)
        owner = data["owner"]
        administrator = data["administrator"]

        if ctx.author.id == owner or administrator:
            if onOroff == "on":
                if data["antighost"] is True:
                    await ctx.send("Anti-Ghost Ping already enabled!")
                else:
                    data["antighost"] = True
                    if data["automoderation"] is not True:
                        data["automoderation"] = True

                updateConfig(ctx.guild.id, data)
                await ctx.send("Anti-Ghost Ping enabled!")

            if onOroff == "off":
                data = getConfig(ctx.guild.id)
                data["antighost"] = False
                if data["antiSpam"] is False:
                    if data["antiWord"] is False:
                        if data["antiLink"] is False:
                            data["automoderation"] = False

                updateConfig(ctx.guild.id, data)
                await ctx.send("Anti-Ghost Ping disabled!")

        else:
            await ctx.send("Only the owner or a selected administrator can use this command!")

    @commands.command(description="Enables or disable the Panic-Mode")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def panicmode(self, ctx, onORoff):
        data = getConfig(ctx.guild.id)
        owner = data["owner"]
        administrator = data["administrator"]

        if ctx.author.id == owner or administrator:
            if onORoff == "on":
                data = getConfig(ctx.guild.id)
                data["panicmode"] = True
                data["antinuke"] = True
                data["automoderation"] = True
                data["joinfilter"] = True
                data["botfilter"] = True
                data["avatarfilter"] = True
                data["checknew"] = True
                data["antiSpam"] = True
                data["antiLink"] = True
                data["antiWord"] = True

                mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

                if not mutedRole:
                    mutedRole = await ctx.guild.create_role(name="Muted")

                    for channel in ctx.guild.channels:
                        await channel.set_permissions(mutedRole, speak=False, send_messages=False,
                                                      read_message_history=True,
                                                      read_messages=False)

                if data["logChannel"] is False:
                    logChannel = await ctx.guild.create_text_channel(f"{self.client.user.name}-logs")

                    perms = logChannel.overwrites_for(ctx.guild.default_role)
                    perms.read_messages = False
                    await logChannel.set_permissions(ctx.guild.default_role, overwrite=perms)

                    data["logChannel"] = logChannel.id


                updateConfig(ctx.guild.id, data)
                embed = discord.Embed(title="Enabled successfully", description=f"I have successfully enabled the Panic-Mode feature.", colour=discord.Colour.blue())
                await ctx.send(embed=embed)

            if onORoff == "off":
                data = getConfig(ctx.guild.id)
                data["panicmode"] = False
                data["antinuke"] = False
                data["automoderation"] = False
                data["joinfilter"] = False
                data["botfilter"] = False
                data["avatarfilter"] = False
                data["checknew"] = False
                data["antiSpam"] = False
                data["antiLink"] = False
                data["antiWord"] = False
                if data["panicmode"] is False:
                    if data["antinuke"] is False:
                        if data["joinfilter"] is False:
                            logChannel = self.client.get_channel(data["logChannel"])
                            await logChannel.delete()

                            data["logChannel"] = False


                updateConfig(ctx.guild.id, data)
                await ctx.send("Panic-Mode disabled! (Also the Anti-Nuke Feature has been disabled!)")

        else:
            await ctx.send("Only the owner or a selected administrator can use this command!")

    @commands.command(description="Sets the Panic-Mode punishment")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def panicpunishment(self, ctx, punishment):
        data = getConfig(ctx.guild.id)
        owner = data["owner"]
        administrator = data["administrator"]

        if ctx.author.id == owner or administrator:

            punishment = punishment.lower()

            if punishment == "kick":
                data = getConfig(ctx.guild.id)
                data["panicpunishment"] = "kick"

                await ctx.send(f"New Panic-Mode punishment: Kick")
                updateConfig(ctx.guild.id, data)

            if punishment == "ban":
                data = getConfig(ctx.guild.id)
                data["panicpunishment"] = "ban"

                await ctx.send("New Panic-Mode punishment: Ban")
                updateConfig(ctx.guild.id, data)

            if punishment == "mute":
                data = getConfig(ctx.guild.id)
                data["panicpunishment"] = "mute"

                await ctx.send(f"New Panic-Mode punishment: Mute")
                updateConfig(ctx.guild.id, data)

        else:
            await ctx.send("Only the owner or a selected administrator can use this command!")

    @commands.command(description="Sets the administrator who can use all of my commands")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def administrator(self, ctx, member: discord.Member = None):
        try:
            data = getConfig(ctx.guild.id)
            owner = data["owner"]
            if ctx.author.id == owner:
                if member == None:
                    return await ctx.send("Please mention a member!")
                else:
                    data = getConfig(ctx.guild.id)
                    data["administrator"] = member.id
                    await ctx.send(f"{member.mention} can now use all of my commands!")
                    updateConfig(ctx.guild.id, data)

            else:
                await ctx.send("Only the owner can use this command!")

        except:
            pass

    @commands.command(description="Reset the administrator who can use all of my commands")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def unadministrator(self, ctx, member: discord.Member = None):
        try:
            data = getConfig(ctx.guild.id)
            owner = data["owner"]
            if ctx.author.id == owner:
                if member == None:
                    return await ctx.send("Please mention a member!")
                else:
                    data = getConfig(ctx.guild.id)
                    data["administrator"] = False
                    await ctx.send(f"From now on, {member.mention} can no longer use any setup commands etc.")
                    updateConfig(ctx.guild.id, data)

            else:
                await ctx.send("Only the owner can use this command!")
        except:
            pass

    @commands.command(description="Enables or disables the Auto-Ban Module")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def autoban(self, ctx, onOroff):

        onOroff = onOroff.lower()

        data = getConfig(ctx.guild.id)
        owner = data["owner"]
        if ctx.author.id == owner:
            if onOroff == 'on':
                if data["autoban"] is True:
                    await ctx.send("Auto-Ban already enabled!")
                else:
                    embed = discord.Embed(title="Server Security Auto-Ban Function",
                                          description=f"Are you sure you want to enable the Auto-Ban function? **I recommend activating it only in emergency situations!**\n\n"
                                                      f'If you want to enable it write **"yes"** else **"no"**', colour=discord.Colour.blue())
                    await ctx.send(embed=embed)

                    def check(message):
                        if message.author == ctx.author and message.content in ["yes", "no"]:
                            return message.content

                    try:
                        msg = await self.client.wait_for('message', timeout=30.0, check=check)
                        if msg.content == "no":
                            await ctx.send("Activation of the Autoban function was canceled")
                        else:
                            data = getConfig(ctx.guild.id)
                            data["autoban"] = True
                            if data["joinfilter"] is not True:
                                data["joinfilter"] = True

                            if data["logChannel"] is False:
                                logChannel = await ctx.guild.create_text_channel(f"{self.client.user.name}-logs")

                                perms = logChannel.overwrites_for(ctx.guild.default_role)
                                perms.read_messages = False
                                await logChannel.set_permissions(ctx.guild.default_role, overwrite=perms)

                                data["logChannel"] = logChannel.id

                            updateConfig(ctx.guild.id, data)
                            embed = discord.Embed(title="Enabled successfully", description=f"I have successfully enabled the Auto-Ban feature.", colour=discord.Colour.blue())
                            await ctx.send(embed=embed)

                    except(asyncio.TimeoutError):
                        await ctx.send("Timeout! (30s)")

            if onOroff == 'off':
                data = getConfig(ctx.guild.id)
                data["autoban"] = False
                if data["avatarfilter"] is False:
                    if data["botfilter"] is False:
                        if data["checknew"] is False:
                            data["joinfilter"] = False

                updateConfig(ctx.guild.id, data)
                await ctx.send("Auto-Ban disabled!")

    @commands.command(description="Enables or disables the Check-New Module")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def checknew(self, ctx, onORoff):

        onORoff = onORoff.lower()

        data = getConfig(ctx.guild.id)
        owner = data["owner"]
        admin = data["administrator"]

        if ctx.author.id == owner or admin:
            if onORoff == 'on':
                data = getConfig(ctx.guild.id)
                data["checknew"] = True
                if data["joinfilter"] is not True:
                    data["joinfilter"] = True

                if data["logChannel"] is False:
                    logChannel = await ctx.guild.create_text_channel(f"{self.client.user.name}-logs")

                    perms = logChannel.overwrites_for(ctx.guild.default_role)
                    perms.read_messages = False
                    await logChannel.set_permissions(ctx.guild.default_role, overwrite=perms)

                    data["logChannel"] = logChannel.id

                embed = discord.Embed(title="Enabled successfully", description=f"I have successfully enabled the Check-New feature.\n\n"
                                                                                f"**Note:**\nThe maximum points are standard set to 25", colour=discord.Colour.blue())
                await ctx.send(embed=embed)
                updateConfig(ctx.guild.id, data)

            if onORoff == 'off':
                data = getConfig(ctx.guild.id)
                data["checknew"] = False
                if data["botfilter"] is False:
                    if data["avatarfilter"] is False:
                        data["joinfilter"] = False

                await ctx.send("Check new members disabled!")
                updateConfig(ctx.guild.id, data)


        if ctx.author.id != owner or admin:
            await ctx.send("Only the owner or a selected admin can use this command!")

    @commands.command(description="Sets the maximum number of points a user may achieve for the Check-New module.")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def maxpoints(self, ctx, points):
        data = getConfig(ctx.guild.id)
        owner = data["owner"]
        admin = data["administrator"]

        if ctx.author.id == owner or admin:

            points = points.lower()
            data = getConfig(ctx.guild.id)

            data["points"] = points

            await ctx.send(f"Maximal points: {points}")
            updateConfig(ctx.guild.id, data)

        if ctx.author.id != owner or admin:
            await ctx.send("Only the server owner or a selected administrator can use this command!")

    @commands.command()
    async def raidmode(self, ctx, onORoff):

        onORoff = onORoff.lower()

        if onORoff == "on":
            data = getConfig(ctx.guild.id)
            data["raid"] = True
            data["automoderation"] = True
            data["antiSpam"] = True
            data["antiWord"] = True
            data["antiLink"] = True
            data["joinfilter"] = True
            data["checknew"] = True

            updateConfig(ctx.guild.id, data)
            await ctx.guild.edit(verification_level=discord.VerificationLevel.very_high)
            embed = discord.Embed(title="Enabled successfully",
                                  description=f"I have successfully enabled the Raid-Mode feature.",
                                  colour=discord.Colour.blue())
            await ctx.send(embed=embed)

        if onORoff == "off":
            data = getConfig(ctx.guild.id)
            data["raid"] = False
            if data["antighost"] is False:
                data["automoderation"] = False
                data["antiSpam"] = False
                data["antiLink"] = False
                data["antiWord"] = False
                data["checknew"] = False
            if data["botfilter"] is False:
                if data["avatarfilter"] is False:
                    if data["autoban"] is False:
                        data["joinfilter"] = False

            updateConfig(ctx.guild.id, data)
            await ctx.guild.edit(verification_level=discord.VerificationLevel.low)
            await ctx.send("Raid-Mode disabled!")


def setup(client):
    client.add_cog(Setup(client))