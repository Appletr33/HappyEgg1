import requests
from datetime import datetime
from pytz import timezone
import discord
from discord.ext import commands, tasks
from discord.utils import get
from itertools import cycle
import json
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from random import randrange
import sherlock
import os
from gtts import gTTS
import matplotlib.pyplot as plt
import mojang
import chat.chat

client = commands.Bot(command_prefix='.')
client.remove_command('help')
status = cycle(["Getting Stats .", "Getting Stats ..", "Getting Stats ..."])
oldtime = 324
lst = ['']
daniel_lst = ["Did the floor make you pee your shorts or not?", "cum what", "Do you think saying the n word on the wrong day should affect the person who said the n word's pants?", "I have to be on do not disturb for the rest of the night because my mom is selking me", "Who is the selkers?", "Dw about it", "If EliteGentro wear glasses, then what happened next", "Should he go pee pants", "Does he look funny with glasses", "Just to clarify, did MarvelousDream become king when the lady pass away", "Homework keeps bullying me", "What date did that lady pass away", "McKayla got away from the police", "EliteGentro have comitted suicide. I'm very heartbroken rn ", "hat song got revenge on McKayla", "i was attracted to pants when i'm little", "some design are scary", "Will eggs in pockets make me gain or lose subscribers", "Just blame the ching chong chinese", "My pants size is about youth XL to Adult XS", "那裡有什麼顏色", "I want to tok tik tok like these girls do"]
started_time = datetime.now()
started_time = started_time.astimezone(timezone('US/Pacific'))
start_time_pacific = started_time.strftime("%Y-%m-%d, %I:%M %p")


def get_uuid(arg):
    try:
        namedata = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{arg}").json()
        return namedata["id"]
    except json.decoder.JSONDecodeError:
        return None


def huang():
    while True:
        item_num = randrange(len(daniel_lst))
        if item_num != lst[-1]:
            lst.append(item_num)
            item = f' "{daniel_lst[item_num]}" \t - Daniel'
            return item
        else:
            pass


def write_time():
    with open("datas.json", "r") as myfile:
        prev_time = myfile.readline()
        overall_time = int(prev_time) + 1
        myfile.close()
    with open('datas.json', 'w') as outfile:
        json.dump(overall_time, outfile)
        myfile.close()


def get_cur_game():
    try:
        data = requests.get(os.environ["HYPIXEL_TOKEN"]).json()
        if data["session"]["online"]:
            values = data["session"]["gameType"] + ' ' + data["session"]["mode"]
            return values
        else:
            return "offline"
    except:
        return "offline"


def get_data():
    result = get_cur_game()
    time = datetime.now(timezone('US/Pacific'))
    time_pacific = time.strftime("%Y-%m-%d, %I:%M:%S %p")
    playtime = json.load(open('time_played.json'))

    if result == "MAIN LOBBY":
        # Do nothing if result is MAIN LOBBY
        """
        if result not in playtime.keys():
            playtime[result] = 0.00833333333
        else:
            playtime[result] += 0.00833333333
        """

    elif "LOBBY" in result and result != "MAIN LOBBY":
        if result not in playtime.keys():
            playtime["Game Lobbies"] = 0.00833333333
        else:
            playtime["Game Lobbies"] += 0.00833333333

    else:
        results = result.split(" ", 1)
        results = results[0].replace("_", " ")
        if results not in playtime.keys():
            playtime[results] = 0.00833333333
        else:
            playtime[results] += 0.00833333333

    with open('time_played.json', 'w') as myfile:
        myfile.write(json.dumps(playtime))
        myfile.close()

    if result == "MAIN LOBBY":
        datas = "WhoDoesnt is in " + result + " Most Likely AFK: " + time_pacific
        write_time()

    elif result != "MAIN LOBBY" and result != "offline":
        datas = "WhoDoesnt is currently in a " + result + ": " + time_pacific

    else:
        datas = "WhoDoesnt is currently " + result + ": " + time_pacific
    return datas


def read_time():
    with open("datas.json", "r") as myfile:
        time = myfile.readline()
        time = ((int(time) * 30) / 60) / 60
        final_time = round(time, 2)
        myfile.close()
        return final_time


def get_fish():
    with open("datas.json", "r") as myfile:
        timed = myfile.readline()
        timed = (int(timed) * 30)
        myfile.close()
    dataset = pd.read_csv('datacsv')
    X = dataset.iloc[:, :-2].values
    y = dataset.iloc[:, 1].values
    regressor = LinearRegression()
    regressor.fit(X, y)
    fish = regressor.predict(np.array([[timed]])) + 42527
    return round(int(fish), 0)


@client.event
async def on_ready():
    print("Bot is ready")
    send_message.start()


@client.event
async def on_command_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="**Error**", color=discord.Color.red())
        embed.add_field(name="Error Message: ", value="***Please pass in all required arguments!***")
        await ctx.send(embed=embed)

    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="**Error**", color=discord.Color.red())
        embed.add_field(name="**Error Message: **", value=f"***This command is on cooldown ~{error.retry_after:.2f}s***")
        await ctx.send(embed=embed)
    else:
        pass


@tasks.loop(seconds=30)
async def send_message():
    message = get_data()
    channel = client.get_channel(739333758058233857)
    await channel.send(message)
    await client.change_presence(activity=discord.Game(next(status)))


@client.command()
async def applebig(ctxs):
    fish = "N/A"#get_fish()
    await ctxs.send("It's Estimated that Isaac caught " + str(fish) + " fish")


@client.command()
async def applebih(ctx):
    time = "N/A" #oldtime + read_time()
    await ctx.send("It's Estimated that Isaac has been fishing for " + str(time) + "hrs Since the start of the summer fishing challenge")


@client.command()
async def ncs(sum):
    messagess = huang()
    await sum.send(messagess)


@client.command()
async def egg(summ):
    await summ.send("https://youtu.be/XDM-t9rZISU")


@client.command()
async def richard(ctx):
    await ctx.send("https://youtu.be/NJTH24--qC8")


@client.command()
async def explosion(ctx):
    await ctx.send("https://youtu.be/rWoW8KuHrqA")


@client.command()
async def lisa(ctx):
    await ctx.send("https://youtu.be/rwdoxptQyTg")


@client.command()
async def josh(ctx):
    await ctx.send("https://youtu.be/D23ylWDrcC8")


@client.command()
async def virus(ctx):
    await ctx.send("*This command is currently disabled*") #https://drive.google.com/file/d/1fGuNHqWBg402mJC7Ne2pDMfsXb6GfW9D/view?usp=sharing


@client.command()
async def wirus(ctx):
    await ctx.send("*This command is currently disabled*") #https://drive.google.com/file/d/1EzbbIztgv0gUkKp49AyEl-jEFiMAlWR0/view?usp=sharing


@client.command()
async def quote(ctx):
    channel = client.get_channel(745310944963592223)
    messages = await channel.history(limit=200).flatten()
    lst = []
    for message in messages:
        if '"' in message.content:
            message = message.content
            lst.append(message.replace("\n", ""))
    item_num = randrange(len(lst))
    await ctx.author.send(lst[item_num])
    await ctx.send(lst[item_num])


@client.command()
@commands.cooldown(1, 3600, commands.BucketType.default)
async def total(ctx):
    await ctx.channel.send("CALCULATING 200,000 MESSAGES... THIS MAKE TAKE A FEW MINUTES")
    channel = client.get_channel(739333758058233857)
    messages = await channel.history(limit=300000).flatten()
    message_num = 0
    total_time = 0
    for message in messages:
        message_num += 1
        message = message.content
        if "offline" not in message:
            print(message)
            total_time += 0.00833333333

    message_num *= 30
    message_num /= 86400
    await ctx.channel.send(f"Isaac has played about {round(total_time, 2)} hrs of Hypixel over {round(message_num, 2)} days of recording")


@client.command()
@commands.cooldown(1, 30, commands.BucketType.default)
async def search(ctx, arg):
    await ctx.channel.send("***Starting... ~5 minutes!***")
    await ctx.channel.send("***I will be offline during this search!***")
    await ctx.channel.send("***Searching...***")
    sherlock.main(user=arg.rstrip())
    file = discord.File("searches/" + arg.rstrip() + ".txt", filename=arg.rstrip() + ".txt")
    await ctx.channel.send(file=file)


@client.command()
async def help(ctx):
    embed = discord.Embed(title="***Available Commands***", color=discord.Color.blurple())
    embed.add_field(name="***Mitai - ***", value=".lisa, .richard, .egg, .explosion\n")
    embed.add_field(name="***Random - ***", value=".virus, .wirus, .ncs, .witt, .quote, .dtat\n")
    embed.add_field(name="***Isaac Status - ***", value=".applebih, .applebig (NOT CURRENTLY AVAILABLE), .time\n")
    embed.add_field(name="***Information - ***", value=".search (username) eg. .search apple\n")
    embed.add_field(name="***Minecraft - ***", value=".mcinfo (username) eg.\t .mcinfo whodoesnt, .mca (username) #Checks for Availability, .mcsnipe - bot ask @Xander5341 how to use it\n")
    embed.add_field(name="***TTS - ***", value='.tts ("text") eg. .tts **"**jam jam**"** \n')
    embed.add_field(name="***Voice - ***", value=' .bounce\n')
    embed.add_field(name="***Play - ***", value=' .play 1201\n')
    embed.add_field(name="***Story - ***", value=' .story\n')
    embed.add_field(name="***Giphs - ***", value=' **.giph** fricked, calm, joint, jamsheed\n')
    embed.add_field(name="***q - ***", value=' **.q** Ask Me About Pants or something!\n')
    embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/739287727580774420/ccbbc7fb0df971bb52b1643a173fd98b.png?size=256')
    await ctx.channel.send(embed=embed)


@commands.cooldown(1, 60, commands.BucketType.user)
@client.command()
async def mcinfo(ctx, arg):
    uuid = get_uuid(arg)

    if uuid is not None:
        name_data = mojang.MojangAPI.get_name_history(uuid)
        profile = mojang.MojangAPI.get_profile(uuid)
        string = ""
        for name in name_data:
            string += "*" + name["name"] + "*" + "\n"

        embed = discord.Embed(title=f"***{arg.title()}***", color=discord.Color.blurple())
        embed.add_field(name="**Previous Names**", value=string)
        embed.add_field(name="**UUID **", value=profile.id, inline=False)

        if profile.cape_url is not None:
            embed.add_field(name="**Cape **", value="Yes", inline=True)
        else:
            embed.add_field(name="**Cape **", value="*No Cape*", inline=False)

        if profile.skin_url is not None:
            embed.set_thumbnail(url=profile.skin_url)

        else:
            embed.set_thumbnail(url='https://media.minecraftforum.net/attachments/307/614/637097591757003256.jpg')

        optifine_cape = f"http://s.optifine.net/capes/{profile.name}.png"
        embed.add_field(name="**Optifine Cape **", value="*Cape:*")
        embed.set_image(url=optifine_cape)

        await ctx.channel.send(embed=embed)
        embed2 = discord.Embed(title="***Cape***", color=discord.Color.blurple())
        embed2.set_image(url=profile.cape_url)
        await ctx.channel.send(embed=embed2)
    else:
        embed = discord.Embed(title=f"***{arg.title()}***", color=discord.Color.red())
        embed.add_field(name="Not Available", value="***There is no Minecraft user with that name currently!***")
        await ctx.channel.send(embed=embed)


@commands.cooldown(1, 10, commands.BucketType.user)
@client.command()
async def mca(ctx, arg):

    if len(arg) > 16 or len(arg) < 3:
        embed = discord.Embed(title=f"***The Name {arg.title()} Is Not Available***", color=discord.Color.red())
        embed.add_field(name="Too Short/Long: ", value=f"***{arg.title()}***")

    else:
        try:
            availability = mojang.MojangAPI.get_drop_timestamp(arg)

            if availability is not None:
                unix_time = datetime.fromtimestamp(availability)
                unix_time = unix_time.astimezone(timezone('US/Pacific'))
                time_pacific = unix_time.strftime("%Y-%m-%d, %I:%M:%S %p")
                embed = discord.Embed(title=f"***The Name {arg.title()} Will Be Available***", color=discord.Color.blurple())
                embed.add_field(name=f'Available On:{time_pacific} PST', value=f"***{arg.title()}***")
            else:
                embed = discord.Embed(title=f"***The Name {arg.title()} Is Not Available***", color=discord.Color.red())
                embed.add_field(name="Not Available: ", value=f"***{arg.title()}***")
        except TypeError:
            embed = discord.Embed(title=f"***The Name {arg.title()} Is Available***", color=discord.Color.green())
            embed.add_field(name="Available: ", value=f"***{arg.title()}***")

    await ctx.channel.send(embed=embed)


@client.command()
async def witt(ctx):
    await ctx.channel.send("https://wigetwinner.wixsite.com/gameguider/blank-1")


@commands.cooldown(1, 20, commands.BucketType.default)
@client.command()
async def tts(ctx, args):
    if len(args) >= 5000:     # if args greater than 5000 (limit)
        print("rip")
    try:
        channels = ctx.message.author.voice.channel
        voice = get(client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channels)
        else:
            voice = await channels.connect()

        tts = gTTS(args)
        tts.save(f'tts/{args[0:10]}.mp3')
        voice.play(discord.FFmpegPCMAudio(source=f'tts/{args[0:10]}.mp3'))

    except AttributeError:  # returned if the user isn't in a voice channel
        await ctx.channel.send("***You must be in a voice channel!***")
        tts = gTTS(args)
        tts.save(f'tts/{args[0:10]}.mp3')
        file = discord.File(f"tts/{args[0:10]}.mp3", filename=f"{args[0:10]}.mp3")
        await ctx.channel.send(file=file)

    #else:
        #await ctx.channel.send("***Your message must be less than 200 characters!***")


@commands.cooldown(1, 60, commands.BucketType.default)
@client.command()
async def story(ctx):
    channel = client.get_channel(776663105551335465)
    messages = await channel.history(limit=40, oldest_first=True).flatten()
    story = ""
    for message in messages:
        message = message.content
        story += " " + message + " "
    await tts(ctx, story)


@client.command()
async def bounce(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.channel.send("*Bounced!*")
    else:
        await ctx.channel.send("*I'm not currently in a voice channel!*")


@commands.cooldown(1, 5, commands.BucketType.default)
@client.command()
async def time(ctx):
    playtime = json.load(open('time_played.json'))
    print(playtime)
    x, y = zip(*sorted(zip(playtime.keys(), playtime.values())))
    plt.bar(x, y)
    plt.title(f"Whodoesnt's Hypixel Time Since {start_time_pacific}")
    plt.ylabel('Hours')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('bar_graph.png')
    file = discord.File("bar_graph.png", filename="bar_graph.png")
    await ctx.channel.send(file=file)


@commands.cooldown(1, 20, commands.BucketType.default)
@client.command()
async def play(ctx, args):
    try:
        channels = ctx.message.author.voice.channel
        voice = get(client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channels)
        else:
            voice = await channels.connect()

        voice.play(discord.FFmpegPCMAudio(f'sounds/{args}.mp3'))

    except AttributeError:  # returned if the user isn't in a voice channel
        await ctx.channel.send("***You must be in a voice channel!***")


@client.command()
async def giph(ctx, arg):
    arg = arg.lower()
    if arg == 'joint':
        await ctx.send("https://tenor.com/view/weed-the-virtual-joint-gif-12178837")
    elif arg == 'fricked':
        await ctx.send("https://media.giphy.com/media/h7R6RtIxvXUQLjknyu/giphy.gif")
    elif arg == 'calm':
        await ctx.send("https://tenor.com/view/calmyotits-calm-down-calm-relax-terry-crews-gif-4655399")
    elif arg == 'jamsheed':
        await ctx.send('https://tenor.com/view/jamsheed-rocket-launcher-military-soldier-rpg-god-gif-17812798')
    else:
        giphs = "joint, fricked, calm"
        embed = discord.Embed(title=f"***Giph Not Found***", color=discord.Color.red())
        embed.add_field(name="Not Found: ", value=f"***{arg.title()}***")
        embed.add_field(name="Available Giphs: ", value=f"***{giphs}***")
        await ctx.send(embed=embed)


@client.command()
async def mcsnipe(ctx):
    await ctx.send('https://drive.google.com/file/d/1Aq1bgoPL38dCFqPdOWCHNXdIVHo1T7Nn/view?usp=sharing')
    await ctx.send('Added:\nSupersnipe aka tries to snipe name very accurately\n bug fixes\n timing improvements\nresponse file for errors\nother fixes/optimizations')


@client.command()
async def q(ctx, arg):
    embed = discord.Embed(title=f"***Happy Egg Says:***", color=discord.Color.orange())
    message = chat.chat.run(arg)
    underline = ""
    for char in message:
        underline += "¯"
    embed.add_field(name=f"***{message}***", value=underline)
    await ctx.send(embed=embed)


@client.event
async def on_message(ctx):
    if ctx.author.id != 739287727580774420:
        bad_words = ["minecraft", "videogames", "politic", 'balls', 'skywars', 'cringe', 'glizzy', 'baiis']
        strips = [' ', '_', '*', '.', ':', "'", '"', '`']
        content = ctx.content.lower()

        for strip in strips:
            content = content.replace(strip, '')

        for word in bad_words:
            if word in content:
                embed = discord.Embed(title=f"***Illegal Word Detected***", color=discord.Color.red())
                embed.add_field(name=f"{ctx.author} Sent: ", value=f"{word}")
                try:
                    await ctx.channel.purge(limit=1)
                except:
                    pass
                await ctx.channel.send(embed=embed)

    await client.process_commands(ctx)


@commands.cooldown(1, 2, commands.BucketType.default)
@client.command()
async def dtat(ctx):
    await ctx.channel.purge(limit=3)
    embed = discord.Embed(title=f"***Dtat***", color=discord.Color.dark_orange())
    embed.add_field(name="Dtat!", value=f"**Dtat!**")
    await ctx.channel.send(embed=embed)


client.run(os.environ["DISCORD_TOKEN"])

