#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# _authors_: Vozec
# _date_ : 27/08/2022

import discord,json,os,logging
from discord.ext import commands

from utils.logger  import logger
from utils.utils   import *
from utils.discord import *

config 	= json.loads(open('config.json','r').read().strip())
bot		= discord.ext.commands.Bot(command_prefix=config["PREFIX"],intents = discord.Intents.all())

async def Analyse(ctx,id):
	user		= await bot.fetch_user(id)
	infos,coeff	= Fetch_user(ctx,user,config)
	result		= Analyse_infos(infos,coeff)
	Send_result(result,config['WEBHOOK'])

@bot.event
async def on_ready():
	print('%s has connected to Discord!\n'%bot.user.name)
	await bot.change_presence(
		status=discord.Status.online,
	 	activity=discord.Game('Preventing Multi-Account')
	)

@bot.event
async def on_member_join(ctx):
	await Analyse(ctx,id)

@bot.command()
async def check(ctx,id=None):
	if(ctx.author.guild_permissions.manage_channels and id):
		try:
			id 		= int(id[2:-1])
			member	= ctx.message.guild.get_member(id)
			await Analyse(member,id)
		except Exception as ex:
			logger('Error: %s'%ex,'error',1,0)

if __name__ == '__main__':
	bot.run(config['TOKEN_BOT'])
