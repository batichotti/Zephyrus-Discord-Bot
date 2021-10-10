import pprint
import asyncio
import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
import re

URL_REG = re.compile(r'https?://(?:www\.)?.+')
YOUTUBE_VIDEO_REG = re.compile(r"(https?://)?(www\.)?youtube\.(com|nl)/watch\?v=([-\w]+)")

class music(commands.Cog):
    def __init__(self, client):
        self.client = client

        #all the music related stuff
        self.is_playing = False
        self.event = asyncio.Event()

        # 2d array containing [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS = {
            'format': 'bestaudio/best',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            #'default_search': 'auto',
            'extract_flat': True
        }
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = ""

     #searching the item on youtube
    def search_yt(self, item):

        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                if (yt_url:=YOUTUBE_VIDEO_REG.match(item)):
                    item = yt_url.group()
                elif not URL_REG.match(item):
                    item = f"ytsearch:{item}"
                info = ydl.extract_info(item, download=False)
            except Exception: 
                return False

        try:
            entries = info["entries"]
        except KeyError:
            entries = [info]

        if info["extractor_key"] == "YoutubeSearch":

            entries = entries[:1]

        tracks = []

        for t in entries:

            tracks.append({'source': f'https://www.youtube.com/watch?v={t["id"]}', 'title': t['title']})

        #if search:
        #    tracks = {'source': info['formats'][0]['url'], 'title': info['title']}

        return tracks

    # infinite loop checking 
    async def play_music(self):

        self.event.clear()

        if len(self.music_queue) > 0:

            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            # If source was a stream (not downloaded), so we should regather to prevent stream expiration
            with YoutubeDL(self.YDL_OPTIONS) as ydl:
                try:
                    info = ydl.extract_info(m_url, download=False)
                    m_url = info['formats'][0]['url']
                except Exception:
                    return False

            #try to connect to voice channel if you are not already connected

            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])

            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda l: self.client.loop.call_soon_threadsafe(self.event.set))
            await self.event.wait()
            await self.play_music()
        else:
            self.is_playing = False
            self.music_queue.clear()
            await self.vc.disconnect()

    @commands.command(name="m_help",alisases=['ajuda'],help="Comando de ajuda com os comandos de música")
    async def help(self,ctx):
        helptxt = ''
        for command in self.client.commands:
            helptxt += f'**{command}** - {command.help}\n'
        embedhelp = discord.Embed(
            colour = 1646116,#grey
            title=f'Comandos do {self.client.user.name}',
            description = helptxt+'\n[Se inscreva no meu canal](https://www.youtube.com/channel/UChMVeWXTvteLDSMjxlPGmCA)'
        )
        embedhelp.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=embedhelp)


    @commands.command(name="play", help="Toca uma música do YouTube", aliases=['p','tocar'])
    async def p(self, ctx: commands.Context, *, query:str = "Rick Astley - Never Gonna Give You Up "):
        
        try:
            voice_channel = ctx.author.voice.channel
        except:
        #if voice_channel is None:
            #you need to be connected so that the bot knows where to go
            embedvc = discord.Embed(
                colour= 1646116,#grey
                description = 'Para tocar uma música, primeiro se conecte a um canal de voz.'
            )
            await ctx.send(embed=embedvc)
            return
        else:
            songs = self.search_yt(query)
            if type(songs) == type(True):
                embedvc = discord.Embed(
                    colour= 12255232,#red
                    description = 'Algo deu errado! Tente mudar ou configurar a playlist/vídeo ou escrever o nome dele novamente!'
                )
                await ctx.send(embed=embedvc)
            else:

                if (size:=len(songs)) > 1:
                    txt = f"Você adicionou **{size} músicas** na fila!"
                else:
                    txt = f"Você adicionou a música **{songs[0]['title']}** à fila!"

                embedvc = discord.Embed(
                    colour= 32768,#green
                    description = f"{txt}\n\n[Crie seu próprio Bot de Música](https://youtu.be/YGx0xNHzjgE)"
                )
                await ctx.send(embed=embedvc)
                for song in songs:
                    self.music_queue.append([song, voice_channel])

                if self.is_playing == False:
                    await self.play_music()

    @commands.command(name="queue", help="Mostra as atuais músicas da fila.",aliases=['q','fila'])
    async def q(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += f'**{i+1} - **' + self.music_queue[i][0]['title'] + "\n"

        print(retval)
        if retval != "":
            embedvc = discord.Embed(
                colour= 12255232,
                description = f"{retval}"
            )
            await ctx.send(embed=embedvc)
        else:
            embedvc = discord.Embed(
                colour= 1646116,
                description = 'Não existe músicas na fila no momento.'
            )
            await ctx.send(embed=embedvc)

    @commands.command(name="skip", help="Pula a atual música que está tocando.",aliases=['pular'])
    @commands.has_permissions(manage_channels=True)
    async def skip(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()
            embedvc = discord.Embed(
                colour= 1646116,#ggrey
                description = f"Você pulou a música."
            )
            await ctx.send(embed=embedvc)

    @skip.error #Erros para kick
    async def skip_error(self,ctx,error):
        if isinstance(error, commands.MissingPermissions):
            embedvc = discord.Embed(
                colour= 12255232,
                description = f"Você precisa da permissão **Gerenciar canais** para pular músicas."
            )
            await ctx.send(embed=embedvc)     
        else:
            raise error

    @commands.command(name="stop",help="Para o player de tocar músicas",aliases=["parar", "sair", "leave", "l"])
    async def stop(self, ctx: commands.Context):

        embedvc = discord.Embed(colour= 12255232)

        if not ctx.me.voice:
            embedvc.description = "Não estou conectado em um canal de voz."
            await ctx.reply(embed=embedvc)
            return

        if not ctx.author.voice or ctx.author.voice.channel != ctx.me.voice.channel:
            embedvc.description = "Você precisa estar no meu canal de voz atual para usar esse comando."
            await ctx.reply(embed=embedvc)
            return

        if any(m for m in ctx.me.voice.channel.members if not m.bot and m.guild_permissions.manage_channels) and not ctx.author.guild_permissions.manage_channels:
            embedvc.description = "No momento você não tem permissão para usar esse comando."
            await ctx.reply(embed=embedvc)
            return

        self.is_playing = False
        self.music_queue.clear()
        await self.vc.disconnect(force=True)

        embedvc.colour = 1646116
        embedvc.description = "Você parou o player"
        await ctx.reply(embed=embedvc)

def setup(client):
    client.add_cog(music(client))