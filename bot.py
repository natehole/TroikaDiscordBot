import os
import random
import sys

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')

END_OF_ROUND = 'End The Round'

# # Initialize the lists used to store the bag and turn log.
# bag = [END_OF_ROUND]
# total_bag = [END_OF_ROUND]
# turn_log = []


# # General dice rolling function
# # Returns first die, second die, total of both dice
# def roll_dice():
# 	die1 = random.randint(1,7)
# 	die2 = random.randint(1,7)
# 	return die1,die2,die1+die2

# # Initialize stuff as the bot comes online.
# @bot.event
# async def on_ready():	
# 	bag.clear()
# 	total_bag.clear()
# 	bag.extend([END_OF_ROUND])
# 	total_bag.extend([END_OF_ROUND])
# 	print(f'{bot.user.name} has connected to Discord!')

# # Command to empty the bag of all tokens, then return the End The Round token to the bag.
# @bot.command(name='empty',help='Empties the bag (except End The Round token) and clears log.')
# async def empty(ctx):
# 	bag.clear()
# 	total_bag.clear()
# 	turn_log.clear()
# 	bag.extend([END_OF_ROUND])
# 	total_bag.extend([END_OF_ROUND])
# 	await ctx.send('Bag Emptied')

# # Command to add tokens to the bag
# # Format: add [number] [token name]
# @bot.command(name='add', help='Adds [number] [tokens] to the bag. May add more than one entity at a time.')
# async def add(ctx, *args):
# 	output_string = ''
# 	for i in range(0,len(args),2):
# 		token_count = args[i]
# 		token_name = args[i+1]
# 		try:
# 			token_count = int(token_count)
# 			bag.extend(token_count*[token_name])
# 			total_bag.extend(token_count*[token_name])
# 			output_string += 'Added {} tokens for {}.\n'.format(token_count, token_name)
# 		except TypeError:
# 			output_string += 'I\'m pretty sure \'{}\' isn\'t a number.\n'.format(token_count)
# 		except ValueError:
# 			output_string += 'I\'m pretty sure \'{}\' isn\'t a number.\n'.format(token_count)
# 		except IndexError:
# 			output_string += 'I think you forgot an input, there were an odd number of them.\n'
# 		except:
# 			output_string += 'What did you do? Something here caused an issue: {} {}\n'.format(args[i],args[i+1])
# 	await ctx.send(output_string)

# # Command to remove tokens from the bag
# # format: remove [number] [token name]
# @bot.command(name='remove', help='Removes [number] [tokens] from the bag.')
# async def remove(ctx, number_of_tokens: int, name_of_tokens: str):
# 	in_bag = total_bag.count(name_of_tokens)
# 	if in_bag>=number_of_tokens:
# 		for i in range(number_of_tokens):
# 			total_bag.remove(name_of_tokens)
# 		await ctx.send('Removed {} {} tokens.'.format(number_of_tokens,name_of_tokens))
# 	else:
# 		await ctx.send('Cannot remove {} {} tokens, only {} in bag.'.format(number_of_tokens,name_of_tokens,in_bag))

# # command to draw a token from the bag
# @bot.command(name='draw',help='Draw a token from the bag.')
# async def draw(ctx):
# 	if len(bag)>0:
# 		random.shuffle(bag)
# 		drawn_token = bag.pop()
# 		if drawn_token == END_OF_ROUND:
# 			turn_log.extend(['Round End'])
# 			await ctx.send('**The Round Ends!**\nReturn all tokens to the bag.\nRemove tokens from dead characters and enemies, and resolve any (End of) Round activities.\nThen draw a new token.')
# 		else:
# 			turn_log.extend([drawn_token])
# 			await ctx.send(drawn_token)
# 	else:
# 		await ctx.send('The bag is empty, nothing to draw! You should probably *return* the tokens to the bag.')

# # Command to return all drawn tokens to the bag
# @bot.command(name='return',help='Return all tokens to the bag.')
# async def reset(ctx):
# 	bag.clear()
# 	bag.extend(total_bag)
# 	await ctx.send('All tokens shuffled into bag.')

# # Command to display the current contents of the bag, as well as all tokens (including drawn, but not removed tokens)
# @bot.command(name='display',help='Displays current and total bag contents.')
# async def display_current(ctx):
# 	bag.sort()
# 	items = set(total_bag)
# 	counts = [(total_bag.count(item), bag.count(item)) for item in items]
# 	item_counts = zip(items,counts)
# 	output_string = "```{:<20}|{:<10}| {:<10}\n".format('Token','Total','Current')
# 	output_string += '-'*42
# 	output_string += '\n'

# 	for item in item_counts:
# 		output_string += "{:<20}|{:<10}| {:<10}\n".format(item[0],item[1][0],item[1][1])
# 	output_string +='```'
# 	await ctx.send(output_string)

# # Command to show the turn log
# # By default will contain all bag actions
# @bot.command(name='log',help='Display initiative log.')
# async def log(ctx):
# 	output_string = ''
# 	for i,l in enumerate(turn_log):
# 		output_string += '{}. {}\n'.format(i+1,l)
# 	await ctx.send(output_string)

# # Command to add an entry to the log
# # format: entry [log text]
# # This lets you put notes for any events you want to keep logged (such as deaths, or changes, or whatever)
# @bot.command(name='entry',help='Add an entry to the log.')
# async def log(ctx,*entry):
# 	turn_log.extend([" ".join(entry)])
# 	await ctx.send('Log entry recorded.')

# helper function
def roll(sides):
    return random.randint(1, sides + 1)

@bot.event
async def on_ready():
	print(f'{bot.user.name} has connected to Discord!')

# Command to generate a character
@bot.command(name='gen-char', help='Generate Skill, Luck, Stamina, and Background')
async def generateCharacter(ctx):
    try:
        skill_roll = roll(3)
        skill_total = skill_roll + 3
        skill_str = 'Skill -> 1d3 + 3 -> ({}) + 3'.format(skill_roll, skill_total)

        stamina_roll_one = roll(6)
        stamina_roll_two = roll(6)
        stamina_total = stamina_roll_one + stamina_roll_two  + 12
        stamina_str = 'Stamina -> 2d6 + 12 -> ({} + {}) + 12 -> {}'.format(stamina_roll_one, stamina_roll_two, stamina_total)
        
        luck_roll = roll(6)
        luck_total = luck_roll + 6
        luck_str = 'Luck -> 1d6 + 6 -> ({}) + 6 -> {}'.format(luck_roll, luck_total)

        pence_total = roll(6) + roll(6)
        pence_str = 'Pence -> 2d6 -> {}'.format(pence_total)

        background_option_one = str(roll(6)) + str(roll(6))
        background_option_one_str = 'Character Background #1 -> {}'.format(background_option_one)
        background_option_two = str(roll(6)) + str(roll(6))
        background_option_two_str = 'Character Background #2 -> {}'.format(background_option_two)

        output_list = [
            'Character generated',
            skill_str,
            stamina_str,
            luck_str,
            pence_str,
            background_option_one_str,
            background_option_two_str
        ]

        output_string = [item + '\n' for item in output_list]
    except:
        output_string = 'IDK what happened boss {}'.format(sys.exc_info()[0])
    await ctx.send(output_string)

bot.run(TOKEN)