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

cred = credentials.Certificate('ovl-investement-game-firebase-adminsdk-4cnm0-7981270c80.json') # graffiti 버젼으로 바꿔야함
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://investment-game-e04fb-default-rtdb.asia-southeast1.firebasedatabase.app/'
})
dir = db.reference()

@bot.command(aliases=['팀'])
async def team_list(ctx):
    team = []
    ID_list = [] # 디스코드 아이디 list 
    EX_name = [] # 대표자분들 이름 list

    #list 미리 못 받을 경우를 생각해야함.

    for ID in ID_list:
        team.append(discord.utils.get(ctx.guild.roles, id = ID))
        break
    for team_number in range(len(team)) :
        if team[team_number] in ctx.author.roles and team_number == 0:
            await ctx.send(f'Hello ICISTS')
            break
        elif team[team_number] in ctx.author.roles and team_number != 0:
            await ctx.send(f'Hello Team{team_number} - 대표자 : {EX_name[team_number]}')
            break

@bot.command(aliases=['도움말'])
async def command(ctx):
    embed = discord.Embed(title="ICISTS 투자게임 명령어", description="투자 단위 : 만원", color=0x4432a8)
    embed.add_field(name="!도움말", value="투자게임에 필요한 명령어들을 알 수 있습니다.", inline=True)
    embed.add_field(name="!자산", value="본인 팀의 현재 자산을 알 수 있습니다.", inline=True)
    embed.add_field(name="!투자", value="투자하고 싶은 팀에게 투자할 수 있습니다.\n예시) !투자 1 1000\n= 1팀에 1000(만원)만큼 투자한다.", inline=True)
    embed.add_field(name="!팀", value="본인의 팀을 알 수 있습니다.", inline=True)
    embed.add_field(name="!전체팀", value="전체 팀과 팀별 번호를 알 수 있습니다.", inline=True) # 전체팀 코드 봐야함
    
    await ctx.send(embed=embed) 

# 평가 명령어도 만들어야함

@bot.command(aliases=['투자'])
async def invest(ctx, startup_num, amount): # 한 번에 여러 개 투자할 수 있게 해야함
    dir_round_num = db.reference('status/currentRound')
    round_num = dir_round_num.get() 

    team_list = []  # team ICISTS는 빠져있어야함.
    ID_list = [] # 디스코드 아이디 list , ICISTS 아이디는 없어야함

    for ID in ID_list:
        team_list.append(discord.utils.get(ctx.guild.roles, id = ID))

    for i in range(len(team_list)) :
        if team_list[i] in ctx.author.roles:
            team_number = i + 1
            break
    
    dir_teamAccount = db.reference(f'teams/{team_number}/account') 
    teamAccount = dir_teamAccount.get()
    if int(teamAccount) < int(amount) or teamAccount <= 0: 
        await ctx.send(f'{team_number}팀 - 해당 금액만큼 투자할 수 없습니다.')
    elif round_num == 0:
        await ctx.send(f'{team_number}팀 - 지금은 투자 시간이 아닙니다.')
    elif int(team_number) < 1 or int(team_number) > len(team_list) :
        await ctx.send(f'{team_number}팀 - 올바른 팀 숫자를 입력해주세요.')
    else:
        New_teamAccount = int(teamAccount) - int(amount)
    dir_invest = db.reference(f'rounds/{round_num}/investAmount/{startup_num}')
    dir_invest.update({f'{team_number}' : int(amount)})
    dir_teamAccount.update(New_teamAccount) # 잘 작동되는 지 확인 (update의 새로운 사용)
    await ctx.send(f'{team_number}팀 - {startup_num}번 스타트업에게 {amount}만원 만큼 투자하였습니다.\n{team_number}팀 - 현재 총 자산 {New_teamAccount}만원입니다.')



@bot.command(aliases=['자산'])
async def capital(ctx):
    dir_round_num = db.reference('status/currentRound')
    round_num = dir_round_num.get()

    if round_num == 0:
        await ctx.send('ICISTS 투자게임 - 현재 투자게임 결과를 계산중에 있습니다.\n라운드가 시작되면 다시 입력해주세요.')
    elif 1 <= round_num <= 3: # 라운드 범위 체크 필요
        team_list = []  # team ICISTS는 빠져있어야함.

        ID_list = [] # 디스코드 아이디 list , ICISTS 아이디는 없어야함

        for ID in ID_list:
            team_list.append(discord.utils.get(ctx.guild.roles, id = ID))

        for i in range(len(team_list)) :
            if team_list[i] in ctx.author.roles:
                team_number = i + 1 # team_number 체크 필요
                break

        dir = db.reference(f'teams/{team_number}/account')
        myCurrentCapital = dir.get()

        await ctx.send(f'{team_number}팀 - 현재 총 자산 {myCurrentCapital}만원입니다.')

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

@bot.command(aliases=['전체팀'])
async def all_team(ctx):
    embed = discord.Embed(title="ICISTS 투자게임", color=0x4432a8)
    embed.add_field(name="팀 번호 - 참여 팀", value="1팀 - 엄태윤\n2팀 - 범지민\n3팀 - 오정섭\n4팀 - 박은수\n5팀 - 이번영\n6팀 - 이상윤\n7팀 - 김은총\n8팀 - 김이삭", inline=True)
    
    await ctx.send(embed=embed)
#이름 변경 필요

# 투자 알고리즘 적용시키는 명령어도 필요함
@bot.command()
async def calculate_rank(ctx):
    dir_round_num = db.reference('status/currentRound')
    round_num = dir_round_num.get()

    data_list = []
    for team_num in range(1,team_number+1) : 
        dir_account = db.reference(f'teams/{team_num}/account')
        account = dir_account.get()
        data = (team_num,account)
        data_list.append(data)

    await ctx.send(f'{round_num}라운드 투자 결과를 반영한 자산 데이터를 받아왔습니다.')
    data_list.sort(key = lambda x : x[1], reverse= True)
    
    for i in range(1,team_number+1):
        dir_Rank = db.reference(f'rounds/{round_num}/rank')
        dir_Rank.update({f'{i}위' : data[i-1][0]})
            
    await ctx.send(f'ICISTS 투자게임 - {round_num}라운드 순위 계산이 완료되었습니다.')
    # 각 팀의 라운드 별 순위가 필요한가?
    # 동점자 처리 >> 말할 때 하면 될 거 같긴 함.

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
            dir.update(formula) # update의 새로운 사용
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
    
    await ctx.send(f'ICISTS 투자게임 - {round_num}라운드 각 팀의 투자 결과 정산이 완료되었습니다. ')

@bot.command()
async def calculate_final(ctx):
    dir_round_num = db.reference('status/currentRound')
    round_num = dir_round_num.get()
    if round_num < 3:
        await ctx.send('ICISTS 투자게임 - 아직 투자게임이 종료되지 않았습니다.')
    elif round_num == 3:
        totalCapital_data = []
        for team_num in range(1,team_number+1):
            dir_totalAccount = db.reference(f'team/{team_num}/account')
            totalMoney = dir_totalAccount.get()
            data = (team_num, totalMoney)
            totalCapital_data.append(data)
        await ctx.send('ICISTS 투자게임 - 최종 결과 데이터를 받아왔습니다.')
        totalCapital_data.sort(key = lambda x : x[1], reverse = True)
        await ctx.send('ICISTS 투자게임 - 최종 순위 계산이 완료되었습니다.')
        for i in range(1,4):
            dir_finalRank = db.reference('result')
            dir_finalRank.update({f'{i}위' : totalCapital_data[i-1][0]})
        await ctx.send(f'ICISTS 투자게임 - 최종 순위 계산이 완료되었습니다.')

@bot.event
async def on_ready():
    print('Bot initialized')
    print(f'{bot.user} has connected to Discord!')
    return
            
@bot.command(aliases=['hi'])
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.mention}!')



bot.run(os.environ['token'])