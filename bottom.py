import discord
from discord.ext import commands

import asyncio
import nest_asyncio
import os
import time
import pandas as pd

main_dir = os.getcwd()
module_dir = os.path.join(main_dir, 'module')
token_dir = main_dir

import sys
sys.path.append(module_dir)
sys.path.append(token_dir)


# read token
os.chdir(token_dir)
tk_f = open('token.txt', 'r')
to = tk_f.readline()
tk_f.close()

# read server id
os.chdir(main_dir + '//module//token')
sv_f = open('server.txt', 'r')
sv = sv_f.readline()
sv_f.close()

# read channel id
ch_f = open('channel.txt', 'r')
channel = ch_f.readline()
ch_f.close()


# prefix $
bot=commands.Bot(command_prefix='$')
print('BOT_TOM awaking')


ch = bot.get_channel(channel)
print(ch)

@bot.event
async def on_ready() :
    print("Tommy is ready !")

    await bot.change_presence(status = discord.Status.online, activity = None)
    #await watchdog()

# channel_list
#text_channel_list = []
#for server in Client.servers :
#    for channel in server.channels :
#        if channel.type == 'Text' :
#            text_channel_list.append(channel)
#ch = text_channel_list[0]

# watchdog
@bot.command()
async def watchdog(ctx) :
    df = pd.DataFrame(columns = 
    if ctx != '' :
        print(f'channel id : {ch}')
        watchdir = os.path.join(main_dir, 'tmp')
        oldtm = 0
        watch = 1
        old_files = os.listdir(watchdir)
        while watch == 1 :

            if os.listdir(watchdir) != [] :
                print(os.listdir(watchdir))
                new_files = os.listdir(watchdir)

                # if new file is added
                if old_files != new_files : 
                    st_files = [x for x in new_files if x not in old_files]
                    if len(st_files) != 0 :
                        await ch.send('new files')
                        for tmpfile in st_files :
                            path_file = os.path.join(watchdir, tmpfile)
                            await ctx.send(file = discord.File(path_file))

                # if file is changed
                for tmpfile in os.listdir(watchdir) : 
                    try :
                        print(f'{tmpfile} checking')
                        os.chdir(watchdir)
                        newtm = os.path.getmtime(tmpfile)
                        print(newtm)

                        if oldtm != newtm :
                            if oldtm != 0 : # {tempfile} changed
                                print(f'{tmpfile} changed')
                                path_file = os.path.join(watchdir, tmpfile)
                                await ctx.send('changed')
                                await ctx.send(file = discord.File(path_file))
#                            for guilds in bot.guilds :
#                                for ch in guilds.channel :
#                                    await ch.send('changed')
#                                    await ch.send(file = discord.File(path_file))
                                oldtm = newtm
                            if oldtm == 0 :
                                oldtm = newtm
                        else :
                            print(f'{tmpfile} not changed')
                            pass
                    except FileNotFoundError :
                        print('file not found')
                        pass
                
            print(f'oldtm = {oldtm}, newtm = {newtm}')
            print('\n\n')
            old_files = os.listdir(watchdir)
            await asyncio.sleep(4)



@bot.command(aliases=['hi'])
async def 안녕(ctx):
    print(ctx.channel)
    a = globals(ctx)
    await ctx.send(f'안녕하세요, {ctx.channel}')

@bot.command()    
async def 따라하기(ctx,*,text):
    await ctx.send(text)

@bot.command()
async def weather(ctx, arg) :
    if arg == 'today' :
        string = 'jonna cold'
    await ctx.channel.send(string)


bot.run(to)
