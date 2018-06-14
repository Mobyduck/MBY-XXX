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


async def fetch_name(session, url):
    '''Returns the name paramater of the given page.'''
    async with session.get(url) as response:
        a = await response.text()
        b = json.loads(a)
        return b['name']


def save_to_file(file, dict):
    w = open(file, 'wb')
    pickle.dump(dict, w)
    w.close()
    print('Dictionary updated:')


async def main():
    async with aiohttp.ClientSession() as session:
        # Create the skills dictionary
        skills = await fetch_list(session, 'https://api.guildwars2.com/v2/skills')
        for i in range(len(skills)):
            if skills[i] in skills_dictionary:
                print('ID', skills[i], 'already found in file. Skipping to next.')
            else:
                html = 'https://api.guildwars2.com/v2/skills/' + str(skills[i])
                print(html)
                skill_name = await fetch_name(session, html)
                skills_dictionary[skills[i]] = skill_name
                save_to_file('skills.data', skills_dictionary)
                print(skills[i], 'saved to file.')
                time.sleep(5)
        # Create the items dictionary
        items = await fetch_list(session, 'https://api.guildwars2.com/v2/items')
        for i in range(len(items)):
            if items[i] in item_dictionary:
                print('ID', items[i], 'already found in file. Skipping to next.')
            else:
                html = 'https://api.guildwars2.com/v2/items/' + str(items[i])
                print(html)
                item_name = await fetch_name(session, html)
                item_dictionary[items[i]] = item_name
                save_to_file('items.data', item_dictionary)
                print(items[i], 'saved to file.')
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
