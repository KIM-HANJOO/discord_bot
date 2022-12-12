import discord
from discord.ext import commands

import asyncio
import nest_asyncio
import os
import time
from PIL import Image
from pathlib import Path


module_dir = os.getcwd()
main_dir = Path(module_dir).parent
token_dir = os.path.join(module_dir, 'token')
watchdir = os.path.join(main_dir, 'log')
workflow_dir = os.path.join(main_dir, 'workflow')
message_dir = os.path.join(main_dir, 'message')

import sys
sys.path.append(module_dir)
sys.path.append(main_dir)
import table
import pandas as pd


#@bot.command()
async def send_sample(ctx) :
    await ctx.send('hi!')


