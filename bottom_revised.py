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
workflow_dir = os.path.join(main_dir, 'workflow')
message_dir = os.path.join(main_dir, 'message')

import sys
sys.path.append(module_dir)
sys.path.append(token_dir)
import table
import pandas as pd



# ----------------------------------------------------------------
# start Bottom
# ----------------------------------------------------------------

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

# ----------------------------------------------------------------
# set all
# ----------------------------------------------------------------

@bot.command()
async def set_all(ctx) :
    await send_messages(ctx)
    await watchdog(ctx)

# ----------------------------------------------------------------
# message
# ----------------------------------------------------------------

def time_keeper_msg(gap) :
    set_time = 10 * 60 # watchdog sleeptime = 1 if gap < 10min
    
    if gap < set_time :
        stime = 3

    else :
        stime = 10

    return stime


@bot.command()
async def send_messages(ctx) :
    await ctx.send('starting endgame ...')
    os.chdir(message_dir)
    global gap_now_msg
    global stime_msg

    fs = open('work_done.txt', 'w')
    fs.write('0')
    fs.close()
    gap_start = time.time()
 
    while True :
        try : 
            f = open('work_done.txt', 'r')
            done_check = f.readline()
            done_check = int(done_check)
            f.close()
        except FileNotFoundError :
            await ctx.send('FileNotFoundError : loop canceled')
            await ctx.send(os.listdir(message_dir))
            break

        if done_check == 1 :
            gap_start = time.time()
            await ctx.send('work done !')
        else :
            pass


        gap_end = time.time()
        gap_now_msg = gap_end - gap_start
        stime_msg = time_keeper_msg(gap_now_msg)
        
        print(f'<send msg>\nresting for {round(gap_now_msg)}sec, sleeptime = {stime_msg}\n')
        await asyncio.sleep(int(round(stime_msg)))


# ----------------------------------------------------------------
# watchdog
# ----------------------------------------------------------------

def size_down_png(path_file) :
    if os.path.getsize(path_file) > 8 * pow(1024, 2):
        file_size = os.path.getsize(path_file)
        img = Image.open(path_file)
        width, height = img.size
        img.close()
        try : 
            ratio = 8 * pow(1024, 2) / file_size
            img = img.resize((width * ratio * 0.8, height * ratio * 0.8))
            img.save(path_file)
        except FileNotFoundError :
            if os.path.isfile(path_file) :
                os.remove(path_file)
            else :
                path_file = f'{path_file[ : -4]}.txt'
                f = open(f'{path_file[ : -4]}.txt', 'w')
                f.write(f'FileNotFounError for : {path_file}')
                f.close()
            
    return path_file

def time_keeper(gap) :
    set_time = 10 * 60 # watchdog sleeptime = 1 if gap < 10min
    
    if gap < set_time :
        stime = 1

    else :
        stime = 10

    return stime

def stable(df, title) : # make string as Table from table.py
    temp = table.Table(df, title)
    temp = temp.make()
    return temp


def is_target_file(file_name) :
    target_list = ['*.xlsx', '*.png', '*.docx', '*.pptx', '*.jpg', '*.jpeg']
    for item in target_list :
        if item[-1] == '*' :
            if item[0] == '*' :
                # *smth* -> smth in string
                if item[1 : -1] in file_name :
                    check = True
                    break
                else :
                    check = False

            # smth* -> start string == smth
            else :
                if file_name[len(item) - 1] == item[ : -1] :
                    check = True
                    break
                else :
                    check = False
        # *smth
        else :
            if file_name[-(len(item) - 1) : ] == item[1 : ] :
                check = True
                break
            else :
                check = False

    return check

@bot.command()

async def watchdog(ctx) :
    if ctx == '' :
        return

    # print info file
    f = open(os.path.join(watchdir, 'watchdog_show.txt'), 'w')
    f.write("sleeptime of watchdog is :\n\t1sec before 10 min from last request\n\t10sec after 10min from last request\n\ndon't send file with name :\n\t'watchdog_show.txt'\n\t'watchdog_info.txt'")
    f.close()

    await ctx.send(file = discord.File(os.path.join(watchdir, 'watchdog_show.txt')))

    # make watchlist (is_target_file())
    watchlist = []
    for item in os.listdir(watchdir) :
        if is_target_file(item) :
            watchlist.append(item)


    # f_dict will make a dictionary which
    # have every item(file) in watchlist as keys
    # item's last used time as values
    global f_dict
    f_dict = dict()
    os.chdir(watchdir)

       
    # add files & mtimes to dictionary
    if len(watchlist) != 0 :
        for file_name in watchlist :
            os.chdir(watchdir)
            f_dict[file_name] = os.path.gettime(file_name)

    # watch changes
    gap_start = time.time()

    # -------------------
    # watchdog
    # -------------------

    except_files = []

    # semi-update
    # if file in watchlist not in folder : delete file from watchlist
    watch = 1
    while watch == 1 :
        for file_name in watchlist :
            if file_name not in os.listdir(watchdir) :
                del f_dict[file_name]

    # check if
    # : file is added
    # : file is used

        # if file is added
        if os.listdir(watchdir) != [] :
            # new_files : newly added, not in f_dict keys
            new_files = [x for x in os.listdir(watchdir) if x not in list(f_dict.keys())]

            # delete 
            for item in new_files :
                if not is_target_file(item) :
                    new_files.remove(item)

            if new_files != [] :
                await ctx.send('new file(s) added\n')
                
                for tmpfile in new_files :
                    path_file = os.path.join(watchdir, tmpfile)
                    if os.path.getsize(path_file) / pow(1024, 2) < 8 :
                    #path_file = size_down_png(path_file)
                        await ctx.send(f'{tmpfile}')
                        await ctx.send(file = discord.File(path_file))
                    else :
                        await ctx.send(f"{tmpfile} size is bigger than 8Mb\ncan't send file")

                    for item in except_files :
                        if item not in tmpfile :
                            f_dict[tmpfile] = os.path.getmtime(tmpfile)

                    gap_start = time.time()
        
        # if change in getmtime
        for tmpfile in list(f_dict.keys()) :
            try :
                for item in except_files :
                    if item not in tmpfile :
                        newtm = os.path.getmtime(tmpfile)
                        if f_dict[tmpfile] != newtm : #if file is changed
                            print(f'{tmpfile} changed\n')
                            path_file = os.path.join(watchdir, tmpfile)
                            if os.path.getsize(path_file) / pow(1024, 2) < 8 :
                            #path_file = size_down_png(path_file)
                                await ctx.send(f'{tmpfile}')
                                await ctx.send(file = discord.File(path_file))
                            else :
                                await ctx.send(f'{tmpfile} size is bigger than 8Mb')

                            f_dict[tmpfile] = newtm
                            gap_start = time.time()
                            print(f'f_dict[tmpfile] = {f_dict[tmpfile]}, newtm = {newtm}')
            except FileNotFoundError :
                print('file not found')
                await ctx.send(f'{tmpfile} raised FileNotFoundError\n')
        #print(f_dict)

        global gap_now
        global stime
        gap_end = time.time()            
        gap_now = gap_end - gap_start
        stime = time_keeper(gap_now)


        print(f'<watchdog>\nresting for {round(gap_end - gap_start)}sec, sleeptime = {stime}\n')
        await asyncio.sleep(int(round(stime)))


@bot.command()
async def watchdog_info(ctx) :
    info_table = pd.DataFrame(columns = ['var', 'explane'], index = ['gap', 'sleeptime', 'log num', 'log volume'])
    info_table.loc['gap', 'var'] = round(gap_now)
    info_table.loc['gap', 'explane'] = 'sec | time after the last request'
    info_table.loc['sleeptime', 'var'] = stime
    info_table.loc['sleeptime', 'explane'] = 'sec | watchdog sleep time'
    info_table.loc['log num', 'var'] = len(os.listdir(watchdir))
    info_table.loc['log num', 'explane'] = 'num | of files in watchdir'
    info_table.loc['log volume', 'var'] = round(os.path.getsize(watchdir) / pow(1024, 2), 3)
    info_table.loc['log volume', 'explane'] = 'mb  | volume of watchdir'

    info_string = stable(info_table, 'Watchdog Info')
    f = open(os.path.join(watchdir, 'watchdog_info.txt'), 'w')
    f.write(info_string)
    f.close()

@bot.command()
async def watchdog_reset(ctx) :
    exceptions = ['watchdog_info.txt', 'watchdog_show.txt']
    for f in os.listdir(watchdir) :
        if f not in exceptions :
            os.remove(os.path.join(watchdir, f))


    await ctx.send('reset log - folder done !')
    await watchdog_info(ctx)


@bot.command()
async def watchdog_getall(ctx) :
    for f in os.listdir(watchdir) :
        await ctx.send(f'{f}')
        await ctx.send(file = discord.File(os.path.join(watchdir, f)))

    await ctx.send(f'{len(os.listdir(watchdir))} found, sent all !')


@bot.command()
async def watchdog_get(ctx, *, arg) :
    found_num = 0
    for f in os.listdir(watchdir) :
        if arg in f :
            found_num += 1
            await ctx.send(f'{f}')
            await ctx.send(file = discord.File(os.path.join(watchdir, f)))

    await ctx.send(f'{found_num} found, sent all !')

@bot.command()
async def watchdog_head(ctx) :
    # send latest 5 items in watchdir
    f_keys = f_dict.keys()
    f_values = f_dict.values()

    for val in f_values :
        pass




###################################################################
###################################################################
###################################################################

# work_flow
def workflow(arg) :
    os.chdir(workflow_dir)
    if f'{arg}.xlsx' in os.listdir(workflow_dir) :
        flower = read_excel(f'{arg}.xlsx')
        check_flower = 2 # there was the flower
    else :
        df = pd.DataFrame()
        df.to_excel(f'{arg}.xlsx')
        check_flower = 1 # desert :

    return check_flower, flower


@bot.command()
async def add_stem_to(ctx, *, arg, arg2) :   
    check_flower, flower = workflow(arg)
    if check_flower == 1 :
        await ctx.send(f'{arg}.xlsx is made and loaded !')
    else :
        await ctx.send(f'{arg}.xlsx loaded !')
        await ctx.send(stable(flower, arg))

    



# ----------------------------------------------------------------
# ETC.
# ----------------------------------------------------------------





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
