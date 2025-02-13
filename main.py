from __future__ import annotations

from discord.ext import commands
import discord
import re

with open('token.txt', 'r') as f:
    token = f.read()
with open('assets/terms.txt', 'r') as f:
    termstext = f.read()

class PersistentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='I Agree', style=discord.ButtonStyle.green, custom_id='persistent_view:green', emoji='\N{WHITE HEAVY CHECK MARK}')
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button):
        if 1339488727822766123 not in [r.id for r in interaction.user.roles]:
            await interaction.user.add_roles(discord.Object(1339488727822766123), reason='User agreed to NSFW channel access terms.')
            await interaction.response.send_message('Thanks for agreeing to the terms!', ephemeral=True)
        else:
            await interaction.response.send_message('You have already agreed to the terms, but thanks for your enthusiasm!', ephemeral=True)

class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix=commands.when_mentioned, intents=intents)

    async def setup_hook(self) -> None:
        self.add_view(PersistentView())

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

bot = PersistentViewBot()

@bot.command()
@commands.is_owner()
async def terms(ctx: commands.Context):
    """Starts a persistent view."""
    em = discord.Embed(title='NSFW Channel Access', description=termstext, color=discord.Color.blurple())
    await ctx.send('Agreeance to the following terms is required to access NSFW channels:', embed=em, view=PersistentView())

bot.run(token)