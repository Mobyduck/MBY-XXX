# This module grabs basic info (ID and name) from the API site
# and saves to a file. It first checks against existing dictionaries to sle
# if the pair is already in the system.
#
# It is important to save {'ID': 'name'} because some of the unique IDs have identical names.

import aiohttp
import asyncio
import time
import json
import pickle


async def fetch_list(session, url):
    async with session.get(url) as response:
        list = await response.text()
        list = list.replace(',','')
        list = list.split()
        del list[0]
        list.pop()
        print('Total amount of ids to save:', len(list))
        return list


async def fetch_name(session, url, quantity=10):
    '''Returns a list with the name paramater of the given IDs.'''
    names = []
    async with session.get(url) as response:
        a = await response.text()
        b = json.loads(a)
        for i in range(quantity):
            names.append(b[i]['name'])
            print(b[i]['name'], 'fetched from list.')
        return names


def save_to_file(file, dict):
    w = open(file, 'wb')
    pickle.dump(dict, w)
    w.close()
    print('Dictionary updated:')


async def main():
    async with aiohttp.ClientSession() as session:
        # Amount of IDs to be grabbed at a time
        s_target = 10
        # Create the skills dictionary
        skills = await fetch_list(session, 'https://api.guildwars2.com/v2/skills')
        for i in range(len(skills)):
            if skills[i] in skills_dictionary:
                print('ID', skills[i], 'already found in file. Skipping to next.')
            elif (len(skills) - i) >= s_target:
                # Create a string with all the 10 IDs
                print('Grabbing', s_target, 'IDs.')
                multiple_ids = ''
                for a in range(0, s_target):
                    multiple_ids += skills[i + a]
                    multiple_ids += ','
                html = 'https://api.guildwars2.com/v2/skills?ids=' + multiple_ids
                print(html)
                skill_names = await fetch_name(session, html)
                for a in range(0, s_target):
                    skills_dictionary[skills[i + a]] = skill_names[a]
                save_to_file('skills.data', skills_dictionary)
                print(multiple_ids, 'saved to file.')
                time.sleep(5)
            else:
                s_target = len(items) - i
                print('Grabbing', s_target, 'IDs.')
                multiple_ids = ''
                for a in range(0, s_target):
                    multiple_ids += skills[i + a]
                    multiple_ids += ','
                html = 'https://api.guildwars2.com/v2/skills?ids=' + multiple_ids
                print(html)
                skill_names = await fetch_name(session, html, s_target)
                for a in range(0, s_target):
                    skills_dictionary[skills[i + a]] = skill_names[a]
                save_to_file('skills.data', skills_dictionary)
                print(multiple_ids, 'saved to file.')
                time.sleep(5)
        # Create the items dictionary
        items = await fetch_list(session, 'https://api.guildwars2.com/v2/items')
        # Amount of IDs to be grabbed at a time
        i_target = 10
        for i in range(len(items)):
            if items[i] in item_dictionary:
                print('ID', items[i], 'already found in file. Skipping to next.')
            elif (len(items) - i) >= i_target:
                # Create a string with all the 10 IDs
                print('Grabbing', i_target, 'IDs.')
                multiple_ids = ''
                for a in range(0, i_target):
                    multiple_ids += items[i + a]
                    multiple_ids += ','
                html = 'https://api.guildwars2.com/v2/items?ids=' + multiple_ids
                print(html)
                item_names = await fetch_name(session, html)
                for a in range(0, i_target):
                    item_dictionary[items[i + a]] = item_names[a]
                save_to_file('items.data', item_dictionary)
                print(multiple_ids, 'saved to file.')
                time.sleep(5)
            else:
                i_target = len(items) - i
                print('Grabbing', i_target, 'IDs.')
                multiple_ids = ''
                for a in range(0, i_target):
                    multiple_ids += items[i + a]
                    multiple_ids += ','
                html = 'https://api.guildwars2.com/v2/items?ids=' + multiple_ids
                print(html)
                item_names = await fetch_name(session, html, i_target)
                for a in range(0, i_target):
                    item_dictionary[items[i + a]] = item_names[a]
                save_to_file('items.data', item_dictionary)
                print(multiple_ids, 'saved to file.')
                time.sleep(5)

# Variables
item_dictionary = {}
skills_dictionary = {}

# This setup section checks to see if a file for the dictionaries already exist
# Important for future uses, when we need to update them
try:
    # Tries to open the item dict
    r = open('items.data', 'rb')
    item_dictionary = pickle.load(r)
    r.close()
except FileNotFoundError:
    # This means the file does not exist. Let's create it.
    print('"items.data" was not found. Creating file...')
    with open('items.data', 'wb') as c:
        pickle.dump(item_dictionary, c)
    print('"items.data" created.\n')

try:
    # Tries to open the skill dict
    r = open('skills.data', 'rb')
    skills_dictionary = pickle.load(r)
    r.close()
except FileNotFoundError:
    # This means the file does not exist. Let's create it.
    print('"skills.data" was not found. Creating file...')
    with open('skills.data', 'wb') as c:
        pickle.dump(skills_dictionary, c)
    print('"skills.data" created.\n')

print('------------')
print('Dictionaries loaded.')
print('Pairs found in skills dictionary:', len(skills_dictionary))
print('Pairs found in items dictionary:', len(item_dictionary))
print('------------')

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
