from discord.flags import Intents
import httpx, requests, discord, threading, socks, random, json, tracemalloc, asyncio
from discord.utils import get;
from dotenv import load_dotenv
from discord.ext import commands 



def get_config():
    config_file = open("config.json","r", encoding="utf8")
    configx = config_file.read()
    config_file.close()
    return configx

def get_prefix():
    config_file = get_config()
    config = json.loads(config_file)
    prefix = config['bot_config']["prefix"] 
    return prefix

config_file = get_config()
config = json.loads(config_file)
prefix = config['bot_config']["prefix"]
token = config['bot_config']["token"]

queue = []

load_dotenv()
intents = discord.Intents().all()
bot = commands.AutoShardedBot(command_prefix=get_prefix(), help_command=None, intents=intents)

def init():
    loop = asyncio.get_event_loop()
    loop.create_task(bot.run(token))
    threading.Thread(target=loop.run_forever).start()

@bot.command()
async def help(ctx):
    print("x")
    await bot.change_presence(activity=discord.Streaming(name="on Twitch", url="https://www.twitch.tv/idcblur"))
    config_file = get_config()
    json_object = json.loads(config_file)
    prefix = json_object['bot_config']["prefix"]
    print(f'{ctx.author} | {ctx.author.id} -> {prefix}help')
    if ctx.channel.type != discord.ChannelType.private:
            embed = discord.Embed(color=16776960)
            embed.set_thumbnail(url='')
            embed.add_field(name='Help', value=f'`{prefix}help`', inline=True)
            embed.add_field(name='Twitch Followers', value=f'`{prefix}tfollow (channel)`', inline=False)
            await ctx.send(embed=embed)

def get_id(user):

    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'Accept-Language': 'en-US',
        'sec-ch-ua-mobile': '?0',
        'Client-Version': '7b9843d8-1916-4c86-aeb3-7850e2896464',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'Content-Type': 'text/plain;charset=UTF-8',
        'Client-Session-Id': '51789c1a5bf92c65',
        'Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko',
        'X-Device-Id': 'xH9DusxeZ5JEV7wvmL8ODHLkDcg08Hgr',
        'sec-ch-ua-platform': '"Windows"',
        'Accept': '*/*',
        'Origin': 'https://www.twitch.tv',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.twitch.tv/',
    }
    data = '[{"operationName": "WatchTrackQuery","variables": {"channelLogin": "'+user+'","videoID": null,"hasVideoID": false},"extensions": {"persistedQuery": {"version": 1,"sha256Hash": "38bbbbd9ae2e0150f335e208b05cf09978e542b464a78c2d4952673cd02ea42b"}}}]'
    try:
        response = httpx.post('https://gql.twitch.tv/gql', headers=headers, data=data)
        id = response.json()[0]['data']['user']['id']
        return id
    except:
        return None

@bot.command()
async def tfollow(ctx, arg):
 if ctx.channel.type != discord.ChannelType.private:
    config_file = get_config()
    json_object = json.loads(config_file)
    print(f'{ctx.author} | {ctx.author.id} -> {prefix}tfollow')
    genchannel =json_object['bot_config']["twitch_channel"]
    genchannel2 =json_object['bot_config']["twitch_channel_2"]
    if ctx.channel.id == int(genchannel) or ctx.channel.id == int(genchannel2):
        role_config = json.loads(config_file)['tfollow']
        for role_name in role_config:
            filefile = open("config.json","r", encoding="utf8")
            follow_count = json.loads(filefile.read())['tfollow'][role_name]
            filefile.close()
            role_id = discord.utils.get(ctx.guild.roles, name=role_name)
            if role_id in ctx.author.roles:
                
                target_id = get_id(arg)
                if target_id == None:
                    embed=discord.Embed(color=3447003, description=f"**ERROR** Invalid **username** {arg}")
                    await ctx.send(embed=embed, delete_after=5)
                    break
                else:
                    None
                
                filefile = open('ttoken_follow.txt')
                num_lines = sum(1 for line in filefile)
                filefile.close()
                
                filefile = open('ttoken_follow.txt', 'r')
                tokens = filefile.read().splitlines()
                filefile.close()
                
                if num_lines < follow_count:
                    
                    embed=discord.Embed(color=16776960, description=f" Adding **{num_lines}** follows to **{arg}**")
                    await ctx.send(embed=embed)
                    
                    caunt_to_follow = num_lines
                else:
                    
                    embed=discord.Embed(color=16776960, description=f" Adding **{follow_count}** Twitch Follows to **{arg}**")
                    await ctx.send(embed=embed)
                
                    caunt_to_follow = follow_count

                    
                class Follow():
                    sent = 0
                        
                def start_follow():

                        
                    for i in range(caunt_to_follow):
                        
                        try:
                            ttoken = random.choice(open("ttoken_follow.txt", "r" ).read().splitlines())
                            
                            payload = '[{\"operationName\":\"FollowButton_FollowUser\",\"variables\":{\"input\":{\"disableNotifications\":false,\"targetID\":\"'+target_id+'\"}},\"extensions\":{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"51956f0c469f54e60211ea4e6a34b597d45c1c37b9664d4b62096a1ac03be9e6\"}}}]'
                            headers = {
                                            "Authorization": f"OAuth {ttoken}",
                                            "Client-Id": 'kimne78kx3ncx6brgo4mv6wki5h1ko',
                                            "Content-Type": "application/json"
                                        }
                            
                            response = httpx.post('https://gql.twitch.tv/gql', data=payload, headers=headers)
                        
                            
                            try:
                                if response.json()[0]['data']['followUser']['error']:
                                    with open("ttoken_follow.txt", "r") as f:
                                        lines = f.readlines()
                                    with open("ttoken_follow.txt", "w") as f:
                                        for line in lines:
                                            if line.strip("\n") != ttoken:
                                                f.write(line)
                                                f.close()
                            except:
                                None
                            try:
                                
                                if response.json()[0]['error'] == "Unauthorized":
                                    with open("ttoken_follow.txt", "r") as f:
                                        lines = f.readlines()
                                        f.close()
                                    with open("ttoken_follow.txt", "w") as f:
                                        for line in lines:
                                            if line.strip("\n") != ttoken:
                                                f.write(line)
                                                f.close()
                            except:
                                None
                            try:
                                
                                if response.json()[0]['data']['followUser']['follow'] == None:
                                        None
                            except:
                                None
                            try:
                                if response.json()[0]['data']['followUser']['follow']['user']:
                                    Follow.sent = Follow.sent + 1
                            except:
                                None   
                        except:
                            None
                x = threading.Thread(target=start_follow)
                x.start()
                break

bot.run(token)