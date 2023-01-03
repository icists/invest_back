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
bot = commands.Bot(command_prefix='!', Status=discord.Status.online, activity=game,intents=discord.Intents.default())
client = discord.Client(intents = discord.Intents.default())

cred = credentials.Certificate('investment-game-e04fb-firebase-adminsdk-q4spd-bcff64ea68.json') 
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://investment-game-e04fb-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

global team_number
team_number = 18

@bot.event
async def on_ready():
    print('Bot initialized')
    print(f'{bot.user} has connected to Discord!')
    return

@bot.command(aliases=['hi'])
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.mention}!')

@bot.command()
async def set_round(ctx, set_round_num):
    if int(set_round_num) == 1 or int(set_round_num) == 2 or int(set_round_num) == 3: #라운드 범위 체크 필요
        dir = db.reference('status')
        dir.update({'currentRound': int(set_round_num)})
        await ctx.send(f'ICISTS 투자게임 - 현재 {set_round_num}라운드로 설정되었습니다.')
    elif int(set_round_num) == 0:
        dir = db.reference('status')
        dir.update({'currentRound': int(set_round_num)})
        await ctx.send(f'ICISTS 투자게임 - 현재 {set_round_num}라운드로 설정되었습니다.\nICISTS 투자게임 - 라운드가 진행되고 있지 않습니다.')
    else:
        await ctx.send(f'ICISTS 투자게임 - 올바른 숫자를 입력해주세요.')

@bot.command()
async def calculate_return(ctx):
    dir_round_num = db.reference('status/currentRound')
    round_num = dir_round_num.get() 
    total_investment = 0
    alpha = 1.5
    
    for startup_num in range(1,9):  
        for team_num in range(1,team_number + 1) :
            dir_investmentData = db.reference(f'rounds/{round_num}/investAmount/{startup_num}/{team_num}')
            invest = dir_investmentData.get()
            total_investment += invest
    avg_investment = total_investment / 8
    await ctx.send(f'전체 스타트업 평균 투자액 : {avg_investment}')

    invest_list = [0] * 9 #각 기업별 총 투자액 리스트, 인덱스 0 은 사용하지 않음
    for startup_num in range(1,9): # 각 기업별 각 팀에게 돌려줄 금액 계산
        total_invest_eachCompany = 0
        for team_num in range(1, team_number + 1) :
            dir_investmentData = db.reference(f'rounds/{round_num}/investAmount/{startup_num}/{team_num}')
            invest = dir_investmentData.get()
            total_invest_eachCompany += invest
        invest_list[startup_num] = total_invest_eachCompany
    await ctx.send('각 스타트업별 받은 총 투자액 정산이 완료되었습니다.')
    
    total_valuation = 0
    for startup_num in range(1,9): # 각 기업별 VC에게 받은 평가
        dir_total_valuation = db.reference(f'rounds/{round_num}/valuation/{startup_num}')
        total_valuation += dir_total_valuation.get()
    avg_valuation = total_valuation / 8
    await ctx.send(f'각 스타트업에 대한 VC 평가 완료, 평균 점수 : {avg_valuation}')

    for startup_num in range(1,9):
        for team_num in range(1,team_number+1):
            dir = db.reference(f'rounds/{round_num}/investResult/{startup_num}/{team_num}')
            dir_investmentData = db.reference(f'rounds/{round_num}/investAmount/{startup_num}/{team_num}')
            dir_valuation = db.reference(f'rounds/{round_num}/valuation/{startup_num}')
            valuation = dir_valuation.get()
            invest = dir_investmentData.get()
            formula = int(((invest_list[startup_num]/avg_valuation)**(alpha - 1)) * invest * (valuation / avg_valuation))
            dir.update({formula}) # update의 새로운 사용
    await ctx.send(f'ICISTS 투자게임 - {round_num}라운드 각 팀에게 돌려줄 금액 계산이 완료되었습니다. ')

@bot.command()
async def sum_account(ctx):
    dir_round_num = db.reference('status/currentRound')
    round_num = dir_round_num.get() 

    for team_num in range(1,team_number+1):
        team_account = 0
        for startup_num in range(1,9):
            dir_investResult = db.reference(f'rounds/{round_num}/investResult/{startup_num}/{team_num}')
            team_account += dir_investResult.get()
        dir_teamAccount = db.reference(f'teams/{team_num}')
        dir_teamAccount.update({'account' : team_account})

    await ctx.send(f'ICISTS 투자게임 - {round_num}라운드 각 팀의 투자 결과 정산이 완료되었습니다')

    bot.run('MTA1ODMwMjA2NTAxNDc1NTMzOA.GAnyUX.8MQ2p2TfipWZxnjGYKyDt5gRiHp3Ku8uCYCJfQ')