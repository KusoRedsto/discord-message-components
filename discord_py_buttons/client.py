import discord
from discord.ext import commands
from .receive import PressedButton

from . import apiRequests
from .receive import Message, getResponseMessage

class Buttons:
    def __init__(self, client: commands.Bot):
        self._discord = client
        # self.listen_interaction_create()

        self._discord.add_listener(self.on_socket_response)
    
    async def on_socket_response(self, msg):
        if msg["t"] != "INTERACTION_CREATE":
            return
        data = msg["d"]

        if data["type"] != 3:
            return
        
        guild = await self._discord.fetch_guild(data["guild_id"])
        user = discord.Member(data=data["member"], guild=guild, state=self._discord._connection)
        
        msg = await getResponseMessage(self._discord, data, user, True)

        self._discord.dispatch("button_press", msg.pressedButton, msg)
    

    async def send(self, channel: discord.TextChannel, content=None, *, tts=False,
            embed=None, file=None, files=None, delete_after=None, nonce=None,
            allowed_mentions=None, reference=None, mention_author=None, buttons=None
        ) -> Message:
        if type(channel) != discord.TextChannel:
            raise discord.InvalidArgument("Channel must be of type discord.TextChannel")
        r = apiRequests.POST(self._discord.http.token, f"{apiRequests.url}/channels/{channel.id}/messages", data=apiRequests.jsonifyMessage(content, tts=tts, embed=embed, file=file, files=files, nonce=nonce, allowed_mentions=allowed_mentions, reference=reference, mention_author=mention_author, buttons=buttons))
        if(r.status_code != 200):
            raise Exception(r.text)
        return await getResponseMessage(self._discord, r.json(), False)