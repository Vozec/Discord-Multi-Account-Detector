#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# _authors_: Vozec
# _date_ : 27/08/2022

from datetime import datetime

from utils.discord import Fetch_from_user

def Convert2Date(time):
	if(time//60 < 60):
		return '%s min'%round(time//60)
	elif(time < 24*60*60):
		return '%s hours'%round(time//(60*60))
	else:
		return '%s days'%round(time//(60*60*24))

def Check_nitro(ctx):
	nitro_discriminator = ['0000','0001','1337','1234','6969','1111','2222','3333','4444','5555','6666','7777','8888','9999']
	if ctx.premium_since is not None \
		or (ctx.avatar and ctx.avatar.is_animated()) \
		or ctx.discriminator in nitro_discriminator:
		return True
	return False

def Fetch_user(ctx,user,config):
	time_diff = round(datetime.now().timestamp() - ctx.created_at.timestamp())
	infos =  {
		'name':ctx.name,
		'tag':ctx.discriminator,
		'id':ctx.id,
		'avatar':ctx.avatar,
		'default_avatar':ctx.default_avatar,
		'ismobile':ctx.is_on_mobile(),
		'creation':ctx.created_at,
		'created_diff': round(time_diff),
		'created_for': Convert2Date(time_diff),
		'flags':ctx.public_flags.all(),
		'nitro':Check_nitro(ctx),
		'banner': user.banner,
		'color': user.color,
		'activities': ctx.activities,
		'status':ctx.status,
		'web_status':ctx.web_status
	}

	coeff = 1.22
	token = config['TOKEN_USER'] if 'TOKEN_USER' in config else None
	if token:
		infos['bio'],infos['accounts'] = Fetch_from_user(ctx.id,token)
		if infos['bio']:
			coeff = 1

	return infos,coeff

def Analyse_infos(infos,coeff=1.22):
	score = 0
	if(infos['avatar']):								score += 20
	if(infos['ismobile']):								score += 5
	if(len(infos['flags'])>0): 							score += min(len(infos['flags']),3) *5
	if(infos['nitro']):									score += 15
	if(infos['banner']):								score += 5
	if(infos['status'].value == 'online'):				score += 2 
	if(str(infos['color']) in ['#000000','#ffffff']):	score += 5
	if(len(infos['activities']) > 0):					score += min(len(infos['activities']),2) *5
	if(infos['bio']):									score += 10
	if(infos['accounts']):								score += min(len(infos['accounts']),4)*5
	if(infos['web_status'].value in ['online','idle']):	score -= 15
	if(infos['created_diff'] < 1814400):				score -= 40 # 3weeks
	elif(infos['created_diff'] < 15552000):				score -= 20 # 6 months
	elif(infos['created_diff'] < 62208000):				score -= 10 # 2 years
	elif(infos['created_diff'] / (60*60*24*365) > 4.0):	score += 7 * (infos['created_diff'] / (60*60*24*365)) # > 4 years

	infos['score'] = max(min(round(score*coeff),100),0)

	if  (infos['score'] > 80) : infos['color'] = '8fce00'
	elif(infos['score'] > 60) : infos['color'] = 'FFD966'
	elif(infos['score'] > 40) : infos['color'] = 'ce7e00'
	else 					  : infos['color'] = 'f44336'

	return infos
