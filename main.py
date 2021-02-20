import requests
import time
import json
import base64
import discord
import random
from discord.ext import commands


f = open('premium.txt','r')
premiums = f.read().splitlines()
f.close()


def last_used(user_id):
    f = open('log.txt','r')
    text = f.read().splitlines()
    f.close()
    
    d = {}
    for line in text:
        if ':' in line:
            d[line[0:line.find(':')]] = line[line.find(':')+1:len(line)]

    if str(user_id) in d:
        return d[str(user_id)]
    else:
        return 0

def update_dict(user_id):
    f = open('log.txt','r')
    text = f.read().splitlines()
    d = {}
    for line in text:
        if ':' in line:
            d[line[0:line.find(':')]] = line[line.find(':')+1:len(line)]
    d[str(user_id)] = str(int(time.time()))

    new_text_file = ''
    keys = d.keys()
    for key in keys:
        new_text_file = new_text_file + str(key) + ':' + str(d[key]) + '\n'
    new_text_file = new_text_file[0:len(new_text_file) -1]
    
    f.close()
    f = open('log.txt','w')
    f.write(new_text_file)
    f.close()


def bypass_link(url):
    first_link = 'https://publisher.linkvertise.com/api/v1/redirect/link/static/'

    second_link = 'https://publisher.linkvertise.com/api/v1/redirect/link/insert/linkvertise/path/here/target?serial=base64encodedjson'
    second_link_front = second_link[0:second_link.find('insert/linkvertise')]
    second_link_back = second_link[second_link.find('/target?serial'):second_link.find('base64encodedjson')]


    input_link = url
    link = ''
    if '.com/' in input_link:
        if '?o=' in input_link:
            link = input_link[input_link.find('.com/')+5:input_link.find('?o=')]
        else:
            link = input_link[input_link.find('.com/')+5:len(input_link)]
    if '.net/' in input_link:
        if '?o=' in input_link:
            link = input_link[input_link.find('.net/')+5:input_link.find('?o=')]
        else:
            link = input_link[input_link.find('.net/')+5:len(input_link)]

    r = requests.get(first_link + link)
    text = r.text
    link_id = text[text.find('"id":')+5:text.find(',"url":')]


    new_json = {"timestamp":int(time.time()), "random":"6548307", "link_id":int(link_id)}

    s = json.dumps(new_json)
    json_converted = base64.b64encode(s.encode('utf-8'))
    json_converted = str(json_converted)
    json_converted = json_converted[2:len(json_converted)-1]


    r = requests.get(second_link_front + link + second_link_back + json_converted)
    converted_json = json.loads(r.text)
    new_link = converted_json['data']['target']
    
    return new_link

# invite https://discord.com/api/oauth2/authorize?client_id=811339635950485546&permissions=8&scope=bot

client = commands.Bot(command_prefix = '.', help_command = None)

@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.online, activity = discord.Activity(type=discord.ActivityType.watching, name=".help"))
    print('Bot is online.')


@client.command()
async def bypass(ctx, url):
    user_id = ctx.message.author.id
    mention = ctx.message.author.mention

    limit = 15 #seconds

    embed = discord.Embed(
        title = 'Linkvertise Bypasser',
        color = discord.Color.green(),
        description = mention+"'s shortlink"
    )
    embed.set_footer(text='Bypassed by GlassTea')


    if str(user_id) in premiums:
        embed.add_field(name='Old Link', value = url, inline=False)
        embed.add_field(name='New link', value = bypass_link(url), inline=False)

        await ctx.send(embed=embed)
        #await ctx.send(mention + '\n\nOld link: ' + url + '\nNew link: ' + bypass_link(url))
    if str(user_id) not in premiums:
        if last_used(user_id) == 0 or int(int(time.time()) - int(last_used(user_id))) >= limit:
            update_dict(user_id)

            embed.add_field(name='Old Link', value = url, inline=False)
            embed.add_field(name='New link', value = bypass_link(url), inline=False)

            await ctx.send(embed=embed)
            
        else:
            embed.add_field(name='ERROR', value = 'You next avaliable bypass is in ' + str( limit - (int(time.time()) - int(last_used(user_id))) ) + ' seconds', inline=False)

            await ctx.send(embed=embed)

@client.command()
async def ping(ctx):

    

    await ctx.send(str(int(client.latency*1000)) + ' ms')

@client.command()
async def invite(ctx):
    embed = discord.Embed(
        title = 'Invite Bot',
        color = discord.Color.green(),
        description = 'Click the link below to invite this bot to YOUR own server:\nhttps://discord.com/api/oauth2/authorize?client_id=811339635950485546&permissions=8&scope=bot'
    )

    await ctx.send(embed = embed)

@client.command()
async def flipcoin(ctx):
    options = ['heads','tails']
    option = random.choice(options)

    embed = discord.Embed(
        title = 'Flip coin',
        color = discord.Color.green(),
        description = option
    )

    await ctx.send(embed = embed)

@client.command()
async def rock(ctx):
    options = ['scissors','paper','rock']
    option = random.choice(options)

    embed = None

    if option == 'scissors':
        embed = discord.Embed(
            title = 'Rock, Paper, Scissors',
            color = discord.Color.green(),
            description = 'I chose `Scissors` You Won!'
        )
    
    if option == 'paper':
        embed = discord.Embed(
            title = 'Rock, Paper, Scissors',
            color = discord.Color.red(),
            description = 'I chose `Paper` You Lost!'
        )
    
    if option == 'rock':
        embed = discord.Embed(
            title = 'Rock, Paper, Scissors',
            color = discord.Color.blue(),
            description = 'I chose `Rock` You Tied!'
        )

    await ctx.send(embed = embed)

@client.command()
async def paper(ctx):
    options = ['scissors','paper','rock']
    option = random.choice(options)

    embed = None

    if option == 'rock':
        embed = discord.Embed(
            title = 'Rock, Paper, Scissors',
            color = discord.Color.green(),
            description = 'I chose `Rock` You Won!'
        )
    
    if option == 'paper':
        embed = discord.Embed(
            title = 'Rock, Paper, Scissors',
            color = discord.Color.blue(),
            description = 'I chose `Paper` You Tied!'
        )
    
    if option == 'scissors':
        embed = discord.Embed(
            title = 'Rock, Paper, Scissors',
            color = discord.Color.red(),
            description = 'I chose `Scissors` You Lost!'
        )
    
    await ctx.send(embed = embed)

@client.command()
async def scissors(ctx):
    options = ['scissors','paper','rock']
    option = random.choice(options)

    embed = None

    if option == 'rock':
        embed = discord.Embed(
            title = 'Rock, Paper, Scissors',
            color = discord.Color.red(),
            description = 'I chose `Rock` You Lost!'
        )
    
    if option == 'paper':
        embed = discord.Embed(
            title = 'Rock, Paper, Scissors',
            color = discord.Color.green(),
            description = 'I chose `Paper` You Won!'
        )
    
    if option == 'scissors':
        embed = discord.Embed(
            title = 'Rock, Paper, Scissors',
            color = discord.Color.blue(),
            description = 'I chose `Scissors` You Tied!'
        )
    
    await ctx.send(embed = embed)


@client.command()
async def help(ctx):
    embed = discord.Embed(
        color = discord.Color.blue(),
        description = 'Command Parameters: <required> {optional}\nOfficial Discord Help Server: https://discord.gg/8uterAf'
    )
    
    embed.add_field(
        name = '.help', 
        value = 'Displays Help', 
        inline = False
    )

    embed.add_field(
        name = '.bypass <link>', 
        value = "Get what's behind the shortlink", 
        inline = False
    )

    embed.add_field(
        name = '.invite', 
        value = 'Gives the invite link for the bot', 
        inline = False
    )

    embed.add_field(
        name = '.ping', 
        value = 'Gives ping', 
        inline = False
    )

    embed.add_field(
        name = '.flipcoin', 
        value = 'Flips a coin', 
        inline = False
    )

    embed.add_field(
        name = '.rock', 
        value = 'Plays rock paper scissors', 
        inline = False
    )

    embed.add_field(
        name = '.paper', 
        value = 'Plays rock paper scissors', 
        inline = False
    )

    embed.add_field(
        name = '.scissors', 
        value = 'Plays rock paper scissors', 
        inline = False
    )
    

    await ctx.send(embed = embed)


client.run(TOKEN)