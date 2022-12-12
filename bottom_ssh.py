import discord
from discord.ext import commands

import asyncio
import nest_asyncio
import os
import time
import paramiko

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

## import submodules from module_dir ##
#import submodule_watchdog as sw
#exec(os.path.join(module_dir, 'submodule_watchdog.py'))
#######################################

main_dir = os.getcwd()
log_dir = os.path.join(main_dir, 'log')

# ----------------------------------------------------------------
# make sample
# ----------------------------------------------------------------
from PIL import Image

def sample_maker(log_dir, title) :
    image = Image.new(mode = 'P', size = (10, 10), color = 'red')
    os.chdir(log_dir)
    image.save(f'{title}.png')
    print('saved')

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


# ----------------------------------------------------------------
# watchdog
# ----------------------------------------------------------------

github_shared_dir = os.path.join('mnt', 'c', 'Users', 'joo09', 'Documents', 'Github', 'watchdog')
to_dropbox_dir = os.path.join(github_shared_dir, 'micro_climate', 'to_dropbox')
https_dir = os.path.join(github_shared_dir, 'https')
drop_dir = os.path.join('mnt', 'd', 'Dropbox', 'github_shared')

src_dir = [to_dropbox_dir, https_dir]
dst_dir = [drop_dir]
#urg_src_dir = [https_dir]



# watchdog with ssh    
@bot.command()
async def watchdog(ctx) :
    log_all = ''

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh.connect('192.168.219.101', username = 'bp', password = 'hanjoo970')

    # init
    last_info_dict = dict()
    for direc in src_dir :
        stdin, stdout, stderr = ssh.exec_command(f'ls -l {direc}')
        lines = stdout.readlines()
        info_list = lines[1 :]
        last_info_dict[direc] = info_list
        

    while True :
        # init
        check = False
        log = ''

        # 
        for direc in src_dir :
            time_now = time.ctime()
            stdin, stdout, stderr = ssh.exec_command(f'ls -l {direc}')
            lines = stdout.readlines()
            info_list = lines[1 :]
            last_info = last_info_dict[direc]

            if info_list != last_info :
                os.system(f'rsync bp@192.168.219.101:{direc} bp@192.168.219.101:{dst_dir[0]}')
                check = True
            else :
                log == f'{time_now}\t{direc}\t{-newest}'

                if check != True :
                    check = False

            last_info_dict[direc] = info_list

        if check == True :
            await ctx.send(f'{log}\nsleeping 5min...')
            print('sleeping 5min ...')
            time.sleep(60 * 5)
        else :
            await ctx.send(f'{log}\nsleeping 60min...')
            print('sleeping 60min ...')
            time.sleep(60 * 60)
        
    ssh.close()
    
    


# ----------------------------------------------------------------
# HTTP Request
# ----------------------------------------------------------------

async def add_summoner(ctx, *, arg) :
    pass
    



