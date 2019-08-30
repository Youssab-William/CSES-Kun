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

topics=[("intro","Introductory Problems"),("sorting","Sorting and Searching"),("searching","Sorting and Searching"),("dp","Dynamic Programming"),("graph","Graph Algorithms"),("rq","Range Queries"),("tree","Tree Algorithms"),("math","Mathematics"),("string","String Algorithms"),("additional","Additional Problems")]
 
    
def getTopic(top):
  top=top.lower()
  for i,j in topics:
    if top == i:
      return j
  return "Error"

def getSolved(userID):
  lst=[]
  os.system("mkdir -pv user/")
  os.system("touch user/"+str(userID)+".txt")
  filef=open("user/"+str(userID)+".txt","r")
  lines=filef.readlines()
  for i in lines:
    lst.append(str(int(i)))
  return lst
  
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

def pick(problems,solved2):
    chosen=[]
    if len(problems) == 0:
        return chosen
    graph = {}
    co=0
    for typ,l,r in problems:
        allp = getall(typ,l,r,solved2)
        if len(allp) == 0:
            continue
        random.shuffle(allp)
        graph[co] = allp
        co=co+1
    if len(graph) == 0:
        return []
    hk = HopcroftKarp(graph)
    max_matching = hk.maximum_matching()
    for i in range(0,co):
        chosen.append(max_matching[i])
    random.shuffle(chosen)
    return chosen
             
@bot.command()
async def solved(ctx , idd :int ):
    """add this problem to your solved problems list to avoid selecting it in future.
    """
    user_id = ctx.message.author.id
    os.system("mkdir -pv user/")
    os.system("touch user/"+str(user_id)+".txt")
    file1 = open("user/"+str(user_id)+".txt","r")
    lines=file1.readlines()
    file1.close()
    for i in lines:
        x = int(i)
        if x==idd:
            await ctx.send('you had already solved this problem before')
            return

    solved2=[]
    for tmp,typ in topics:
      solved2 = getall(typ, 0, 1000000000000000000000 , solved2)
      if str(idd) in solved2:
        file = open("user/"+str(user_id)+".txt","a+")
        file.write(str(idd)+"\n")
        file.close()
        await ctx.send('one more problem solved! ')
        return 
    await ctx.send('invalid problem ID')
        
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

@bot.command()
async def suggest(ctx, *args: str):
    """suggest a problem on you didn't solve which had been solved by number of users between l and r
    """
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
    if len(problems) == 0:
        await ctx.send("Couldn't find any problems")
        return
    random.shuffle(problems)
    for i in problems:
        await ctx.send("https://cses.fi/problemset/task/"+i)
