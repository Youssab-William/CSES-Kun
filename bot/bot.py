import discord
import os
from discord.ext import commands
import random
import update_db
from hopcroftkarp import HopcroftKarp

description = '''CSES Kun a discord bot to practice cses problems'''
bot = commands.Bot(command_prefix='?', description=description)

update_db.main()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    if times > 10:
        await ctx.send('I cannot repeat a word more than 10 times')
        return 
    for i in range(times):
        await ctx.send(content)

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send('{0.name} joined in {0.joined_at}'.format(member))

 
@bot.group()
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))

@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')

#Get all problems that hadn't been solved by user in topic typ
def getall(typ, l, r, solved2):
  problems = []
  path = "problems/"+typ+".txt"
  file = open(path , "r")
  for problem in file.readlines(): #xD
    pnum = problem.split(' ')[0]
    pnum = pnum.split('/')[-1]
    solvedcount=int(problem.split(' ')[1])
    if pnum in solved2:
      pass
    elif solvedcount < l or solvedcount > r:
      pass
    else:
      problems.append(pnum)
  random.shuffle(problems)
  return problems

#pick problems that user hadn't solved
def pick1(l, r, solved2):
  problems = []
  for tmp,typ in topics:
    tpc = getall(typ, l, r, solved2)
    for prb in tpc:
      problems.append(prb)
  return problems
             
@bot.command()
async def problem(ctx, l: int, r: int):
    """pick a problem you didn't solve which had been solved by number of users between l and r
    """
    if r < l:
        await ctx.send("First number must be <= second number")
        return
    if(l < 0):
        await ctx.send("Numbers should be >= 0")
        return
    problems = pick1(l,r,getSolved(ctx.message.author.id))
    if len(problems) == 0:
        await ctx.send("couldn't find a problem")
        return
    random.shuffle(problems)
    await ctx.send("https://cses.fi/problemset/task/"+problems[0])
