import discord
from discord.ext import commands
import platform
from Tools.utils import getGuildPrefix, getConfig
from dislash import InteractionClient, ActionRow, Button, ButtonStyle
from reactionmenu import ReactionMenu, Button, ButtonType
from discord import *
import datetime
import time
from datetime import datetime
import os
import reactionmenu
from reactionmenu import ButtonsMenu, ComponentsButton


class General(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.counter = 0

    @commands.command(description="Shows information about Server Security")
    async def about(self, ctx):
        emote = ("<:rightArrow:904016483108143115>")
        dpyVersion = discord.__version__
        serverCount = len(self.client.guilds)
        about = discord.Embed(colour=0x2f3136, title=f"About {self.client.user.name}")
        about.add_field(name="General Information: ",
                        value=f"Name: {self.client.user.name}\n"
                              f"{emote}Tag: {self.client.user}\n"
                              f"{emote}ID: {self.client.user.id}\n"
                              f"{emote}Mention: {self.client.user.mention}\n"
                              f"Creation: <t:{round(self.client.user.created_at.timestamp())}:R>\n"
                              f"Dpy-Version: {dpyVersion}\n"
                              f"Ping: {round(self.client.latency * 1000)}ms\n"
                              f"Guilds: {serverCount}\n"
                              f"{emote}Total Members: {len(set(self.client.get_all_members()))}")
        about.add_field(name="**――――――――――**", value=f"[Avatar]({self.client.user.avatar_url})", inline=False)
        about.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=about)

    @commands.command(description="Sends you a bot invite link via DM")
    async def invite(self, ctx):
        invitelink = ("https://discord.com/api/oauth2/authorize?client_id=882901345466724373&permissions=8&scope=bot")
        msg = await ctx.send("Check your DMs")
        try:
            await ctx.author.send(f"`Invite Link`: {invitelink}")
        except discord.errors.Forbidden:
            await msg.edit(content="I am not allowed to send you a DM, look at my User profile there is also a invite link!")

    @commands.command(description="Shows information about this server")
    async def serverinfo(self, ctx):
        emote = ("<:rightArrow:904016483108143115>")
        guild_roles = len(ctx.guild.roles)
        guild_members = len(ctx.guild.members)
        text_channels = len(ctx.guild.text_channels)
        voice_channels = len(ctx.guild.voice_channels)
        channels = text_channels + voice_channels

        result = ' '
        data = getConfig(ctx.guild.id)
        userinwhitelist = data["whitelist"]
        for i in userinwhitelist:
            user2 = self.client.get_user(i)
            if user2 == None:
                user = 'Unable to Fetch Name'
            else:
                user = user2.mention
            result += f"{user}\n"

        serverinfo = discord.Embed(colour=0x2f3136, title="Guild Information")
        serverinfo.add_field(name="General Information:",
                             value=f"Name: {ctx.guild.name}\n"
                                   f"{emote}ID: {ctx.guild.id}\n"
                                   f"{emote}Region: {ctx.guild.region}\n"
                                   f"Owner: {ctx.guild.owner.name}\n"
                                   f"{emote}ID: {ctx.guild.owner.id}\n"
                                   f"{emote}Mention: {ctx.guild.owner.mention}\n"
                                   f"Creation: <t:{round(ctx.guild.created_at.timestamp())}:R>\n"
                                   f"Total Member: {guild_members}\n"
                                   f"Roles: {guild_roles}\n"
                                   f"Channel: {channels}\n"
                                   f"{emote}Text Channel: {text_channels}\n"
                                   f"{emote}Voice Channel: {voice_channels}", inline=False)
        if data["whitelist"] == []:
            serverinfo.add_field(name="Server Security: ", value=f"Whitelist: -")
        else:
            serverinfo.add_field(name="Server Security: ", value=f"Whitelist: \n{result}")
        serverinfo.set_thumbnail(url=ctx.guild.icon_url)
        serverinfo.add_field(name="**――――――――――**", value=f"[Icon]({ctx.guild.icon_url})", inline=False)
        serverinfo.set_image(url=ctx.guild.banner_url)
        await ctx.send(embed=serverinfo)

    @commands.command(description="Shows information about a user")
    async def userinfo(self, ctx, member: discord.Member = None):
        dnd = ("<:dnd:913844829350395924>")
        online = ("<:online:913846756662460456>")
        idle = ("<:idle:913848622595067904>")
        data = getConfig(ctx.guild.id)
        whitelist = data["whitelist"]
        emote = ("<:rightArrow:904016483108143115>")
        member = ctx.author if not member else member
        member_roles = len(member.roles)
        userinfo = discord.Embed(colour=0x2f3136, title=f"{member.name}'s profile")
        if member.status == discord.Status.online:
            userinfo.add_field(name="General Information:",
                                 value=f"Name: {member.name}\n"
                                       f"{emote}Tag: {member}\n"
                                       f"{emote}ID: {member.id}\n"
                                       f"{emote}Mention: {member.mention}\n"
                                       f"Creation: <t:{round(member.created_at.timestamp())}:R>\n"
                                       f"Mobile: {member.is_on_mobile()}\n"
                                       f"Status: {online}\n"
                                       f"Activity: {member.activity}", inline=False)
        if member.status == discord.Status.dnd:
            userinfo.add_field(name="General Information:",
                               value=f"Name: {member.name}\n"
                                     f"{emote}Tag: {member}\n"
                                     f"{emote}ID: {member.id}\n"
                                     f"{emote}Mention: {member.mention}\n"
                                     f"Creation: <t:{round(member.created_at.timestamp())}:R>\n"
                                     f"Mobile: {member.is_on_mobile()}\n"
                                     f"Status: {dnd}\n"
                                     f"Activity: {member.activity}", inline=False)

        if member.status == discord.Status.idle:
            userinfo.add_field(name="General Information:",
                               value=f"Name: {member.name}\n"
                                     f"{emote}Tag: {member}\n"
                                     f"{emote}ID: {member.id}\n"
                                     f"{emote}Mention: {member.mention}\n"
                                     f"Creation: <t:{round(member.created_at.timestamp())}:R>\n"
                                     f"Mobile: {member.is_on_mobile()}\n"
                                     f"Status: {idle}\n"
                                     f"Activity: {member.activity}", inline=False)

        userinfo.add_field(name="Server information:",
                           value=f"{'**Guild Owner**' if member == ctx.guild.owner else ''}\n"
                                 f"Joined: <t:{round(member.joined_at.timestamp())}:R>\n"
                                 f"Roles: {member_roles}\n"
                                 f"Colour: {member.colour}\n"
                                 f"Nickname: {member.nick if member.nick is not None else '-'}\n"
                                 f"Whitelisted: {'Yes' if member.id in whitelist else 'No'}", inline=False)
        req = await self.client.http.request(discord.http.Route("GET", "/users/{uid}", uid=member.id))
        banner_id = req["banner"]
        if banner_id:
            banner_url = f"https://cdn.discordapp.com/banners/{member.id}/{banner_id}?size=1024"
            userinfo.add_field(name="**――――――――――**", value=f"[Avatar]({member.avatar_url}) | [Banner]({banner_url})")
            userinfo.set_image(url=banner_url)
        else:
            userinfo.add_field(name="**――――――――――**", value=f"[Avatar]({member.avatar_url})")
        userinfo.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=userinfo)

    @commands.command(usage="<invitelink/code>",
                      description="Shows information about a invite link")
    async def inviteinfo(self, ctx, invite):
        emote = ("<:rightArrow:904016483108143115>")
        invite = await self.client.fetch_invite(invite)
        inviteinfo = discord.Embed(colour=0x2f3136, title=f"Invite Info")
        inviteinfo.add_field(name="General Information: ",
                             value=f"Name: {invite.guild.name}\n"
                                   f"{emote}ID: {invite.guild.id}\n"
                                   f"{emote}Creation: <t:{round(invite.guild.created_at.timestamp())}:R>\n"
                                   f"Inviter: {invite.inviter}\n"
                                   f"Total Member: {invite.approximate_member_count}\n"
                                   f"Channel: {invite.channel}\n"
                                   f"Uses: {invite.uses}")
        inviteinfo.set_thumbnail(url=invite.guild.icon_url)
        inviteinfo.add_field(name="**――――――――――**", value=f"[Icon]({invite.guild.icon_url}) | [Invite Link]({invite})",
                             inline=False)
        await ctx.send(embed=inviteinfo)

    @commands.command(name="commands",
                      description="Shows you all available commands")
    async def _commands(self, ctx):
        emote = ("<:rightArrow:904016483108143115>")
        prefix = await getGuildPrefix(self.client, ctx)
        menu = ButtonsMenu(ctx, menu_type=ButtonsMenu.TypeEmbed)

        back_button = ComponentsButton(style=ComponentsButton.style.primary, label='Back',
                                       custom_id=ComponentsButton.ID_PREVIOUS_PAGE)

        next_button = ComponentsButton(style=ComponentsButton.style.primary, label='Next',
                                       custom_id=ComponentsButton.ID_NEXT_PAGE)

        end_button = ComponentsButton(style=ComponentsButton.style.red, label='End',
                                      custom_id=ComponentsButton.ID_END_SESSION)

        page1 = discord.Embed(title="Available commands", colour=discord.Colour.blue(),
                              description=f"{emote} `{prefix}about`\n"
                                          f"{emote} `{prefix}invite`\n"
                                          f"{emote} `{prefix}serverinfo`\n"
                                          f"{emote} `{prefix}userinfo`\n"
                                          f"{emote} `{prefix}prefix`\n"
                                          f"{emote} `{prefix}inviteinfo`\n"
                                          f"{emote} `{prefix}lockall`\n"
                                          f"{emote} `{prefix}unlockall`\n"
                                          f"{emote} `{prefix}lock`\n"
                                          f"{emote} `{prefix}unlock`")
        page2 = discord.Embed(title="Available commands", colour=discord.Colour.blue(),
                              description=f"{emote} `{prefix}kick`\n"
                                          f"{emote} `{prefix}ban`\n"
                                          f"{emote} `{prefix}unban`\n"
                                          f"{emote} `{prefix}clear`\n"
                                          f"{emote} `{prefix}mute`\n"
                                          f"{emote} `{prefix}unmute`\n"
                                          f"{emote} `{prefix}nuke`\n"
                                          f"{emote} `{prefix}whitelist`\n"
                                          f"{emote} `{prefix}unwhitelist`\n"
                                          f"{emote} `{prefix}whitelisted`\n")
        page3 = discord.Embed(title="Available commands", colour=discord.Colour.blue(),
                              description=
                              f"{emote} `{prefix}punishment`\n"
                              f"{emote} `{prefix}help`\n"
                              f"{emote} `{prefix}setup`\n"
                              f"{emote} `{prefix}commands`\n"
                              f"{emote} `{prefix}bug`\n"
                              f"{emote} `{prefix}verifiedrole`\n"
                              f"{emote} `{prefix}captchapunishment`\n"
                              f"{emote} `{prefix}panicmode`\n"
                              f"{emote} `{prefix}administrator`\n"
                              f"{emote} `{prefix}unadministrator`\n")
        page4 = discord.Embed(title="Available commands", colour=discord.Colour.blue(),
                              description=f"{emote} `{prefix}raidmode`\n"
                                          f"{emote} `{prefix}uptime`\n"
                                          f"{emote} `{prefix}disable`\n"
                                          f"{emote} `{prefix}jr`")
        menu.add_page(page1)
        menu.add_page(page2)
        menu.add_page(page3)
        menu.add_page(page4)
        menu.add_button(back_button)
        menu.add_button(next_button)
        menu.add_button(end_button)
        member_details = []
        for member_embed in member_details:
            menu.add_page(member_embed)
        await menu.start()

    @commands.command(usage="<message>", description="Reports a bug")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def bug(self, ctx, *, message=None):
        prefix = await getGuildPrefix(self.client, ctx)
        if message == None:
            await ctx.send(f"Please do `{prefix}bug` for this command to work!")
        else:
            await ctx.send("Thank you for reporting this bug my developer will try to fix it!")

            channel = self.client.get_channel(894943888832360539)
            embed2 = discord.Embed(title=f"Bug reported by {ctx.author}", colour=discord.Colour.blue())
            embed2.add_field(name="Server", value=f"{ctx.guild.name}")
            embed2.add_field(name="Bug", value=f"{message}")
            embed2.set_thumbnail(url=ctx.guild.icon_url)
            await channel.send(embed=embed2)

    @commands.command(description="Shows you the current server settings")
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx):
        emote = ("<:rightArrow:904016483108143115>")
        alarm = ("🚨")
        shild = ("🛡️")
        general = ("⚙")
        filter = ("🚫")
        verify = ("📝")
        auto = ("🤖")
        raidemote = ("🔒")
        data = getConfig(ctx.guild.id)
        captcha = data["captcha"]
        captchaChannel = data["captchaChannel"]
        temporaryRole = data["temporaryRole"]
        roleGivenAfterCaptcha = data["roleGivenAfterCaptcha"]
        antinuke = data["antinuke"]
        punishment = data["punishment"]
        prefix = data["prefix"]
        owner = data["owner"]
        captchaLog = data["captchaLog"]
        captchapunishment = data["captchapunishment"]
        joinfilter = data["joinfilter"]
        botfilter = data["botfilter"]
        avatarfilter = data["avatarfilter"]
        logChannel = data["logChannel"]
        automoderation = data["automoderation"]
        antiSpam = data["antiSpam"]
        antiWord = data["antiWord"]
        antiLink = data["antiLink"]
        antighost = data["antighost"]
        panicmode = data["panicmode"]
        panicpunishment = data["panicpunishment"]
        administrator = data["administrator"]
        autoban = data["autoban"]
        checknew = data["checknew"]
        points = data["points"]
        raid = data["raid"]

        if roleGivenAfterCaptcha is not False:
            roleGivenAfterCaptcha = f"<@&{roleGivenAfterCaptcha}>"
        else:
            roleGivenAfterCaptcha = f"Not Found"
        if temporaryRole is not False:
            temporaryRole = f"<@&{temporaryRole}>"
        else:
            temporaryRole = f"Not Found"
        if captchaChannel is not False:
            captchaChannel = f"<#{captchaChannel}>"
        else:
            captchaChannel = f"Not Found"

        if captcha is True:
            captchaonoff = f"**enabled**"
        else:
            captchaonoff = f"disabled"

        if antinuke is True:
            antinuke = f"**enabled**"
        else:
            antinuke = f"disabled"
        if captchaLog is not False:
            captchaLog = f"<#{captchaLog}>"
        else:
            captchaLog = f"Not Found"
        if captchapunishment is False:
            captchapunishment = f"None"

        if joinfilter is True:
            joinfilter = f"**enabled**"
        else:
            joinfilter = f"disabled"

        if botfilter is True:
            botfilter = f"**enabled**"
        else:
            botfilter = f"disabled"

        if avatarfilter is True:
            avatarfilter = f"**enabled**"
        else:
            avatarfilter = f"disabled"

        if punishment is False:
            punishment = f"None"

        if logChannel is False:
            logChannel = f"Not Found"
        else:
            logChannel = f"<#{logChannel}>"

        if automoderation is not False:
            automoderation = f"**enabled**"
        else:
            automoderation = f"disabled"

        if antiSpam is not False:
            antiSpam = f"**enabled**"
        else:
            antiSpam = f"disabled"

        if antiLink is not False:
            antiLink = f"**enabled**"
        else:
            antiLink = f"disabled"

        if antiWord is not False:
            antiWord = f"**enabled**"
        else:
            antiWord = f"disabled"
        if antighost is not False:
            antighost = f"**enabled**"
        else:
            antighost = f"disabled"
        if panicmode is not False:
            panicmode = f"**enabled**"
        else:
            panicmode = f"disabled"

        if administrator is not False:
            administrator = f"<@{administrator}>"
        else:
            administrator = f"None"

        owner = f"<@{owner}>"

        if autoban is not False:
            autoban = f"**enabled**"
        else:
            autoban = f"disabled"

        if checknew is not False:
            checknew = f"**enabled**"
        else:
            checknew = f"disabled"

        if raid is not False:
            raid = f"**enabled**"
        else:
            raid = f"disabled"

        embed = discord.Embed(title=f"Settings for {ctx.guild.name}", colour=discord.Colour.blue())
        embed.add_field(name=f"{general} General Settings", value=f"{emote} Owner: {owner}\n{emote} Administrator: {administrator}\n{emote} Prefix: {prefix}\n{emote} Log-Channel: {logChannel}", inline=False)
        embed.add_field(name=f"{shild} Anti-Nuke", value=f"{emote} Anti-Nuke: {antinuke}\n{emote} Punishment: {punishment}", inline=False)
        embed.add_field(name=f"{filter} Join-Filter", value=f"{emote} Join-Filter: {joinfilter}\n{emote} Bot-Filter: {botfilter}\n{emote} Avatar-Filter: {avatarfilter}\n{emote} Auto-Ban: {autoban}\n{emote} Check new member: {checknew}\n{emote} Points: {points}", inline=False)
        embed.add_field(name=f"{verify} Captcha-Verification", value=f"{emote} Captcha-Verification: {captchaonoff}\n{emote} Verification-Channel: {captchaChannel}\n{emote} Captcha-Log: {captchaLog}\n{emote} Captcha-Punishment: {captchapunishment}\n{emote} Unverified-Role: {temporaryRole}\n{emote} Verified-Role: {roleGivenAfterCaptcha}", inline=False)
        embed.add_field(name=f"{auto} Auto-Moderation", value=f"{emote} Auto-Moderation: {automoderation}\n{emote} Anti-Spam: {antiSpam}\n{emote} Anti-Link: {antiLink}\n{emote} Anti-Word: {antiWord}\n{emote} Anti-Ghostping: {antighost}", inline=False)
        embed.add_field(name=f"{alarm} Panic-Mode", value=f"{emote} Panic-Mode: {panicmode}\n{emote} Panic-Mode punishment: {panicpunishment}\n", inline=False)
        embed.add_field(name=f"{raidemote} Raid-Mode", value=f"{emote} Raid-Mode: {raid}", inline=False)
        embed.set_footer(text=f"If you want to disable everything at once use the command → {prefix}disable all")
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True, description="Shows you all available Server Security features")
    async def features(self, ctx):
        emote = ("<:rightArrow:904016483108143115>")
        alarm = ("🚨")
        shild = ("🛡️")
        filter = ("🚫")
        verify = ("📝")
        auto = ("🤖")
        raid = ("🔒")
        info = ("ℹ")
        roles = ("<:Role:911574636280561694>")
        prefix = await getGuildPrefix(self.client, ctx)
        menu = ButtonsMenu(ctx, menu_type=ButtonsMenu.TypeEmbed)

        back_button = ComponentsButton(style=ComponentsButton.style.primary, label='Back',
                                       custom_id=ComponentsButton.ID_PREVIOUS_PAGE)

        next_button = ComponentsButton(style=ComponentsButton.style.primary, label='Next',
                                       custom_id=ComponentsButton.ID_NEXT_PAGE)

        end_button = ComponentsButton(style=ComponentsButton.style.red, label='End',
                                      custom_id=ComponentsButton.ID_END_SESSION)

        first_button = ComponentsButton(style=ComponentsButton.style.primary, label='First',
                                        custom_id=ComponentsButton.ID_GO_TO_FIRST_PAGE)

        features = discord.Embed(title=f"{self.client.user.name} features", colour=discord.Colour.blue(),
                                 description=f"With some powerful features, Server Security will be able to protect your server from being nuked, raided, malicous users, spammer etc. Make sure the bot has the highest possible role on your server. Don't give it a higher role! Move the role it created higher! **Also the bot won't function without having the Administrator permission.**")
        features.add_field(name=f"{info} Information", value=f"{emote} `{prefix}features captcha`\n"
                                                             f"{emote} `{prefix}features antinuke`\n"
                                                             f"{emote} `{prefix}features joinfilter`\n"
                                                             f"{emote} `{prefix}features automoderation`\n"
                                                             f"{emote} `{prefix}features panicmode`\n"
                                                             f"{emote} `{prefix}features raidmode`\n"
                                                             f"{emote} `{prefix}features rolemanagement`", inline=False)
        '''CAPTCHA FEATURE'''
        captcha = discord.Embed(title=f"{verify} Captcha-Verification",
                                description=f"The Captcha-Verification will protect your server from malicious raids using automoated bots and malicious users/discord scammer! I will create a Verification-Channel, Captcha-Logs, Unverified-Role and a Verified-Role. You can also change the punishment!",
                                colour=discord.Colour.blue())
        captcha.add_field(name=f"Setup", value=f"{emote} `{prefix}setup captcha`", inline=False)
        captcha.add_field(name="Disable", value=f"{emote} `{prefix}captcha <off>`", inline=False)
        captcha.add_field(name=f"Verified Role", value=f"{emote} `{prefix}verifiedrole <role id>`", inline=False)
        captcha.add_field(name=f"Punishment", value=f"{emote} `{prefix}captchapunishment <kick/ban/none>`",
                          inline=False)

        '''Anti-Nuke'''
        antinuke = discord.Embed(title=f"{shild} Anti-Nuke",
                                 description=f"If the Anti-Nuke system is enabled, Server Security will constantly monitor the audit log. This means that malicous bots can no longer destroy your server! **You should whitelist some users!**",
                                 colour=discord.Colour.blue())
        antinuke.add_field(name="Setup", value=f"{emote} `{prefix}setup antinuke`", inline=False)
        antinuke.add_field(name="Disable", value=f"{emote} `{prefix}antinuke <off>`", inline=False)
        antinuke.add_field(name=f"Punishment", value=f"{emote} `{prefix}punishment <kick/ban/none>`", inline=False)
        antinuke.add_field(name=f"Whitelist", value=f"{emote} `{prefix}whitelist <user>`\n"
                                                    f"{emote} `{prefix}unwhitelist <user>`\n"
                                                    f"{emote} `{prefix}whitelisted`", inline=False)

        '''Join-Filter'''
        joinfilter = discord.Embed(title=f"{filter} Join-Filter",
                                   description=f"The Join-Filter filters out bots, users who don't have a custom avatar, or it checks the users with a points system. The maximum default number of points is 25, but you can change it at any time. Tip I would be careful with the Auto-Ban module and enable it only in emergency situations!",
                                   colour=discord.Colour.blue())
        joinfilter.add_field(name=f"Setup", value=f"{emote} `{prefix}setup joinfilter`", inline=False)
        joinfilter.add_field(name=f"Disable", value=f"{emote} `{prefix}joinfilter <off>`", inline=False)
        joinfilter.add_field(name="Module",
                             value=f"{emote} `{prefix}botfilter <on/off>`\n{emote} `{prefix}avatarfilter <on/off>`\n{emote} `{prefix}autoban <on/off>`\n{emote} `{prefix}checknew <on/off>`\n{emote} `{prefix}maxpoints <points>`\n",
                             inline=False)

        '''Auto-Moderation'''
        automoderation = discord.Embed(title=f"{auto} Auto-Moderation",
                                       description=f"The Auto-Moderation System is enabled it will monitor every message!",
                                       colour=discord.Colour.blue())
        automoderation.add_field(name=f"Setup", value=f"{emote} `{prefix}setup automoderation`", inline=False)
        automoderation.add_field(name=f"Disable", value=f"{emote} `{prefix}automoderation <off>`", inline=False)
        automoderation.add_field(name="Module", value=f"{emote} `{prefix}antispam <on/off>`\n"
                                                      f"{emote} `{prefix}antiword <on/off>`\n"
                                                      f"{emote} `{prefix}antilink <on/off>`\n"
                                                      f"{emote} `{prefix}antighost <on/off>`\n", inline=False)

        '''Panic-Mode'''
        panicmode = discord.Embed(title=f"{alarm} Panic-Mode",
                                  description=f"If the Panic-Mode is enabled, every user who writes a message will be kicked/banned/muted",
                                  colour=discord.Colour.blue())
        panicmode.add_field(name=f"Enable", value=f"{emote} `{prefix}panicmode <on>`", inline=False)
        panicmode.add_field(name=f"Disable", value=f"{emote} `{prefix}panicmode <off>`", inline=False)
        panicmode.add_field(name=f"Punishment", value=f"{emote} `{prefix}panicpunishment <kick/ban/mute>`",
                            inline=False)

        '''Raid-Mode'''
        raidmode = discord.Embed(title=f"{raid} Raid-Mode",
                                 description=f"If the Raid-Mode is enabled, the server verification level is set to highest, auto-mod is enabled and server security pays more attention to join behavior.",
                                 colour=discord.Colour.blue())
        raidmode.add_field(name=f"Enable", value=f"{emote} `{prefix}raidmode <on>`", inline=False)
        raidmode.add_field(name=f"Disable", value=f"{emote} `{prefix}raidmode <off>`", inline=False)

        '''Role Management'''
        role = discord.Embed(title=f"{roles} Role Management",
                             description=f"The role management feature includes the Join Role and Reaction Role features",
                             color=discord.Colour.blue())
        role.add_field(name=f"Join Role",
                       value=f"{emote} `{prefix}jr <?add> <role>`\n"
                             f"{emote} `{prefix}jr <?remove> <role>`",
                       inline=False)

        menu.add_button(back_button)
        menu.add_button(next_button)
        menu.add_button(first_button)
        menu.add_button(end_button)
        menu.add_page(features)
        menu.add_page(captcha)
        menu.add_page(antinuke)
        menu.add_page(joinfilter)
        menu.add_page(automoderation)
        menu.add_page(panicmode)
        menu.add_page(raidmode)
        menu.add_page(role)
        member_details = []
        for member_embed in member_details:
            menu.add_page(member_embed)
        await menu.start()

    @features.command()
    async def captcha(self, ctx):
        emote = ("<:rightArrow:904016483108143115>")
        verify = ("📝")
        prefix = await getGuildPrefix(self.client, ctx)
        embed = discord.Embed(title=f"{verify} Captcha-Verification",
                              description=f"The Captcha-Verification will protect your server from malicious raids using automoated bots and malicious users/discord scammer! I will create a Verification-Channel, Captcha-Logs, Unverified-Role and a Verified-Role. You can also change the punishment!",
                              colour=discord.Colour.blue())
        embed.add_field(name=f"Setup", value=f"{emote} `{prefix}setup captcha`", inline=False)
        embed.add_field(name="Disable", value=f"{emote} `{prefix}captcha <off>`", inline=False)
        embed.add_field(name=f"Verified Role", value=f"{emote} `{prefix}verifiedrole <role id>`", inline=False)
        embed.add_field(name=f"Punishment", value=f"{emote} `{prefix}captchapunishment <kick/ban/none>`", inline=False)
        await ctx.send(embed=embed)

    @features.command()
    async def antinuke(self, ctx):
        emote = ("<:rightArrow:904016483108143115>")
        shild = ("🛡️")
        prefix = await getGuildPrefix(self.client, ctx)
        embed = discord.Embed(title=f"{shild} Anti-Nuke",
                              description=f"If the Anti-Nuke system is enabled, Server Security will constantly monitor the audit log. This means that malicous bots can no longer destroy your server! **You should whitelist some users!**",
                              colour=discord.Colour.blue())
        embed.add_field(name="Setup", value=f"{emote} `{prefix}setup antinuke`", inline=False)
        embed.add_field(name="Disable", value=f"{emote} `{prefix}antinuke <off>`", inline=False)
        embed.add_field(name=f"Punishment", value=f"{emote} `{prefix}punishment <kick/ban/none>`", inline=False)
        embed.add_field(name=f"Whitelist", value=f"{emote} `{prefix}whitelist <user>`\n"
                                                 f"{emote} `{prefix}unwhitelist <user>`\n"
                                                 f"{emote} `{prefix}whitelisted`", inline=False)
        await ctx.send(embed=embed)

    @features.command()
    async def joinfilter(self, ctx):
        emote = ("<:rightArrow:904016483108143115>")
        filter = ("🚫")
        prefix = await getGuildPrefix(self.client, ctx)
        embed = discord.Embed(title=f"{filter} Join-Filter",
                              description=f"The Join-Filter filters out bots, users who don't have a custom avatar, or it checks the users with a points system. The maximum default number of points is 25, but you can change it at any time. Tip I would be careful with the Auto-Ban module and enable it only in emergency situations!",
                              colour=discord.Colour.blue())
        embed.add_field(name=f"Setup", value=f"{emote} `{prefix}setup joinfilter`", inline=False)
        embed.add_field(name=f"Disable", value=f"{emote} `{prefix}joinfilter <off>`", inline=False)
        embed.add_field(name="Module",
                        value=f"{emote} `{prefix}botfilter <on/off>`\n`{prefix}avatarfilter <on/off>`\n`{prefix}autoban <on/off>`\n`{prefix}checknew <on/off>`\n`{prefix}maxpoints <points>`\n",
                        inline=False)
        await ctx.send(embed=embed)

    @features.command()
    async def automoderation(self, ctx):
        emote = ("<:rightArrow:904016483108143115>")
        auto = ("🤖")
        prefix = await getGuildPrefix(self.client, ctx)
        embed = discord.Embed(title=f"{auto} Auto-Moderation",
                              description=f"The Auto-Moderation System is enabled it will monitor every message!",
                              colour=discord.Colour.blue())
        embed.add_field(name=f"Setup", value=f"{emote} `{prefix}setup automoderation`", inline=False)
        embed.add_field(name=f"Disable", value=f"{emote} `{prefix}automoderation <off>`", inline=False)
        embed.add_field(name="Module", value=f"{emote} `{prefix}antispam <on/off>`\n"
                                             f"{emote} `{prefix}antiword <on/off>`\n"
                                             f"{emote} `{prefix}antilink <on/off>`\n"
                                             f"{emote} `{prefix}antighost <on/off>`\n", inline=False)
        await ctx.send(embed=embed)

    @features.command()
    async def panicmode(self, ctx):
        emote = ("<:rightArrow:904016483108143115>")
        alarm = ("🚨")
        prefix = await getGuildPrefix(self.client, ctx)
        embed = discord.Embed(title=f"{alarm} Panic-Mode",
                              description=f"If the Panic-Mode is enabled, every user who writes a message will be kicked/banned/muted",
                              colour=discord.Colour.blue())
        embed.add_field(name=f"Enable", value=f"{emote} `{prefix}panicmode <on>`", inline=False)
        embed.add_field(name=f"Disable", value=f"{emote} `{prefix}panicmode <off>`", inline=False)
        embed.add_field(name=f"Punishment", value=f"{emote} `{prefix}panicpunishment <kick/ban/mute>`", inline=False)
        await ctx.send(embed=embed)

    @features.command()
    async def raidmode(self, ctx):
        emote = ("<:rightArrow:904016483108143115>")
        raid = ("🔒")
        prefix = await getGuildPrefix(self.client, ctx)
        raidmode = discord.Embed(title=f"{raid} Raid-Mode",
                                 description=f"If the Raid-Mode is enabled, the server verification level is set to highest, auto-mod is enabled and server security pays more attention to join behavior.",
                                 colour=discord.Colour.blue())
        raidmode.add_field(name=f"Enable", value=f"{emote} `{prefix}raidmode <on>`", inline=False)
        raidmode.add_field(name=f"Disable", value=f"{emote} `{prefix}raidmode <off>`", inline=False)
        await ctx.send(embed=raidmode)

    @features.command()
    async def rolemanagement(self, ctx):
        roles = ("<:Role:911574636280561694>")
        emote = ("<:rightArrow:904016483108143115>")
        role = discord.Embed(title=f"{roles} Role Management",
                             description=f"The role management feature includes the Join Role and Reaction Role features",
                             color=discord.Colour.blue())
        role.add_field(name=f"Join Role",
                       value=f"{emote} `{prefix}jr <?add> <role>`\n"
                             f"{emote} `{prefix}jr <?remove> <role>`",
                       inline=False)
        await ctx.send(embed=role)

    @commands.command(usage="user id", description="Shows you information about a user who is not on this server")
    async def fetchuser(self, ctx, user: discord.User = id):
        emote = ("<:rightArrow:904016483108143115>")
        user = await self.client.fetch_user(int(user.id))
        embed = discord.Embed(colour=0x2f3136, title=f"Who is {user.name}?")
        embed.add_field(name=f"General Information",
                        value=f"Name: {user.name}\n"
                              f"{emote}Tag: {user}\n"
                              f"{emote}ID: {user.id}\n"
                              f"{emote}Mention: {user.mention}\n"
                              f"Creation: <t:{round(user.created_at.timestamp())}:R>\n")
        embed.set_thumbnail(url=user.avatar_url)
        req = await self.client.http.request(discord.http.Route("GET", "/users/{uid}", uid=user.id))
        banner_id = req["banner"]
        if banner_id:
            banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}?size=1024"
            embed.add_field(name="**――――――――――**", value=f"[Avatar]({user.avatar_url}) | [Banner]({banner_url})",
                            inline=False)
            embed.set_image(url=banner_url)
        else:
            embed.add_field(name="**――――――――――**", value=f"[Avatar]({user.avatar_url})", inline=False)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(General(client))