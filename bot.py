import os
import discord
from discord.ext import commands
import datetime
from datetime import datetime
from datetime import timedelta
import asyncio

bot = commands.Bot(command_prefix='@')
guild_id = 287487891003932672
minutes_in_a_day = 1440
expiration_times = {}
role = 0

async def get_role():
    global role
    if role == 0:
        role = discord.utils.get(bot.get_guild(guild_id).roles, name="LFG")

@bot.command(pass_context=True)
async def im_LFG(ctx, minutes=minutes_in_a_day):
    if role in ctx.message.author.roles:
        await ctx.message.author.remove_roles(role)
        await ctx.send(str(ctx.message.author.name) + " is no longer looking for a game.")
    else:
        print(role)
        expiration_time = datetime.now() + timedelta(minutes=minutes)
        expiration_times[ctx.author.id] = expiration_time
        await ctx.message.author.add_roles(role)
        await ctx.send("Hey, @LFG! " + str(ctx.message.author.name) + " is looking for a game.")

@bot.command(pass_context=True)
async def whos_LFG(ctx):
    currently_looking = []
    role = discord.utils.get(ctx.message.guild.roles, name="LFG")
    for member in ctx.message.guild.members:
        if role in member.roles:
            currently_looking.append(member)
    if len(currently_looking) > 0:
        for member in currently_looking:
            await ctx.send(str(member.name) + " is looking for a game.")
    else:
        await ctx.send("Nobody is looking for a game :(")


@bot.command(pass_context=True)
async def info(ctx):
    embed = discord.Embed(title="Looking For Game Bot", description="Keeps track of who is currently looking for a game.", color=0xeee657)
    embed.add_field(name="Author", value="FluffM")
    await ctx.send(embed=embed)

bot.remove_command('help')

@bot.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(title="Looking For Game Bot", description="Keeps track of who is currently looking for a game. The following commands are available:", color=0xeee657)

    embed.add_field(name="@LFG [minutes]", value="Toggles your role for LFG. You can limit the length of time you will be LFG by entering a number of minutes after the command.", inline=False)
    embed.add_field(name="@whos_LFG", value="Tells you who is currently looking.", inline=False)
    embed.add_field(name="@info", value="Gives a little info about the bot.", inline=False)
    embed.add_field(name="@help", value="Gives this message.", inline=False)

    await ctx.send(embed=embed)

async def check_LFG():
    await bot.wait_until_ready()
    await get_role()
    while not bot.is_closed == True:
        print(expiration_times)
        for uid, expiration_time in expiration_times.items():
            if datetime.now() > expiration_time:
                await discord.utils.get(bot.get_all_members(), id=uid).remove_roles(role)

        await asyncio.sleep(60)

bot.loop.create_task(check_LFG())
bot.run(os.environ["LFG_TOKEN"])
