#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# _authors_: Vozec
# _date_ : 27/08/2022

from discord_webhook import DiscordWebhook, DiscordEmbed
import requests,json

from utils.logger import logger

def Send_result(infos,url):
	icon 	= (str(infos['avatar']) if infos['avatar'] else str(infos['default_avatar']))	
	webhook = DiscordWebhook(url=url)
	embed 	= DiscordEmbed(title='%s#%s'%(infos['name'],infos['tag']), description='', color=infos['color'])

	embed.set_author(name=str(infos['name']), url='', icon_url=icon)
	embed.set_footer(text='', icon_url=icon)
	embed.set_timestamp()

	embed.add_embed_field(name='Account Id'	, value=str(infos['id'])			, inline=False)
	embed.add_embed_field(name='Score'		, value='%s/100'%str(infos['score']), inline=False)
	embed.add_embed_field(name='Created the', value=str(infos['creation'])		, inline=True )
	embed.add_embed_field(name='Created for', value=str(infos['created_for'])	, inline=True )

	
	webhook.add_embed(embed)
	response = webhook.execute()

	logger("User Check: %s | Score: %s"%(infos['name'],infos['score']),'warning',0,0)

def Fetch_from_user(id,token):	
	try:
		url = 'https://discord.com/api/v9/users/%s/profile'%id
		res = requests.get(url,headers={"authorization":token})
		if(res.status_code == 200):
			rep = json.loads(res.text)
			bio = rep['user']['bio']
			accounts = rep['connected_accounts']
			return bio,accounts
	except Exception as ex:
		logger('Error: %s'%ex,'error',1,0)

	return None,None