import discord
import logging
import pywars

logging.basicConfig(level=logging.DEBUG)

TOKEN = '***'

client = discord.Client()

skills_dictionary_id = {}
items_dictionary_id = {}
skills_dictionary = {}
items_dictionary = {}

@client.event
async def on_member_join(member):
    # This function is called when a new member joins the server
    if member.bot:
        return
    else:
        message = '''Hi there, {0}!\n
        \n
        Welcome!'''.format(member)
        await client.send_message(member, message)


@client.event
async def on_message(message):
    # This event is called whenever a new message is sent to the server
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}!'.format(message)
        await client.send_message(message.channel, msg)

    # !skill command
    # paramaters: !skill <name of the skill>
    # returns: basic info about the skill
    if message.content.startswith('!skill'):
        cmd = message.content.split()
        if len(cmd) <= 1:
            msg = 'The correct command is "!skill <name of the skill>"'
            await client.send_message(message.channel, msg)
        else:
            del cmd[0]
            sk_name = ' '
            sk_name = sk_name.join(cmd)
            msg = 'The skill you are looking for is ' + sk_name
            await client.send_message(message.channel, msg)

    # !item command
    # paramaters: !item <name of the item>
    # returns: basic info about the item
    if message.content.startswith('!item'):
        cmd = message.content.split()
        if len(cmd) <= 1:
            msg = 'The correct command is "!item <name of the item>"'
            await client.send_message(message.channel, msg)
        else:
            cmd[0] = 'The item you are looking for is'
            msg = ' '
            msg = msg.join(cmd)
            await client.send_message(message.channel, msg)


@client.event
async def on_ready():
    # This event is called after a sucessful login
    print('-----------')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----------')


# Initial setup
# Load our dictionaries
skills_dictionary, items_dictionary = load_dictionaries()
print('-----------')
print('Dictionaries loaded')
print('Pairs in Skills dictionary (ID first):', len(skills_dictionary_id))
print('Pairs in Items dictionary (ID first):', len(items_dictionary_id))
print('-----------')
# Invert dictionaries so names come first
skills_dictionary = {a: b for b, a in skills_dictionary_id.items()}
items_dictionary = {a: b for b, a in items_dictionary.items()}
print('-----------')
print('Dictionaries inverted')
print('Pairs in Skills dictionary (name first):', len(skills_dictionary))
print('Pairs in Items dictionary (name first):', len(items_dictionary))
print('-----------')

client.run(TOKEN)
