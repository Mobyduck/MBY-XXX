# For now this script will serve as the main interaction with the Guild Wars 2 API.
# It

import pickle
import aiohttp
import asyncio
import json
import math

def load_dictionaries():
    # Load the skills list
    s = open('bin\skills.data', 'rb')
    skills = {}
    skills = pickle.load(s)
    s.close()
    # Load the items list
    i = open('bin\items.data', 'rb')
    items = {}
    items = pickle.load(i)
    i.close()
    return skills, items


def gold_conversion(units: int):
    """This function receives an int and converts it to gold units.
    For example: 18000005 = 1800g 00s 05c"""
    if math.isnan(units):
        raise TypeError("Function 'gold_conversion' expected a number.")
    copper = int(math.remainder(units, 100))
    units = math.floor(units / 100)
    silver = int(math.remainder(units, 100))
    gold = int(math.floor(units / 100))
    result = '' + str(gold) + 'g ' + str(silver) + 's ' + str(copper) + 'c'
    return result


async def fetch_recipes(name, dict, id_dict):
    """This function receives an item name and checks it against the dictionary.
    Returns False if not found."""
    recipe_info = []
    url = ''
    if name not in dict:
        return 0, 0
    async with aiohttp.ClientSession() as session:
        search_url = 'https://api.guildwars2.com/v2/recipes/search?output=' + dict[name]
        async with session.get(search_url) as response:
            y = await response.text()
            recipe_list = json.loads(y)
            recipe_list_length = len(recipe_list)
            if recipe_list_length == 0:
                session.close()
                return 1, 1
            else:
                recipe_ids = ''
                url = 'https://api.guildwars2.com/v2/recipes?ids='
                for i in range(recipe_list_length):
                    recipe_ids = recipe_ids + str(recipe_list[i]) + ','
                url += recipe_ids
        async with session.get(url) as other_response:
            z = await other_response.text()
            recipe_info = json.loads(z)

    return recipe_info, recipe_list_length


async def fetch_item(name, dict):
    """This function receives an item name and checks against the dictionary.
    Returns False if not found, else returns json dictionary with desired information."""
    # First check if the skill exists
    if name not in dict:
        return False
    # Start the session
    async with aiohttp.ClientSession() as session:
        url = 'https://api.guildwars2.com/v2/items/' + dict[name]
        tp_url = 'https://api.guildwars2.com/v2/commerce/prices/' + dict[name]
        async with session.get(tp_url) as tp_response:
            tp_a = await tp_response.text()
            tp_b = json.loads(tp_a)
            tp_buy_price = gold_conversion(tp_b['buys']['unit_price'])
            tp_sell_price = gold_conversion(tp_b['sells']['unit_price'])
        async with session.get(url) as response:
            a = await response.text()
            b = json.loads(a)
            extra_info = False
            b['extra_info'] = extra_info
            b['tp_buy_price'] = tp_buy_price
            b['tp_sell_price'] = tp_sell_price
            # If no default description, add a fake one.
            try:
                print(b['description'])
            except KeyError:
                b['description'] = 'No available description.'
            # Grab 'Extra' information according to type.
            # For weapons we just want the kind of weapon: 'LongBow', 'Axe', etc.
            if b["type"] == 'Weapon':
                b['type'] = 'Weapon - ' + b['details']['type']
            # For armor we want the weight class ('light', 'medium', 'heavy')
            # as well as kind ('boots', 'coat') and restrictions, if those exist ('Sylvari', 'Charr')
            elif b['type'] == 'Armor':
                b['type'] = b['details']['weight_class'] + ' armor - ' + b['details']['type']
                try:
                    x = 1/len(b['restrictions'])
                    b['extra_info_name'] = 'Restrictions'
                    extra_info = ''
                    for i in range(len(b['restrictions'])):
                        extra_info += b['restrictions'][i]
                        if i != len(b['restrictions']) - 1:
                            extra_info += ', '
                    b['extra_info'] = extra_info
                except ZeroDivisionError:
                    pass
            # For "UpgradeComponent" we want bonuses, which can be under different names.
            elif b['type'] == 'UpgradeComponent':
                b['type'] = 'Upgrade Component'
                try:
                    x = 1/len(b['details']['bonuses'])
                    extra_info = ''
                    for i in range(len(b['details']['bonuses'])):
                        extra_info += b['details']['bonuses'][i]
                        if i != len(b['details']['bonuses']) - 1:
                            extra_info += ', '
                except KeyError:
                    extra_info = b['details']['infix_upgrade']['buff']['description']
                b['extra_info'] = extra_info
                b['extra_info_name'] = 'Bonuses'
    return b
