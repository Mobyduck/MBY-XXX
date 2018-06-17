import discord
import logging
import pywars

logging.basicConfig(level=logging.DEBUG)

TOKEN = '***'

client = discord.Client()

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

    if message.content.startswith('!help'):
        help_message = discord.Embed(title="Welcome to MBY's help document!", colour=rarity['Exotic'], description="Hi, my name is {0}, and I'm here to assist you! As a servant bot, I desire nothing more than to help you receive all the information you want! Below is a list of all of my commands, and how to correctly use them. I recommend reading it all, since I have many functions!".format(bot_version))
        help_message.add_field(name='List of Commands', value="""
**!help**
Returns the message you are reading right now!
It contains lots of info about all the other commands.

**!skill** *Name of Skill*
Returns information about the skill you want.
This includes description, chat link and profession.

**!item** *Name of Item*
Returns information about item you want.
This includes description, type, rarity, chat link and level.

**!recipe** *Name of Item*
Returns information about the crafting of the desired item.
This includes name of all components and their prices in the auction house, if available.

**!price** *Name of Item*
Returns information about the cost of the item you want.
This includes from vendors and the auction house.""")
        await client.send_message(message.author, embed=help_message)

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
            del cmd[0]
            it_name = ' '
            it_name = it_name.join(cmd)
            it_info = await pywars.fetch_info(it_name, items_dictionary, type='items')
            if it_info == False:
                msg = 'No such item found. Be sure to type the name as it appears in the game.'
                await client.send_message(message.channel, msg)
            else:
                # Create embed message
                item = discord.Embed(type='rich', title=it_name, colour=rarity[it_info['rarity']], description=it_info['description'])
                item.set_thumbnail(url=it_info['icon'])
                item.set_footer(text='Info provided by the Guild Wars 2 API v2.', icon_url='https://wiki.guildwars2.com/images/d/df/GW2Logo_new.png')
                item.add_field(name='Rarity', value=it_info['rarity'])
                item.add_field(name='Type', value=it_info['type'])
                temp = it_name.split()
                it_wiki = '%20'
                it_wiki = it_wiki.join(temp)
                item.add_field(name='Wiki Link', value='https://wiki.guildwars2.com/wiki/' + it_wiki)
                await client.send_message(message.channel, embed=item)


@client.event
async def on_ready():
    # This event is called after a sucessful login
    print('-----------')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----------')
    await client.edit_profile(username=bot_version)
    print('Set username to', bot_version)


# Setup
## Bot version
bot_version = 'MBY-001'
bot_avatar = 'https://pbs.twimg.com/profile_images/1002920144883081216/hYtXo5ak_400x400.jpg'
## Skill and Item dictionaries
skills_dictionary_id = {}
items_dictionary_id = {}
skills_dictionary = {}
items_dictionary = {}
## Color scheme according to rarity
## Used in the embed function to define the color according to rarity.
rarity = {'Junk': 0xAAAAAA, 'Fine': 0x62A4DA, 'Basic': 0x000000, 'Masterwork': 0x1A9306, 'Rare': 0xFCD00B, 'Exotic': 0xFFA405, 'Ascended': 0xFB3E8D, 'Legendary': 0x4C139D}

# Initial setup
# Load our dictionaries
skills_dictionary_id, items_dictionary_id = pywars.load_dictionaries()
print('-----------')
print('Dictionaries loaded')
print('Pairs in Skills dictionary (ID first):', len(skills_dictionary_id))
print('Pairs in Items dictionary (ID first):', len(items_dictionary_id))
print('-----------')
# Invert dictionaries so names come first
skills_dictionary = {a: b for b, a in skills_dictionary_id.items()}
items_dictionary = {a: b for b, a in items_dictionary_id.items()}
print('-----------')
print('Dictionaries inverted')
print('Pairs in Skills dictionary (name first):', len(skills_dictionary))
print('Pairs in Items dictionary (name first):', len(items_dictionary))
print('-----------')

client.run(TOKEN)
