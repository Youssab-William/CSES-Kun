import discord
from discord.ext import commands
import random
import update_db

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
#code starting from here
#write it here youssab
# how r u guys so geniosity, how can I be geniosity like u guys
@bot.command()
async def solved(ctx , idd :int )
	user_id = ctx.message.author.id
  file = open("users/"+user_id+".txt","a+")
	file.write(str(idd)+"\n")
  await ctx.send('one more problem solved! ')

topics=[("intro","Introductory Problems"),("sorting","Sorting and Searching"),("searching","Sorting and Searching"),("dp","Dynamic Programming"),("graph","Graph Algorithms"),("rq","Range Queries"),("tree","Tree Algorithms"),("math","Mathematics"),("string","String Algorithms"),("additional","Additional Problems")]
  
def getall(typ, l, r, solved):
  problems = []
  path = "problems/"+typ+".txt"
  file = open(path , "r")
  for problem in file.readlines(): #xD
    pnum = problem.split(' ')[0]
    pnum = pnum.split('/')[-1]
    solvedcount=int(problems.split(' ')[1])
    if pnum in solved:
      pass
    else if solvedcount < l or solvedcount > r:
      pass
    else:
      problems.append(pnum)
  return problems
    
  
  
  
def pick1(l, r, solved):
  problems = []
  problems.append(1321) #مزاجى

  
def pick(problems,solved):
	for typ,l,r in problems:
		allp = get_all(typ,l,r,solved)
		avail = []
		for i in allp:
			if i in solved or i in problems:
				pass
			else:
				avail.append(i)
		if len(avail) == 0:
			pass
		else:
			cur=random.choice(avail)
			problems.append(cur)

  
def getTopic(top):
  top=top.lower()
  for i,j in topics:
    if top == i:
      return j
  return "Error"
  
@bot.command()
async def problem(ctx, l: int, r: int):
	if r < l:
		await ctx.send("First number must be <= second number")
		return
	if(l < 0):
		await ctx.send("Numbers should be >= 0")
		return
  problem = pick1(l,r,getSolved(ctx.message.author.id))

@bot.command()
async def suggest(ctx, *args: str):
  if len(args) == 0:
    await ctx.send("Provide valid arguments")
    return
  try:
  	n=int(args[0])
  except:
    await ctx.send("Provide valid arguments")
    return
	if len(args) != 3*n+1:
    await ctx.send("Provide valid arguments")
    return
  types=[]
  for i in range(n):
    try:
    	topic=args[1+3*i]
    	l=int(args[2+3*i])
      r=int(args[3+3*i])
    except:
      await ctx.send("Provide valid arguments")
    	return
    topic=getTopic(topic)
    if topic == "Error":
      await ctx.send("Provide valid arguments")
    	return
    types.append((topic,l,r))
  problems=pick(types,getSolved(ctx.message.author.id))
  random.shuffle(problems)
  for i in problems:
    await ctx.send("https://cses.fi/problemset/task/"+i)
  
bot.run('token')
