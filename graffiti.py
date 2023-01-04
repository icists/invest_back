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

cred = credentials.Certificate('investment-game-e04fb-firebase-adminsdk-q4spd-bcff64ea68.json') 
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://investment-game-e04fb-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

global team_number
global startup_list 
startup_list = ['QTC','AET','INB','SHZ','RFY','SWT','NUT','NUV']
team_number = 24

@bot.command(aliases=['hi'])
async def hello(ctx):
    await ctx.send('ver 2.1.6')

@bot.command()
async def set_round(ctx, set_round_num):
    if int(set_round_num) == 0 or int(set_round_num) == 1 or int(set_round_num) == 2 or int(set_round_num) == 3: #라운드 범위 체크 필요
        dir = db.reference('status')
        dir.update({'currentRound': int(set_round_num)})
        await ctx.send(f'ICISTS 투자게임 - 현재 {set_round_num}라운드로 설정되었습니다.')
    elif int(set_round_num) == 999:
        dir = db.reference('status')
        dir.update({'currentRound': int(set_round_num)})
        await ctx.send(f'ICISTS 투자게임 - 현재 999 라운드로 설정되었습니다.\nICISTS 투자게임 - 현재 설정 중입니다')
    else:
        await ctx.send(f'ICISTS 투자게임 - 올바른 숫자를 입력해주세요.')

@bot.command()
async def function1(ctx , input):
    dir_round_num = db.reference('status/currentRound')
    round_num = dir_round_num.get() 
    total_investment = 0
    
    alpha = float(input)

    await ctx.send(f'function1 작동 시작')
    
    for startup_name in startup_list:  
        for team_num in range(1,team_number + 1) :
            dir_investmentData = db.reference(f'rounds/{round_num}/investAmount/{team_num}/{startup_name}')
            invest = int(dir_investmentData.get())
            total_investment += invest
    avg_investment = total_investment / 8
    await ctx.send(f'전체 스타트업 평균 투자액 : {avg_investment}')

    invest_list = [0] * 8 #각 기업별 총 투자액 리스트
    index = 0
    for startup_name in startup_list: # 각 기업별 각 팀에게 돌려줄 금액 계산
        total_invest_eachCompany = 0
        for team_num in range(1, team_number + 1) :
            dir_investmentData = db.reference(f'rounds/{round_num}/investAmount/{team_num}/{startup_name}')
            invest = int(dir_investmentData.get())
            total_invest_eachCompany += invest
        invest_list[index] = total_invest_eachCompany
        index += 1
    await ctx.send('각 스타트업별 받은 총 투자액 정산이 완료되었습니다.')
    
    total_score = 0
    for startup_name in startup_list: # 각 기업별 VC에게 받은 평가
        dir_total_score = db.reference(f'rounds/{round_num}/score/{startup_name}')
        total_score += dir_total_score.get()
    avg_score = total_score / 8
    await ctx.send(f'각 스타트업에 대한 VC 평가 완료, 평균 점수 : {avg_score}')

    index = 0
    for startup_name in startup_list:
        for team_num in range(1,team_number+1):
            dir = db.reference(f'rounds/{round_num}/investResult/{team_num}')
            dir_investmentData = db.reference(f'rounds/{round_num}/investAmount/{team_num}/{startup_name}')
            dir_valuation = db.reference(f'rounds/{round_num}/valuation')
            dir_score = db.reference(f'rounds/{round_num}/score/{startup_name}')
            score = dir_score.get()
            invest = int(dir_investmentData.get())
            valuation = int((invest_list[index]/avg_investment)**(alpha) * (score / avg_score) * avg_investment)
            dir_valuation.update({f'{startup_name}' : valuation})
            formula = int(((invest_list[index]/avg_investment)**(alpha - 1)) * invest * (score / avg_score))
            dir.update({f'{startup_name}' : formula}) 
        index += 1
    await ctx.send(f'ICISTS 투자게임 - {round_num}라운드 각 팀에게 돌려줄 금액 계산이 완료되었습니다. ')

@bot.command()
async def function2(ctx):
    dir_round_num = db.reference('status/currentRound')
    round_num = dir_round_num.get() 

    await ctx.send(f'function2 작동 시작')

    for team_num in range(1,team_number+1):
        team_account = 0
        for startup_name in startup_list:
            dir_investResult = db.reference(f'rounds/{round_num}/investResult/{team_num}/{startup_name}')
            team_account += dir_investResult.get()
        dir_teamAccount = db.reference(f'teams/{team_num}')
        dir_teamAccount.update({'account' : team_account})

    await ctx.send(f'ICISTS 투자게임 - {round_num}라운드 각 팀의 투자 결과 정산이 완료되었습니다')

@bot.command()
async def base_setting(ctx, round_num):
    await ctx.send(f'ICISTS 투자게임 - {round_num} 라운드 기본 설정을 시작합니다.\n')
    for startup_name in startup_list:
        dir = db.reference(f'rounds/{round_num}/valuation')
        dir.update({
            f'{startup_name}' : 0
        })
    
    for team_num in range(1,team_number+1):
        dir = db.reference(f'rounds/{round_num}/investAmount')
        dir.update({
            f'{team_num}' : 0
        })
    
    for team_num in range(1,team_number+1):
        dir = db.reference(f'rounds/{round_num}/investResult')
        dir.update({
            f'{team_num}' : 0
        })
    
    await ctx.send(f'ICISTS 투자게임 - {round_num} 라운드 기본 설정을 완료했습니다.\n')

@bot.command()
async def able(ctx):
    dir = db.reference('status')
    dir.update({
        'investable' : True
    })
    await ctx.send('ICISTS 투자게임 - 현재 투자가 가능하게 되었습니다.')

@bot.command()
async def unable(ctx):
    dir = db.reference('status')
    dir.update({
        'investable' : False
    })
    await ctx.send('ICISTS 투자게임 - 현재 투자가 불가능하게 되었습니다.')
    

@bot.command()
async def setting(ctx, round_num):
    await ctx.send(f'ICISTS 투자게임 - {round_num} 라운드 Firebase 데이터베이스 설정을 시작합니다.\n')

    defaultmoney = 10000000

    for team_num in range(1,team_number+1):
        dir = db.reference(f'teams/{team_num}')
        dir.update({
            'account' : defaultmoney
        })

    for team_num in range(1, team_number + 1):
        dir_investAmount= db.reference(f'rounds/{round_num}/investAmount/{team_num}')
        dir_investAmount.set({ 
            f'{startup_list[0]}' : int(random.random()*1250000),
            f'{startup_list[1]}' : int(random.random()*1250000),
            f'{startup_list[2]}' : int(random.random()*1250000),
            f'{startup_list[3]}' : int(random.random()*1250000),
            f'{startup_list[4]}' : int(random.random()*1250000),
            f'{startup_list[5]}' : int(random.random()*1250000),
            f'{startup_list[6]}' : int(random.random()*1250000),
            f'{startup_list[7]}' : int(random.random()*1250000)

        })
    for team_num in range(1, team_number + 1):
        dir_investResult= db.reference(f'rounds/{round_num}/investResult/{team_num}')
        dir_investResult.set({ 
            f'{startup_list[0]}' : 0,
            f'{startup_list[1]}' : 0,
            f'{startup_list[2]}' : 0,
            f'{startup_list[3]}' : 0,
            f'{startup_list[4]}' : 0,
            f'{startup_list[5]}' : 0,
            f'{startup_list[6]}' : 0,
            f'{startup_list[7]}' : 0
        })

    
    dir_score = db.reference(f'rounds/{round_num}/score')
    dir_score.set({
        f'{startup_list[0]}' : 10,
        f'{startup_list[1]}' : 8,
        f'{startup_list[2]}' : 4,
        f'{startup_list[3]}' : 6,
        f'{startup_list[4]}' : 5,
        f'{startup_list[5]}' : 4,
        f'{startup_list[6]}' : 3,
        f'{startup_list[7]}' : 2
    })

    for startup_name in startup_list :
        dir_valuation = db.reference(f'rounds/{round_num}/valuation')
        dir_valuation.update({
            f'{startup_name}' : 0
        })
    await ctx.send(f'ICISTS 투자게임 - Firebase 데이터 기본 설정이 완료되었습니다.\n')

bot.run(os.environ['token'])