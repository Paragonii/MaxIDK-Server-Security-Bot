import discord
from discord.ext import commands
from Tools.utils import getConfig, getGuildPrefix, updateConfig
from reactionmenu import ButtonsMenu, ComponentsButton


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        prefix = await getGuildPrefix(self.client, ctx)
        emote = ("<:rightArrow:904016483108143115>")

        menu = ButtonsMenu(ctx, menu_type=ButtonsMenu.TypeEmbed)

        back_button = ComponentsButton(style=ComponentsButton.style.primary, label='Back',
                                       custom_id=ComponentsButton.ID_PREVIOUS_PAGE)

        next_button = ComponentsButton(style=ComponentsButton.style.primary, label='Next',
                                       custom_id=ComponentsButton.ID_NEXT_PAGE)

        end_button = ComponentsButton(style=ComponentsButton.style.red, label='End',
                                      custom_id=ComponentsButton.ID_END_SESSION)

        help = discord.Embed(title="Overview",
                             description="Server Security is an anti nuke bot with some other cool features.",
                             colour=discord.Colour.blue())
        help.add_field(name=f"{emote} General Commands:",
                       value="`about`, `invite`, `serverinfo`, `userinfo`, `prefix`, `inviteinfo`, `commands`, `bug`, `fetchuser`, `snipe`",
                       inline=False)
        help.add_field(name=f"{emote} Moderation Commands:",
                       value=f"`lock`, `unlock`, `kick`, `ban`, `softban`, `unban`, `clear`, `mute`, `unmute`, `nuke`, `role`, `slowmode`")
        help.add_field(name=f"{emote} Server Security",
                       value=f"`features`, `settings`, `permissions`\n\nDo you want to setup Server Security? use `{prefix}setup`",
                       inline=False)

        # Moderation Help Command
        help_general = discord.Embed(title=f"Overview General Commands", colour=discord.Colour.blue(),
                                     description=f"<...> Duty | [...] Optional\n\n"
                                                 f"`{prefix}about`\n"
                                                 f"Shows information about Server Security\n\n"
                                                 f"`{prefix}invite`\n"
                                                 f"Sends you a bot invite link via DM\n\n"
                                                 f"`{prefix}serverinfo`\n"
                                                 f"Shows information about this server\n\n"
                                                 f"`{prefix}userinfo [member]`\n"
                                                 f"Shows information about a user\n\n"
                                                 f"`{prefix}prefix <new prefix>`\n"
                                                 f"Changes the server prefix\n\n"
                                                 f"`{prefix}inviteinfo <link/code>`\n"
                                                 f"Shows information about a invite link\n\n"
                                                 f"`{prefix}commands`\n"
                                                 f"Shows you all available commands\n\n"
                                                 f"`{prefix}bug <message>`\n"
                                                 f"Reports a bug\n\n"
                                                 f"`{prefix}fetchuser <user id>`\n"
                                                 f"Shows you information about a user who is not on this server\n\n"
                                                 f"`{prefix}snipe`\n"
                                                 f"Snipes the last deleted message\n\n"
                                                 f"`{prefix}uptime`\n"
                                                 f"Shows you Server Security's Uptime\n\n")

        help_mod = discord.Embed(title=f"Overview Moderation Commands", colour=discord.Colour.blue(),
                                 description=f"<...> Duty | [...] Optional\n\n"
                                             f"`{prefix}lock [#channel/id]`\n"
                                             f"Locks a channel\n\n"
                                             f"`{prefix}unlock [#channel/id]`\n"
                                             f"Unlocks a channel\n\n"
                                             f"`{prefix}kick <member> [reason]`\n"
                                             f"Kicks a user from the server\n\n"
                                             f"`{prefix}ban <member> [reason]`\n"
                                             f"Bans a user from the server\n\n"
                                             f"`{prefix}softban <member> [reason]`\n"
                                             f"Bans a user from the server and deletes all of his messages of the last 7 days\n\n"
                                             f"`{prefix}unban <user id>`\n"
                                             f"Unbans a user from the server\n\n"
                                             f"`{prefix}clear <amount>`\n"
                                             f"Deletes a certain number of messages\n\n"
                                             f"`{prefix}mute <member> [reason]`\n"
                                             f"Mutes a user on the server\n\n"
                                             f"`{prefix}unmute <member>`\n"
                                             f"Unmutes a user on the server\n\n"
                                             f"`{prefix}nuke`\n"
                                             f"Clones a text channel and then deletes the old one\n\n"
                                             f"`{prefix}role <add/remove> <member> <role>`\n"
                                             f"Adds or removes a role from a user\n\n"
                                             f"`{prefix}slowmode <seconds>`\n"
                                             f"Sets the chat delay\n\n")

        menu.add_button(back_button)
        menu.add_button(next_button)
        menu.add_button(end_button)
        menu.add_page(help)
        menu.add_page(help_general)
        menu.add_page(help_mod)
        member_details = []
        for member_embed in member_details:
            menu.add_page(member_embed)
        await menu.start()


def setup(client):
    client.add_cog(Help(client))