import discord
import logging
import pywars
import guild_members

logging.basicConfig(level=logging.DEBUG)

TOKEN = '***'

bot = discord.Client()

@bot.event
async def on_member_join(member):
    # This function is called when a new member joins the server
    if member.bot:
        return
    else:
        message = '''Hi there, {0}!\n
        \n
        Welcome!'''.format(member)
        await bot.send_message(member, message)


@bot.event
async def on_message(message):
    # This event is called whenever a new message is sent to the server
    # we do not want the bot to reply to itself
    if message.author == bot.user:
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
        await bot.send_message(message.author, embed=help_message)

    # !skill command
    # paramaters: !skill <name of the skill>
    # returns: basic info about the skill
    if message.content.startswith('!skill'):
        cmd = message.content.split()
        if len(cmd) <= 1:
            msg = 'The correct command is "!skill <name of the skill>"'
            await bot.send_message(message.channel, msg)
        else:
            del cmd[0]
            sk_name = ' '
            sk_name = sk_name.join(cmd)
            msg = 'The skill you are looking for is ' + sk_name
            await bot.send_message(message.channel, msg)

    # !item command
    # paramaters: !item <name of the item>
    # returns: basic info about the item
    if message.content.startswith('!item'):
        cmd = message.content.split()
        if len(cmd) <= 1:
            msg = 'The correct command is "!item <name of the item>"'
            await bot.send_message(message.channel, msg)
        else:
            del cmd[0]
            it_name = ' '
            it_name = it_name.join(cmd)
            it_name = it_name.lower()
            it_info = await pywars.fetch_item(it_name, items_dictionary)
            if it_info == False:
                msg = 'No such item found. Be sure to type the name as it appears in the game.'
                await bot.send_message(message.channel, msg)
            else:
                # Create embed message
                print(it_info['id'])
                item = discord.Embed(type='rich', title=it_info['name'], colour=rarity[it_info['rarity']], description=it_info['description'])
                item.set_thumbnail(url=it_info['icon'])
                item.set_footer(text='Info provided by the Guild Wars 2 API v2.', icon_url='https://wiki.guildwars2.com/images/d/df/GW2Logo_new.png')
                item.add_field(name='Rarity', value=it_info['rarity'])
                item.add_field(name='Type', value=it_info['type'])
                if it_info['extra_info']:
                    item.add_field(name=it_info['extra_info_name'], value=it_info['extra_info'])
                temp = it_info['name'].split()
                it_wiki = '%20'
                it_wiki = it_wiki.join(temp)
                item.add_field(name='Wiki Link', value='https://wiki.guildwars2.com/wiki/' + it_wiki, inline=False)
                await bot.send_message(message.channel, embed=item)

    # !recipe command
    if message.content.startswith('!recipe'):
        cmd = message.content.split()
        if len(cmd) <= 1:
            msg = 'The correct command is "!recipe <name of the item>"'
            await bot.send_message(message.channel, msg)
        else:
            del cmd[0]
            rcp_name = ' '
            rcp_name = rcp_name.join(cmd)
            rcp_name = rcp_name.lower()
            rcp_info, rcp_length = await pywars.fetch_recipes(rcp_name, items_dictionary, items_dictionary_id)
            it_info = await pywars.fetch_item(rcp_name, items_dictionary)
            if rcp_info == 0:
                msg = 'No such item found. Be sure to type the name as it appears in the game.'
                await bot.send_message(message.channel, msg)
            elif rcp_info == 1:
                msg = 'This item does not have a recipe in the system.'
                await bot.send_message(message.channel, msg)
            else:
                title_em = 'Recipes for ' + rcp_name
                description_em = "I've found " + str(rcp_length) + " recipes"
                rcp_em = discord.Embed(type='rich', title=title_em, colour=rarity[it_info['rarity']], description=description_em)
                rcp_em.set_thumbnail(url=it_info['icon'])
                for i in range(rcp_length):
                    ing_list = ''
                    for y in range(len(rcp_info[i]['ingredients'])):
                        ing_list = ing_list + items_dictionary_id[str(rcp_info[i]['ingredients'][y]['item_id'])] + ' x ' + str(rcp_info[i]['ingredients'][y]['count']) + '\n'
                    cur_recipe = i + 1
                    recipe_title_em = 'Recipe ' + str(cur_recipe)
                    rcp_em.add_field(name=recipe_title_em, value=ing_list)
                temp = it_info['name'].split()
                it_wiki = '%20'
                it_wiki = it_wiki.join(temp)
                rcp_em.add_field(name='Wiki Link', value='https://wiki.guildwars2.com/wiki/' + it_wiki, inline=False)
                rcp_em.set_footer(text='Info provided by the Guild Wars 2 API v2.', icon_url='https://wiki.guildwars2.com/images/d/df/GW2Logo_new.png')
                await bot.send_message(message.channel, embed=rcp_em)


@bot.event
async def on_ready():
    # This event is called after a sucessful login
    print('-----------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-----------')
    if bot.user.name != bot_version:
        await bot.edit_profile(username=bot_version)
        print('Set username to', bot_version)
    bot_game = discord.Game(name='type !help')
    await bot.change_presence(game=bot_game)



# Setup
## Bot version
bot_version = 'MBY-003'
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
# This should help stopping returning bad IDs when they have the same name value.
for a, b in skills_dictionary_id.items():
    b = b.lower()
    if b not in skills_dictionary:
        skills_dictionary[b] = a
    else:
        pass
for a, b in items_dictionary_id.items():
    b = b.lower()
    if b not in items_dictionary:
        items_dictionary[b] = a
    else:
        pass
print('-----------')
print('Dictionaries inverted')
print('Pairs in Skills dictionary (name first):', len(skills_dictionary))
print('Pairs in Items dictionary (name first):', len(items_dictionary))
print('-----------')

bot.run(TOKEN)
