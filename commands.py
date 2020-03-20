import discord
import os
import psycopg2
from discord.ext import commands

MissingPerm = MissingPerm = "💌 | Missing permissions. Please make sure I have all the necessary permissions to properly work!\nPermissions such as: `Manage Channels`, `Read Text Channels & See Voice Channels`, `Send Messages`, `Manage Messages`, `Use External Emojis`, `Connect`, `Move Members`"

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='Lg', help='Bot goes offline')
    @commands.guild_only()
    async def boutaheadout(self, ctx):
        if ctx.author.id == 649813303836672010 or ctx.author.id == 609329952180928513:
            try:
                await ctx.message.delete()
                await self.bot.close()
                print(f"{self.bot.user.name} has went offline.")
            except discord.Forbidden:
                try:
                    await ctx.send(MissingPerm)
                except discord.Forbidden:
                    return

    @commands.command(name='L', help='Loads a cog.')
    async def load(self, ctx, extension):
        if ctx.author.id == 649813303836672010 or ctx.author.id == 609329952180928513:
            try:
                try:
                    self.bot.load_extension(extension)
                    await ctx.send(f'Loaded {extension}')
                    print(f"Loaded {extension}")
                except Exception as error:
                    await ctx.send(f'{extension} could not be loaded. [{error}]')
            except discord.Forbidden:
                return

    @commands.command(name='U', help='Unloads a cog.')
    async def unload(self, ctx, extension):
        if ctx.author.id == 649813303836672010 or ctx.author.id == 609329952180928513:
            try:
                try:
                    if extension != 'commands':
                        self.bot.unload_extension(extension)
                        await ctx.send(f'Unloaded {extension}')
                        print(f"Unloaded {extension}")
                    else:
                        await ctx.send("Please try reloading this script instead!")
                        print("Please try reloading this script instead!")
                except Exception as error:
                    await ctx.send(f'{extension} could not be unloaded. [{error}]')
            except discord.Forbidden:
                return
    
    @commands.command(name='R', help='Reloads a cog.')
    async def reload(self, ctx, extension):
        if ctx.author.id == 649813303836672010 or ctx.author.id == 609329952180928513:
            try:
                try:
                    self.bot.unload_extension(extension)
                    con = await ctx.send(f'Unloaded {extension}')
                    self.bot.load_extension(extension)
                    await con.edit(content=f'Reloaded {extension}')
                    print(f"Reloaded {extension}")
                except Exception as error:
                    await ctx.send(f'{extension} could not be reloaded. [{error}]')
            except discord.Forbidden:
                return
    
    @commands.command(name='Rolelink', help='Link embeds for my server roles.') # Personal command
    @commands.is_owner()
    async def role_link(self, ctx):
        try:
            linkembed = discord.Embed(
                    title='CLICK THE LINK TO HAVE IT BRING YOU TO THE ROLES',
                    description='',
                    color=discord.Color.purple()
            )
            linkembed.add_field(name='`🌈 Color`', value='[Click Here](https://discordapp.com/channels/647205092029759488/647285590659694612/647707491169206302)', inline=True)
            linkembed.add_field(name='`🌈 Color list`', value='[Click Here](https://discordapp.com/channels/647205092029759488/647285590659694612/647708228406345739)', inline=True)
            linkembed.add_field(name='`🤖 Bot Paradise`', value='[Click Here](https://discordapp.com/channels/647205092029759488/647285590659694612/647708342785146930)', inline=True)
            linkembed.add_field(name='`🏳️‍🌈 Gender`', value='[Click Here](https://discordapp.com/channels/647205092029759488/647285590659694612/647708520497807361)', inline=True)
            linkembed.add_field(name='`🔢 Age`', value='[Click Here](https://discordapp.com/channels/647205092029759488/647285590659694612/647708744561590272)', inline=True)
            linkembed.add_field(name='`❤️ Sexuality`', value='[Click Here](https://discordapp.com/channels/647205092029759488/647285590659694612/647708976502407179)', inline=True)
            linkembed.add_field(name='`🔒 DM Status`', value='[Click Here](https://discordapp.com/channels/647205092029759488/647285590659694612/647709123323887626)', inline=True)
            linkembed.add_field(name='`🗺️ Continent`', value='[Click Here](https://discordapp.com/channels/647205092029759488/647285590659694612/647709296284663820)', inline=True)
            linkembed.add_field(name="`🏠 Squee's House Category`", value='[Click Here](https://discordapp.com/channels/647205092029759488/647285590659694612/647709461317812246)', inline=True)

            await ctx.send(embed=linkembed)
        except discord.Forbidden:
            return

    @commands.command(name='Test', help="For testing purposes.") # Personal command
    @commands.is_owner()
    async def test(self, ctx):
        try:
            tstcmd = self.bot.get_command('tst')
            await ctx.invoke(tstcmd)
            await ctx.send(ctx)
        except discord.Forbidden:
            return
    @commands.command(name='Tst', help="For testing purposes.") # Personal command
    @commands.is_owner()
    async def tst(self, ctx):
        try:
            if self.bot.get_channel(688233415048429609) == None:
                lol = 'empty'
            else:
                lol = 'notempy'
            await ctx.send(lol)
        except discord.Forbidden:
            return

    @commands.command(name='Ping', help="Shows bot's latency in milliseconds.")
    async def ping(self, ctx):
        try:
            await ctx.send(f'Pong: {round(self.bot.latency * 1000)}ms')
        except discord.Forbidden:
            return

    @commands.command(name='Join', help='Has the bot join the vc. Mainly for testing purposes.')
    @commands.guild_only()
    async def join(self, ctx):
        try:
            try:
                try:
                    try:
                        await ctx.author.voice.channel.connect()
                        await ctx.message.delete()
                    except AttributeError:
                        await ctx.send("You're not in a VC!")
                except discord.ClientException:
                    await ctx.send("I'm already in a VC!")
            except TimeoutError:
                try:
                    ctx.send(MissingPerm)
                except discord.Forbidden:
                    return
        except discord.Forbidden:
            try:
                await ctx.send(MissingPerm)
            except discord.Forbidden:
                return
    @commands.command(name='Leave', help='Has the bot leave the vc. Mainly for testing purposes.')
    @commands.guild_only()
    async def leave(self, ctx):
        try:
            try:
                    await ctx.voice_client.disconnect()
                    await ctx.message.delete()
            except AttributeError:
                    await ctx.send("I'm not in a VC!")
        except discord.Forbidden:
            try:
                await ctx.send(MissingPerm)
            except discord.Forbidden:
                return

    @commands.command(name='Status', help="Changes bot's status message.") # Anyone can use this command and it changes the bot's status.
    async def status(self, ctx, *, changestatus=None): # example(*, args) : ex. "Example text" | example(*args) : ex. "Example" "text"
        try:
            DATABASE_URL = os.environ['DATABASE_URL']
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        except KeyError:
            conn = psycopg2.connect(database=os.getenv('database'), user=os.getenv('user'), password=os.getenv('password'))
        finally:
            cur =conn.cursor()
            if changestatus == None:
                cur.execute("UPDATE bot SET message = '' WHERE name = 'Status';")
                conn.commit()
                await self.bot.change_presence(activity=discord.Game(''))
            elif len(changestatus) <= 128:
                if 'https://' in changestatus:
                    await ctx.send('No links.')
                else:
                    cur.execute(f"UPDATE bot SET message = '{changestatus}' WHERE name = 'Status';")
                    conn.commit()
                    await self.bot.change_presence(activity=discord.Game(changestatus))
            elif len(changestatus) >= 128:
                await ctx.send(f"Character limit is 128. You reached {len(changestatus)} characters.")
            cur.close()
            conn.close()

def setup(bot):
    bot.add_cog(Commands(bot))