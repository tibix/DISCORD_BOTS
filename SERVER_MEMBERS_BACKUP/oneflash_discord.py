import discord, time, datetime
from discord.ext import commands
from discord.ext.commands import Bot
from yt_data import get_top_10_videos, get_video_title, get_last_10_videos, get_top_10_channel_comments

intents = discord.Intents.all()
intents.presences = True 
intents.members = True

BOT_PREFIX = ("!")
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

TOKEN = 'OTM1ODMzMjc1MDY1MzI3NjQ2.G_Xsn8.RS3DhnOSx0Ou-0J6XkX8UslxDaEC-_phQL5-pw'

# log to the console when bot is logged in
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# !prune command
@bot.command()
async def prune(ctx):
    embed=discord.Embed(title="Hai la prune!", description='Bravo <@678298480493461529>! Alte idei crete mai ai?', color=discord.Color.dark_red())
    await ctx.send(embed=embed)

# !members_backup command
@bot.command()
async def members_backup(ctx):
    server_members = ctx.guild.members
    with open('members.txt', 'r') as fr:
        existing_data = fr.read().splitlines()

    with open('members.txt', 'a') as fa:
        counter = 0
        for member in server_members:
            member_info = member.name + "#" + member.discriminator + " cu ID: " + str(member.id) + " si cu rol(uri): " + ",".join([str(role) for role in member.roles])
            if member_info in existing_data:
                continue
            else:
                fa.write(member_info)
                fa.write('\n')
                counter += 1
    embed = discord.Embed(title = 'Back-up Membrii', description=f"Am salvat datele a {counter} membrii fata de ultima salvare!\n" ,color = discord.Color.teal())
    await ctx.send(embed=embed)
 
# !members_info command
@bot.command()
async def members_info(ctx):
    online = 0
    offline = 0
    server_members = ctx.guild.members
    for member in server_members:
        if member.status.name == "online":
            online += 1
        if member.status.name == "offline":
            offline += 1
    
    embed = discord.Embed(
        title = 'Members Info',
        description = f"Mai suntem:\n\t - {online} b8ers activi 💪\n \t - \
            {offline} b8ers in repaus 😫 \n\t - \
            {len(server_members)-online-offline} b8ers pe in alte ipostaze indecente 🍑 \
            \n\nIn total {len(server_members)} de b8eri!",
        color = discord.Color.purple()
        )
    await ctx.send(embed=embed)

# !c_top_comments command
@bot.command()
async def c_top_comments(ctx):
    comments = get_top_10_channel_comments()
    for c in comments:
        message = message + c
    embed = discord.Embed(
        title = 'Top 10 comentarii ale canalului OneFlash',
        description = f"{message}",
        color = discord.Color.blurple()
    )
    await ctx.send(embed=embed)

# !top_10_videos command
@bot.command()
async def top_10_videos(ctx):
    videos = get_top_10_videos()
    video_description = ""
    for v in videos:
        video_description += f"**Video ID**: {v}\n **Titlu**: {get_video_title(v)}\n\n"
    embed = discord.Embed(
        title = 'Top 🔟 Clipuri produse de @OneFlash',
        description = f"{video_description}",
        color = discord.Color.dark_gold()
    )
    await ctx.send(embed=embed)

# !last_10_videos command
@bot.command()
async def last_10_videos(ctx):
    videos = get_last_10_videos()
    video_description = ""
    for v in videos:
        video_description += f"**Video ID**: {v}\n **Titlu**: {get_video_title(v)}\n\n"
    embed = discord.Embed(
        title = 'Ultimele 🔟 Clipuri produse de @OneFlash',
        description = f"{video_description}",
        color = discord.Color.dark_magenta()
    )
    await ctx.send(embed=embed)

# Event handler on_command_error
@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"Aceasta comanda nu exista!\n{error} \nComenzi disponibile: \n\t - !prune\n\t - !members_backup\n\t - !members_info\n\t - !top_10_videos\n\t - !top_comments\n\t - !last_10_videos")


if __name__ == "__main__":
    bot.run(TOKEN)
