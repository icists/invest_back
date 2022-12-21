from audioop import reverse
from signal import SIG_DFL
from this import d
from xml.etree.ElementTree import tostring
import discord, os
import asyncio
from discord import message
from discord.ext import commands
import random

import json

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

game = discord.Game("ICISTS-KAIST")
bot = commands.Bot(command_prefix='!', Status=discord.Status.online, activity=game)
client = discord.Client()

cred = credentials.Certificate('ovl-investement-game-firebase-adminsdk-4cnm0-7981270c80.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://ovl-investement-game-default-rtdb.asia-southeast1.firebasedatabase.app/'
})
dir = db.reference()

@bot.command()
async def default_firebase_test(ctx):
    dir.update({'test':'Hello World'})
    await ctx.send('ICISTS 투자게임 - Firebase 테스트가 완료되었습니다.')

bot.run(os.environ['token'])