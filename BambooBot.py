import asyncio
import discord
from discord.utils import get
import os

client = discord.Client()
#전역변수선언
adminID = "" #내 계정 id


@client.event
async def on_ready():
    print("Logged in as ") #봇의 id, 닉네임 출력
    print(client.user.name)
    print(client.user.id)
    print("===========")
    #현재 플레이중인 게임 표시 -> k!help 등으로 설정할 것
    await client.change_presence(game=discord.Game(name="이카 요로시쿠~", type=1))
    dmUser = await client.get_user_info(adminID)
    await client.send_message(dmUser, "봇 온라인이에요!")
# 봇이 새로운 메시지를 수신했을때 동작
@client.event
async def on_message(message):
    userID = message.author.id  #id == 메세지를 보낸사람의 ID (str 35890358)
    channelID = message.channel
    if message.author.bot: #봇체크 = 봇이 메세지를 보낸 경우 무시함
        return None
    if message.content == "(뉴비에오 콘)" or message.content == "뉴비에오~와우" :
        await client.send_file(destination=channelID, fp="noob.png")
        return
    if message.content == "(오와우 콘)" or message.content == "오와우~!":
        await client.send_file(destination=channelID, fp="OhWow.png")
        return
    if message.content == "(우워우 콘)" or message.content == "우워우...":
        await client.send_file(destination=channelID, fp="UhWah.png")
        return
    if message.content == "즐겁다":
        await client.send_file(destination=channelID, fp="Tanoshi.png")
        return
    if message.content == "골-든 즐겁다" :
        await client.send_file(destination=channelID, fp="Golden_Tanoshi.png")
        return
    if message.content == "안녕하다":
        await client.send_file(destination=channelID, fp="Hi.png")
        return
    if message.content == "받아치다":
        await client.send_file(destination=channelID, fp="ReturnHi.png")
        return
        ############################################################################################
        #TODO 셀프 이모지 추가하기
        
        ###########################################################################################
access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
