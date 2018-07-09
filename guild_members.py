"""This script takes care of the users' informations:
Guild Wars 2 access API;
Discord ID."""

class Guild_Member:

    member_count = 0

    def __init__(self, discord_id, name):
        self.discord_id = discord_id
        self.name = name
        Guild_Member.member_count += 1

    def register_api(self, api):
        self.api = api
