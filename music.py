import discord
import asyncio
import os
from discord.ext import commands
import lavalink
from discord import utils

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.music= lavalink.Client(self.bot.user.id)
        self.bot.music.add_node(os.getenv('linkhost'), os.getenv('port'), os.getenv('lavapass'), 'na', 'music-node')
        self.bot.add_listener(self.bot.music.voice_update_handler, 'on_socket_response')
        self.bot.music.add_event_hook(self.track_hook)
        
    @commands.command(name=['Join', 'Connect'], help="Joins current voice channel to play music")
    async def join(self, ctx):
        member = utils.find(lambda m: m.id == ctx.author.id, ctx.guild.members)
        if member is not None and member.voice is not None:
            vc = member.voice.channel
            player = self.bot.music.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
            if not player.is_connected:
                player.store('channel', ctx.channel.id)
                await self.connect_to(ctx.guild.id, str(vc.id))

    @commands.command(name='Play', help="Simple music player")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def play(self, ctx, *, query):
        try:
            await ctx.invoke(self.join)
            player = self.bot.music.player_manager.get(ctx.guild.id)
            query = f"ytsearch:{query}"
            results = await player.node.get_tracks(query)
            tracks = results['tracks'][0:10]
            i = 0
            query_result = ''
            for track in tracks:
                i = i + 1
                query_result = query_result + f'`{i}.)` {track["info"]["title"]} - {track["info"]["uri"]}\n'
            embed = discord.Embed()
            embed.description = query_result
            await ctx.channel.send(embed=embed)
            try:
                def verify(m):
                    return m.content and m.author == ctx.author and m.channel == ctx.channel
                response = await self.bot.wait_for('message', timeout=60, check=verify)
                track = tracks[int(response.content)-1]
                player.add(requester=ctx.author.id, track=track)
                if not player.is_playing:
                    await player.play()
            except asyncio.TimeoutError:
                await ctx.send("Timeout")
        except Exception as error:
            print(error)
    @play.error
    async def play_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)
            return
        else:
            raise error

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            await self.connect_to(guild_id, None)

    async def connect_to(self, guild_id: int, channel_id: str):
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)

def setup(bot):
    bot.add_cog(Music(bot))