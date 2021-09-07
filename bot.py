import os
import discord
from game import game
import math
from discord.ext.commands import Bot
import asyncio
import time


client = Bot("$")


@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.command()
async def test(ctx):
  await ctx.send('Nice Test')


@client.command()
async def play(ctx):
  list = game.build_csvlist()
  round = 1
  await ctx.send('Welcome to Higher or Lower (Runescape Edition)\nAssume ALL bolts,darts,etc to be a stack of ONE')
  item_list = []
  while(True):
    if round == 1:
      first_item = game.pull_item()
      second_item = game.pull_item()
      item_list.append(first_item[0])
    else:
      first_item = second_item
      second_item = game.pull_item()
    if first_item[0] == second_item[0]:
      second_item = game.pull_item()
    pity = 0
    check_result = game.check_item(int(first_item[1]),int(second_item[1]),round,pity)
    upper_bound = len(list)
    lower_bound = 0
    while(check_result != 0):
      if(check_result == -1):
        pity+=1
        upper_bound = int(second_item[3])
        second_item = game.pull_item(lower_bound,upper_bound)
        while (second_item[0] in item_list) or (first_item[0] == second_item[0]):
          second_item = game.pull_item(lower_bound,upper_bound) 
        check_result = game.check_item(int(first_item[1]),int(second_item[1]),round,pity)
      else:
        pity+=1
        lower_bound = int(second_item[3])
        second_item = game.pull_item(lower_bound,upper_bound)
        while (second_item[0] in item_list) or (first_item[0] == second_item[0]):
          second_item = game.pull_item(lower_bound,upper_bound) 
        check_result = game.check_item(int(first_item[1]),int(second_item[1]),round,pity)
    item_list.append(second_item)
    if round == 1:
      score = 0
    else:
      score = math.factorial(round)-1
    await ctx.send('\nRound: ' + str(round) + ' Score: ' + str(score))
    await ctx.send('Is a(n) "' + first_item[0] + '" worth MORE \u2B06 or LESS \u2B07 than a "' + second_item[0] + '" (React)')
    print(first_item[0] + ' ' + first_item[1])
    print(second_item[0] + ' ' + second_item [1])
    first_embed=discord.Embed()
    first_embed.set_thumbnail   (url=first_item[2])
    first_embed.add_field(name=first_item[0], value="\u200b", inline=False)
    embed_msg1 = await ctx.send(embed=first_embed)

    second_embed=discord.Embed()
    second_embed.set_thumbnail   (url=second_item[2])
    second_embed.add_field(name=second_item[0], value="\u200b", inline=False)
    embed_msg2 = await ctx.send(embed=second_embed)
    await embed_msg2.add_reaction('\u2B06')
    await embed_msg2.add_reaction('\u2B07')
    first_embed.set_field_at(0,name=first_item[0], value=first_item[1], inline=False)
    second_embed.set_field_at(0,name=second_item[0], value=second_item[1], inline=False)
    
    def checkReaction(reaction, user):
      return user == ctx.author and (reaction.emoji == '\u2B06' or reaction.emoji == '\u2B07')
    result = '0'
    try:
      reaction, user = await client.wait_for('reaction_add', timeout=60.0, check = checkReaction)
      if reaction.emoji == '\u2B06':
        result = '1'
      elif reaction.emoji == '\u2B07':
        result = '2'
      else:
        break
    except asyncio.TimeoutError:
      await ctx.send('... ok :/ (60s timeout)')
      break
    if game.correct(int(first_item[1]),int(second_item[1]),result):
      await ctx.send('Correct! The actual prices are ^^^\n')
      await embed_msg1.edit(embed=first_embed)
      await embed_msg2.edit(embed=second_embed)
      time.sleep(2)
      round += 1
    else:
      await ctx.send('Nope thats incorrect! The actual prices are ^^^\n')
      await embed_msg1.edit(embed=first_embed)
      await embed_msg2.edit(embed=second_embed)
      break
  await ctx.send("Thanks for playing!")




client.run(os.getenv('bot_code'))