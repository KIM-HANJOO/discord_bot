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
watchdir = os.path.join(main_dir, 'log')

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
    df = pd.DataFrame()

    if ctx == '' :
        return

    os.chdir(watchdir)

    oldtm = 0
    watch = 1
    old_files = os.listdir(watchdir)
       
    # add files & mtimes to df
    if len(old_files) != 0 :
        for ofile in old_files :
            if ('.swp' not in ofile) & ('.swo' not in ofile) :
                df[f'{ofile}'] = [os.path.getmtime(ofile)]

    # watch changes
    while watch == 1 :
        print('\nwatching ...\n')
        # delete deleted files
        for ofile in df.columns :
            if ofile not in os.listdir(watchdir) :
                df.drop([ofile], axis = 1, inplace = True)

        
        # if file is added
        if os.listdir(watchdir) != [] :
            st_files = [x for x in os.listdir(watchdir) if x not in df.columns]
            for item in st_files :
                if ('.swp' in item) | ('.swo' in item) :
                    st_files.remove(item)

            if st_files != [] :
                await ctx.send('new file(s) added\n')
                
                for tmpfile in st_files :
                    path_file = os.path.join(watchdir, tmpfile)
                    await ctx.send(f'{tmpfile}')
                    await ctx.send(file = discord.File(path_file))

                    df[tmpfile] = [os.path.getmtime(tmpfile)]
        
        # if change in getmtime
        for tmpfile in df.columns :
            try :
                newtm = os.path.getmtime(tmpfile)
                if df.loc[0, tmpfile] != newtm : #if file is changed
                    print(f'{tmpfile} changed\n')
                    path_file = os.path.join(watchdir, tmpfile)
                    await ctx.send(f'{tmpfile} changed')
                    await ctx.send(file = discord.File(path_file))

                    df.loc[0, tmpfile] = newtm
            except FileNotFoundError :
                print('file not found')
                await ctx.send(f'{tmpfile} raised FileNotFoundError\n')
        print(df)
                    
        await asyncio.sleep(4)




#                # if file is changed
#                for tmpfile in os.listdir(watchdir) : 
#                    try :
#                        print(f'{tmpfile} checking')
#                        os.chdir(watchdir)
#                        newtm = os.path.getmtime(tmpfile)
#                        print(newtm)
#
#                        if oldtm != newtm :
#                            if oldtm != 0 : # {tempfile} changed
#                                print(f'{tmpfile} changed')
#                                path_file = os.path.join(watchdir, tmpfile)
#                                await ctx.send('changed')
#                                await ctx.send(file = discord.File(path_file))
##                            for guilds in bot.guilds :
##                                for ch in guilds.channel :
##                                    await ch.send('changed')
##                                    await ch.send(file = discord.File(path_file))
#                                oldtm = newtm
#                            if oldtm == 0 :
#                                oldtm = newtm
#                        else :
#                            print(f'{tmpfile} not changed')
#                            pass
#                    except FileNotFoundError :
#                        print('file not found')
#                        pass
#                
#            print(f'oldtm = {oldtm}, newtm = {newtm}')
#            print('\n\n')
#            old_files = os.listdir(watchdir)
#            await asyncio.sleep(4)



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
