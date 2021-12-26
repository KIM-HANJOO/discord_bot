import discord
from discord.ext import commands

import asyncio
import nest_asyncio
import os

module_dir = os.getcwd() + '\\module'
token_dir = os.getcwd() + '\\token'

import sys
sys.path.append(module_dir)
sys.path.append(token_dir)

bot=commands.Bot(command_prefix='./')

to = 'OTAzNTM4MjA0NzM5NzY4MzIx.YXubhg.tqThOF_xwrf78KrYDtiCLwGWKLA'

@bot.event
async def on_ready() :
	print('로그인중입니다 ')
	print(f"봇 = {bot.user.name}으로 연결중")
	print("연결이 완료되었습니다.")
	await bot.change_presence(status = discord.Status.online, activity = None)

@bot.command(aliases=['hi'])
async def 안녕(ctx):
    await ctx.send('안녕하세요.')

@bot.command()    
async def 따라하기(ctx,*,text):
    await ctx.send(text)


bot.run(to)
