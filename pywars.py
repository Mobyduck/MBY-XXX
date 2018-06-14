# For now this script will serve as the main interaction with the Guild Wars 2 API.
# It should be able to grab any information from the site and return the relevant bits.

import pickle
import aiohttp
import asyncio
import json

def load_dictionaries():
    # Load the skills list
    s = open('bin\skills.data', 'rb')
    skills = {}
    skills = pickle.load(s)
    s.close()

    i = open('bin\items.data', 'rb')
    items = {}
    items = pickle.load(i)
    i.close()
    return skills, items


async def fetch_info(name, dict):
    """This function receives a skill or item name and checks against the dictionary.
    Returns False if not found, else returns tuple with desired information."""
    # First check if the skill exists
    if name not in dict:
        return False
    # Start the session
    async with aiohttp.ClientSession() as session:
        url = 'https://api.guildwars2.com/v2/skills/' + str(id)
        async with session.get(url) as response:
            a = await response.text()
            b = json.loads(a)
            print('Name:', b['name'])
            print('Description:', b['description'])
            print(b['icon'])
