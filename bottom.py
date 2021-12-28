import discord
from discord.ext import commands

import asyncio
import nest_asyncio
import os
import time
from PIL import Image

main_dir = os.getcwd()
module_dir = os.path.join(main_dir, 'module')
token_dir = os.path.join(module_dir, 'token')
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
def size_down_png(file_path) :
    if os.path.getsize(file_path) > 8 * pow(1024, 2):
        img = Image.open(file_path)
        width, height = img.size

        ratio = 8 * pow(1024, 2) / os.path.getsize(file_path)
        img = img.resize((width * ratio * 0.8, height * ratio * 0.8))
        img.save(file_path)

def time_keeper(gap) :
    set_time = 10 * 60 # watchdog sleeptime = 1 if gap < 10min
    
    if gap < set_time :
        stime = 1

    else :
        stime = 10

    return stime

@bot.command()
async def watchdog(ctx) :
    f_dict = dict()

    if ctx == '' :
        return

    os.chdir(watchdir)

    oldtm = 0
    watch = 1
    old_files = os.listdir(watchdir)
       
    # add files & mtimes to dictionary
    if len(old_files) != 0 :
        for ofile in old_files :
            if ('.swp' not in ofile) & ('.swo' not in ofile) :
                f_dict[ofile] =  os.path.getmtime(ofile)

    # watch changes
    gap_start = time.time()

    while watch == 1 :
        print('\nwatching ...\n')
        # delete deleted files
        for ofile in list(f_dict.keys()) :
            if ofile not in os.listdir(watchdir) :
                del f_dict[ofile]

        
        # if file is added
        if os.listdir(watchdir) != [] :
            st_files = [x for x in os.listdir(watchdir) if x not in list(f_dict.keys())]
            for item in st_files :
                if ('.swp' in item) | ('.swo' in item) :
                    st_files.remove(item)

            if st_files != [] :
                await ctx.send('new file(s) added\n')
                
                for tmpfile in st_files :
                    path_file = os.path.join(watchdir, tmpfile)
                    size_down_png(path_file)
                    await ctx.send(f'{tmpfile}')
                    await ctx.send(file = discord.File(path_file))

                    f_dict[tmpfile] = os.path.getmtime(tmpfile)
                    gap_start = time.time()
        
        # if change in getmtime
        for tmpfile in list(f_dict.keys()) :
            try :
                newtm = os.path.getmtime(tmpfile)
                if f_dict[tmpfile] != newtm : #if file is changed
                    print(f'{tmpfile} changed\n')
                    path_file = os.path.join(watchdir, tmpfile)
                    size_down_png(path_file)
                    await ctx.send(f'{tmpfile} changed')
                    await ctx.send(file = discord.File(path_file))

                    f_dict[tmpfile] = newtm
                    gap_start = time.time()
            except FileNotFoundError :
                print('file not found')
                await ctx.send(f'{tmpfile} raised FileNotFoundError\n')
        print(f_dict)

        gap_end = time.time()            
        stime = time_keeper(gap_end - gap_start)

        print(f'resting for {round(gap_end - gap_start)}sec, sleeptime = {stime}')
        await asyncio.sleep(int(round(stime)))



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
