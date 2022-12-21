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

def rank_ratio(rank):
    if rank == 1:
        return 1.25
    elif rank == 2:
        return 1.20
    elif rank == 3:
        return 1.15
    elif rank == 4:
        return 1.10
    elif rank == 5:
        return 1.05
    elif rank == 6:
        return 1.0
    elif rank == 7:
        return 0.95
    elif rank == 8:
        return 0.90
    elif rank == 9:
        return 0.85
    elif rank == 10:
        return 0.80
    elif rank == 11:
        return 0.75
    elif rank == 12:
        return 0.75

@bot.event
async def on_ready():
    print('Bot initialized')
    print(f'{bot.user} has connected to Discord!')
    return
            
@bot.command(aliases=['hi'])
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.mention}!')

@bot.command(aliases=['팀'])
async def team(ctx):
    teamICISTS = discord.utils.get(ctx.guild.roles, id = 1011716391138770964)
    team1 = discord.utils.get(ctx.guild.roles, id = 1010074740389584978)
    team2 = discord.utils.get(ctx.guild.roles, id = 1010074862435450961)
    team3 = discord.utils.get(ctx.guild.roles, id = 1010074892038848523)
    team4 = discord.utils.get(ctx.guild.roles, id = 1010074912016310272)
    team5 = discord.utils.get(ctx.guild.roles, id = 1010074931293343817)
    team6 = discord.utils.get(ctx.guild.roles, id = 1010074960053674006)
    team7 = discord.utils.get(ctx.guild.roles, id = 1010075019658932327)
    team8 = discord.utils.get(ctx.guild.roles, id = 1010075048587046982)
    team9 = discord.utils.get(ctx.guild.roles, id = 1010075088265166858)
    team10 = discord.utils.get(ctx.guild.roles, id = 1010075116354416700)
    team11 = discord.utils.get(ctx.guild.roles, id = 1010075159744495657)
    team12 = discord.utils.get(ctx.guild.roles, id = 1010075196293652550)
    if teamICISTS in ctx.author.roles:
        await ctx.send(f'Hello ICISTS')
    elif team1 in ctx.author.roles:
        await ctx.send(f'Hello Team1 - 대표자 : 엄태윤')
    elif team2 in ctx.author.roles:
        await ctx.send(f'Hello Team2 - 대표자 : 범지민')
    elif team3 in ctx.author.roles:
        await ctx.send(f'Hello Team3 - 대표자 : 오정섭')
    elif team4 in ctx.author.roles:
        await ctx.send(f'Hello Team4 - 대표자 : 박은수')
    elif team5 in ctx.author.roles:
        await ctx.send(f'Hello Team5 - 대표자 : 이번영')
    elif team6 in ctx.author.roles:
        await ctx.send(f'Hello Team6 - 대표자 : 이상윤')
    elif team7 in ctx.author.roles:
        await ctx.send(f'Hello Team7 - 대표자 : 김은총')
    elif team8 in ctx.author.roles:
        await ctx.send(f'Hello Team8 - 대표자 : 김이삭')
    elif team9 in ctx.author.roles:
        await ctx.send(f'Hello Team9')
    elif team10 in ctx.author.roles:
        await ctx.send(f'Hello Team10')
    elif team11 in ctx.author.roles:
        await ctx.send(f'Hello Team11')
    elif team12 in ctx.author.roles:
        await ctx.send(f'Hello Team12')

@bot.command(aliases=['도움말'])
async def command(ctx):
    embed = discord.Embed(title="ICISTS 투자게임 명령어", description="투자 단위 : 만원", color=0x4432a8)
    embed.add_field(name="!도움말", value="투자게임에 필요한 명령어들을 알 수 있습니다.", inline=True)
    embed.add_field(name="!자산", value="본인 팀의 현재 자산을 알 수 있습니다.", inline=True)
    embed.add_field(name="!투자", value="투자하고 싶은 팀에게 투자할 수 있습니다.\n예시) !투자 1 1000\n= 1팀에 1000(만원)만큼 투자한다.", inline=True)
    embed.add_field(name="!팀", value="본인의 팀을 알 수 있습니다.", inline=True)
    embed.add_field(name="!전체팀", value="전체 팀과 팀별 번호를 알 수 있습니다.", inline=True)
    
    message = await ctx.send(embed=embed)

@bot.command(aliases=['전체팀'])
async def all_team(ctx):
    embed = discord.Embed(title="ICISTS 투자게임", color=0x4432a8)
    embed.add_field(name="팀 번호 - 참여 팀", value="1팀 - 엄태윤\n2팀 - 범지민\n3팀 - 오정섭\n4팀 - 박은수\n5팀 - 이번영\n6팀 - 이상윤\n7팀 - 김은총\n8팀 - 김이삭", inline=True)
    
    message = await ctx.send(embed=embed)

@bot.command(aliases=['투자'])
async def invest(ctx, to_team, ammount):
    dir_round_num = db.reference('setting/roundNum')
    round_num = dir_round_num.get()

    team1 = discord.utils.get(ctx.guild.roles, id = 1010074740389584978)
    team2 = discord.utils.get(ctx.guild.roles, id = 1010074862435450961)
    team3 = discord.utils.get(ctx.guild.roles, id = 1010074892038848523)
    team4 = discord.utils.get(ctx.guild.roles, id = 1010074912016310272)
    team5 = discord.utils.get(ctx.guild.roles, id = 1010074931293343817)
    team6 = discord.utils.get(ctx.guild.roles, id = 1010074960053674006)
    team7 = discord.utils.get(ctx.guild.roles, id = 1010075019658932327)
    team8 = discord.utils.get(ctx.guild.roles, id = 1010075048587046982)
    team9 = discord.utils.get(ctx.guild.roles, id = 1010075088265166858)
    team10 = discord.utils.get(ctx.guild.roles, id = 1010075116354416700)
    team11 = discord.utils.get(ctx.guild.roles, id = 1010075159744495657)
    team12 = discord.utils.get(ctx.guild.roles, id = 1010075196293652550)
    if team1 in ctx.author.roles:
        from_team = 1
    elif team2 in ctx.author.roles:
        from_team = 2
    elif team3 in ctx.author.roles:
        from_team = 3
    elif team4 in ctx.author.roles:
        from_team = 4
    elif team5 in ctx.author.roles:
        from_team = 5
    elif team6 in ctx.author.roles:
        from_team = 6
    elif team7 in ctx.author.roles:
        from_team = 7
    elif team8 in ctx.author.roles:
        from_team = 8
    elif team9 in ctx.author.roles:
        from_team = 9
    elif team10 in ctx.author.roles:
        from_team = 10
    elif team11 in ctx.author.roles:
        from_team = 11
    elif team12 in ctx.author.roles:
        from_team = 12
    
    dir_myCurrentCapital = db.reference(f'team/{from_team}/currentCapital')
    myCurrentCapital = dir_myCurrentCapital.get()
    if int(myCurrentCapital) < int(ammount) or myCurrentCapital <= 0: 
        await ctx.send(f'{from_team}팀 - 해당 금액만큼 투자할 수 없습니다.')
    elif round_num == 0:
        await ctx.send(f'{from_team}팀 - 지금은 투자 시간이 아닙니다.')
    elif int(from_team) == int(to_team):
        await ctx.send(f'{from_team}팀 - 자신의 팀에게 투자할 수 없습니다.')
    elif int(to_team) < 1 or int(to_team) > 8:
        await ctx.send(f'{from_team}팀 - 올바른 팀 숫자를 입력해주세요.')
    else:
        myNewCapital = int(myCurrentCapital) - int(ammount)

        if round_num == 1:
            dir_theirCurrentInvestment = db.reference(f'team/{to_team}/firstInvestment')
            theirCurrentInvestment = dir_theirCurrentInvestment.get()
            theirNewInvestment = int(theirCurrentInvestment) + int(ammount)

            dir = db.reference(f'team/{to_team}')
            dir.update({'firstInvestment' : int(theirNewInvestment)})
        elif round_num == 2:
            dir_theirCurrentInvestment = db.reference(f'team/{to_team}/secondInvestment')
            theirCurrentInvestment = dir_theirCurrentInvestment.get()
            theirNewInvestment = int(theirCurrentInvestment) + int(ammount)

            dir = db.reference(f'team/{to_team}')
            dir.update({'secondInvestment' : int(theirNewInvestment)})
        elif round_num == 3:
            dir_theirCurrentInvestment = db.reference(f'team/{to_team}/thirdInvestment')
            theirCurrentInvestment = dir_theirCurrentInvestment.get()
            theirNewInvestment = int(theirCurrentInvestment) + int(ammount)

            dir = db.reference(f'team/{to_team}')
            dir.update({'thirdInvestment' : int(theirNewInvestment)})

        dir = db.reference(f'round/{round_num}/{from_team}')
        dir.update({f'{to_team}' : int(ammount)})

        dir = db.reference(f'team/{from_team}')
        dir.update({'currentCapital' : int(myNewCapital)})

        dir_theirCurrentTotalInvestment = db.reference(f'team/{to_team}/totalInvestment')
        theirCurrentTotalInvestment = dir_theirCurrentTotalInvestment.get()
        theirNewTotalInvestment = int(theirCurrentTotalInvestment) + int(ammount)
        dir = db.reference(f'team/{to_team}')
        dir.update({'totalInvestment' : int(theirNewTotalInvestment)})

        await ctx.send(f'{from_team}팀 - {to_team}팀에게 {ammount}만원 만큼 투자하였습니다.\n{from_team}팀 - 현재 총 자산 {myNewCapital}만원입니다.')

@bot.command(aliases=['자산'])
async def capital(ctx):
    dir_round_num = db.reference('setting/roundNum')
    round_num = dir_round_num.get()

    if round_num == 0:
        await ctx.send('ICISTS 투자게임 - 현재 투자게임 결과를 계산중에 있습니다.\n라운드가 시작되면 다시 입력해주세요.')
    elif 1 <= round_num <= 3:
        team1 = discord.utils.get(ctx.guild.roles, id = 1010074740389584978)
        team2 = discord.utils.get(ctx.guild.roles, id = 1010074862435450961)
        team3 = discord.utils.get(ctx.guild.roles, id = 1010074892038848523)
        team4 = discord.utils.get(ctx.guild.roles, id = 1010074912016310272)
        team5 = discord.utils.get(ctx.guild.roles, id = 1010074931293343817)
        team6 = discord.utils.get(ctx.guild.roles, id = 1010074960053674006)
        team7 = discord.utils.get(ctx.guild.roles, id = 1010075019658932327)
        team8 = discord.utils.get(ctx.guild.roles, id = 1010075048587046982)
        team9 = discord.utils.get(ctx.guild.roles, id = 1010075088265166858)
        team10 = discord.utils.get(ctx.guild.roles, id = 1010075116354416700)
        team11 = discord.utils.get(ctx.guild.roles, id = 1010075159744495657)
        team12 = discord.utils.get(ctx.guild.roles, id = 1010075196293652550)
        if team1 in ctx.author.roles:
            my_team = 1
        elif team2 in ctx.author.roles:
            my_team = 2
        elif team3 in ctx.author.roles:
            my_team = 3
        elif team4 in ctx.author.roles:
            my_team = 4
        elif team5 in ctx.author.roles:
            my_team = 5
        elif team6 in ctx.author.roles:
            my_team = 6
        elif team7 in ctx.author.roles:
            my_team = 7
        elif team8 in ctx.author.roles:
            my_team = 8
        elif team9 in ctx.author.roles:
            my_team = 9
        elif team10 in ctx.author.roles:
            my_team = 10
        elif team11 in ctx.author.roles:
            my_team = 11
        elif team12 in ctx.author.roles:
            my_team = 12

        dir = db.reference(f'team/{my_team}/currentCapital')
        myCurrentCapital = dir.get()

        await ctx.send(f'{my_team}팀 - 현재 총 자산 {myCurrentCapital}만원입니다.')

@bot.command()
async def set_round(ctx, set_round_num):
    if int(set_round_num) == 1 or int(set_round_num) == 2 or int(set_round_num) == 3:
        dir = db.reference('setting')
        dir.update({'roundNum': int(set_round_num)})
        await ctx.send(f'ICISTS 투자게임 - 현재 {set_round_num}라운드로 설정되었습니다.')
    elif int(set_round_num) == 0:
        dir = db.reference('setting')
        dir.update({'roundNum': int(set_round_num)})
        await ctx.send(f'ICISTS 투자게임 - 현재 {set_round_num}라운드로 설정되었습니다.\nICISTS 투자게임 - 라운드가 진행되고 있지 않습니다.')
    else:
        await ctx.send(f'ICISTS 투자게임 - 올바른 숫자를 입력해주세요.')

@bot.command()
async def calculate_rank(ctx):
    dir_round_num = db.reference('setting/roundNum')
    round_num = dir_round_num.get()
    if round_num == 1:
        first_data = []
        for i in range(1,9):
            dir_firstInvestment = db.reference(f'team/{i}/firstInvestment')
            firstInvestment = dir_firstInvestment.get()
            temp_data = (i, firstInvestment)
            first_data.append(temp_data)
        await ctx.send('ICISTS 투자게임 - 1라운드 투자 결과 데이터를 받아왔습니다.')
        first_data.sort(key = lambda x : x[1], reverse = True)
        await ctx.send('ICISTS 투자게임 - 1라운드 순위 계산이 완료되었습니다.')
        for i in range(1,9):
            team_num = first_data[i-1][0]
            dir_firstRank = db.reference(f'team/{team_num}')
            dir_firstRank.update({'firstRank' : i})
        await ctx.send(f'ICISTS 투자게임 - 1라운드 투자 순위 계산이 완료되었습니다.')
        
    elif round_num == 2:
        second_data = []
        for i in range(1,9):
            dir_secondInvestment = db.reference(f'team/{i}/secondInvestment')
            secondInvestment = dir_secondInvestment.get()
            temp_data = (i, secondInvestment)
            second_data.append(temp_data)
        await ctx.send('ICISTS 투자게임 - 2라운드 투자 결과 데이터를 받아왔습니다.')
        second_data.sort(key = lambda x : x[1], reverse = True)
        await ctx.send('ICISTS 투자게임 - 2라운드 순위 계산이 완료되었습니다.')
        for i in range(1,9):
            team_num = second_data[i-1][0]
            dir_secondRank = db.reference(f'team/{team_num}')
            dir_secondRank.update({'secondRank' : i})
        await ctx.send(f'ICISTS 투자게임 - 2라운드 투자 순위 계산이 완료되었습니다.')

    elif round_num == 3:
        third_data = []
        for i in range(1,9):
            dir_thirdInvestment = db.reference(f'team/{i}/thirdInvestment')
            thirdInvestment = dir_thirdInvestment.get()
            temp_data = (i, thirdInvestment)
            third_data.append(temp_data)
        await ctx.send('ICISTS 투자게임 - 3라운드 투자 결과 데이터를 받아왔습니다.')
        third_data.sort(key = lambda x : x[1], reverse = True)
        await ctx.send('ICISTS 투자게임 - 3라운드 순위 계산이 완료되었습니다.')
        for i in range(1,9):
            team_num = third_data[i-1][0]
            dir_thirdRank = db.reference(f'team/{team_num}')
            dir_thirdRank.update({'thirdRank' : i})
        await ctx.send(f'ICISTS 투자게임 - 3라운드 투자 순위 계산이 완료되었습니다.')

@bot.command()
async def calculate_return(ctx):
    dir_round_num = db.reference('setting/roundNum')
    round_num = dir_round_num.get()
    if round_num == 1:
        for i in range(1,9):
            total_return = 0
            for j in range(1,9):
                dir_investmentData = db.reference(f'round/1/{i}/{j}')
                ij_investment = dir_investmentData.get()
                dir_jRank = db.reference(f'team/{j}/firstRank')
                jRank = dir_jRank.get()
                investment_return = round(ij_investment * rank_ratio(jRank))
                total_return = total_return + investment_return
                await ctx.send(f'ICISTS 투자게임 - {i}팀의 {j}팀에 대한 정산이 완료되었습니다.')
            dir = db.reference(f'team/{i}/currentCapital')
            leftCapital = dir.get()
            firstCapital = leftCapital + total_return
            dir_firstCapital = db.reference(f'team/{i}')
            dir_firstCapital.update({'firstCapital' : int(firstCapital)})

            dir = db.reference(f'team/{i}')
            dir.update({'currentCapital' : int(firstCapital)})
            await ctx.send(f'ICISTS 투자게임 - {i}팀의 투자 정산이 완료되었습니다.\n')
        await ctx.send('ICISTS 투자게임 - 1라운드 정산이 완료되었습니다.')
    elif round_num == 2:
        for i in range(1,9):
            total_return = 0
            for j in range(1,9):
                dir_investmentData = db.reference(f'round/2/{i}/{j}')
                ij_investment = dir_investmentData.get()
                dir_jRank = db.reference(f'team/{j}/secondRank')
                jRank = dir_jRank.get()
                investment_return = ij_investment * rank_ratio(jRank)
                total_return = total_return + investment_return
                await ctx.send(f'ICISTS 투자게임 - {i}팀의 {j}팀에 대한 정산이 완료되었습니다.')
            dir = db.reference(f'team/{i}/currentCapital')
            leftCapital = dir.get()
            secondCapital = leftCapital + total_return
            dir_secondCapital = db.reference(f'team/{i}')
            dir_secondCapital.update({'secondCapital' : int(secondCapital)})

            dir = db.reference(f'team/{i}')
            dir.update({'currentCapital' : int(secondCapital)})
            await ctx.send(f'ICISTS 투자게임 - {i}팀의 투자 정산이 완료되었습니다.\n')
        await ctx.send('ICISTS 투자게임 - 2라운드 정산이 완료되었습니다.')
    elif round_num == 3:
        for i in range(1,9):
            total_return = 0
            for j in range(1,9):
                dir_investmentData = db.reference(f'round/3/{i}/{j}')
                ij_investment = dir_investmentData.get()
                dir_jRank = db.reference(f'team/{j}/thirdRank')
                jRank = dir_jRank.get()
                investment_return = ij_investment * rank_ratio(jRank)
                total_return = total_return + investment_return
                await ctx.send(f'ICISTS 투자게임 - {i}팀의 {j}팀에 대한 정산이 완료되었습니다.')
            dir = db.reference(f'team/{i}/currentCapital')
            leftCapital = dir.get()
            thirdCapital = leftCapital + total_return
            dir_thirdCapital = db.reference(f'team/{i}')
            dir_thirdCapital.update({'thirdCapital' : int(thirdCapital)})

            dir = db.reference(f'team/{i}')
            dir.update({'currentCapital' : int(thirdCapital)})
            await ctx.send(f'ICISTS 투자게임 - {i}팀의 투자 정산이 완료되었습니다.\n')
        await ctx.send('ICISTS 투자게임 - 3라운드 정산이 완료되었습니다.')

@bot.command()
async def calculate_final(ctx):
    dir_round_num = db.reference('setting/roundNum')
    round_num = dir_round_num.get()
    if round_num < 3:
        await ctx.send('ICISTS 투자게임 - 아직 투자게임이 종료되지 않았습니다.')
    elif round_num == 3:
        totalCapital_data = []
        for i in range(1,9):
            dir_totalInvestment = db.reference(f'team/{i}/totalInvestment')
            totalInvestment = dir_totalInvestment.get()
            dir_totalCapital = db.reference(f'team/{i}/thirdInvestment')
            totalCapital = dir_totalCapital.get()
            totalMoney = int(totalInvestment) + int(totalCapital)
            temp_data = (i, totalMoney)
            totalCapital_data.append(temp_data)
        await ctx.send('ICISTS 투자게임 - 최종 투자 결과 데이터를 받아왔습니다.')
        totalCapital_data.sort(key = lambda x : x[1], reverse = True)
        await ctx.send('ICISTS 투자게임 - 최종 순위 계산이 완료되었습니다.')
        for i in range(1,4):
            dir_finalCapital = db.reference('result/capital')
            dir_finalCapital.update({f'{i}' : totalCapital_data[i-1][0]})
        await ctx.send(f'ICISTS 투자게임 - 최종 순위 계산이 완료되었습니다.')

@bot.command()
async def default_firebase_test(ctx):
    dir.update({'test':'Hello World'})
    await ctx.send('ICISTS 투자게임 - Firebase 테스트가 완료되었습니다.')

@bot.command()
async def default_firebase_setting(ctx):
    dir = db.reference()
    dir.update({'setting':{
        'defaultMoney' : 10000,
        'roundNum' : 0
    }})
    await ctx.send('ICISTS 투자게임 - Firebase 초기 변수 설정이 완료되었습니다.')

@bot.command()
async def default_firebase_start(ctx):
    dir_defaultMoney = db.reference('setting/defaultMoney')
    default_money = dir_defaultMoney.get()
    await ctx.send('ICISTS 투자게임 - Firebase 데이터베이스 설정을 시작합니다.\n')
    dir = db.reference('team')
    for i in range(1,9):
        dir.update(
            {f'{i}' : 
            {
                'currentCapital' : int(default_money),
                'firstCapital' : 0,
                'secondCapital' : 0,
                'thirdCapital' : 0,
                'firstInvestment' : 0,
                'secondInvestment' : 0,
                'thirdInvestment' : 0,
                'totalInvestment' : 0,
                'firstRank' : 0,
                'secondRank' : 0,
                'thirdRank' : 0
            }
        })
        await ctx.send(f'ICISTS 투자게임 - {i}팀의 데이터 초기화 완료.')
    await ctx.send('ICISTS 투자게임 - 팀별 데이터 초기화 완료.\n')
    for i in range(1,4):
        for j in range(1,9):
            for k in range(1,9):
                dir = db.reference(f'round/{i}/{j}')
                dir.update({
                    f'{k}' : 0
                    })
            await ctx.send(f'ICISTS 투자게임 - {i} 라운드 | {j}팀의 투자 데이터 초기화 완료.')
        await ctx.send(f'ICISTS 투자게임 - {i}라운드 데이터 초기화 완료.\n')
    await ctx.send('ICISTS 투자게임 - 투자 데이터 초기화 완료.\n')
    dir = db.reference('result')
    dir.update(
        {'investment' : 
            {
                '1' : 0,
                '2' : 0,
                '3' : 0
            },
            'capital' :
            {
                '1' : 0,
                '2' : 0,
                '3' : 0
            }
        })
    await ctx.send('ICISTS 투자게임 - 최종 결과 데이터 초기화 완료.')
    await ctx.send('ICISTS 투자게임 - Firebase 초기 데이터베이스 설정이 완료되었습니다.')

bot.run(os.environ['token'])