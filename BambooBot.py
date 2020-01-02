

#내 계정(댕댕이) id == 169596780579782658
'''
TODO 대신 전해드립니다봇

'''
import os
import asyncio
import discord
from discord.utils import get

client = discord.Client()

#전역변수선언
adminID = "169596780579782658" #내 계정 id
generalID = "None" #제네럴 ID를 입력받으세요
generalName = "None" #제네럴 ID를 받고, 제네럴 이름을 알아내여 대입하기
setupRoute = "BambooBotsetup.txt"
#접두사 = k!
chatLogList = []
logSize = 200 #로그의 크기는 최대 얼마
isUtilOnline = False
isGeneralInput = False
banList = []

class BanUser :
    def __init__(self, id):
        self.id = id
        self.banTime = int(time.time())
        self.banChatCount = 50
class chatLog :
    def __init__(self, id, name, chat) :
        self.id = id
        self.name = name
        self.chat = chat

#startSetUp
@client.event
async def on_ready():
    print("Logged in as ") #봇의 id, 닉네임 출력
    print(client.user.name)
    print(client.user.id)
    print("===========")
    #현재 플레이중인 게임 표시 -> !help 등으로 설정할 것
    await client.change_presence(game=discord.Game(name="type k!help", type=1))
    global generalID, generalName, isGeneralInput
    #봇이 시작했음을 알림
    try :
        with open(setupRoute, mode="r", encoding="utf-8") as f :
            setup = f.readlines()
        # f.write("True\n%s\n%s" %(generalName,generalID))
        if setup[0].split("\n")[0] == "True" :
            isGeneralInput = True
            generalName = setup[1].split("\n")[0]
            print(generalName)
            generalID = setup[2].split("\n")[0]
    except FileNotFoundError as e :
        print(e)
        isGeneralInput = False
    '''if generalID != "None" :
        await client.send_message(discord.Object(id=generalID), "짜잔! 봇이 돌아왔어요!")'''

# 봇이 새로운 메시지를 수신했을때 동작
@client.event
async def on_message(message):
    if message.author.bot: #봇체크 = 봇이 메세지를 보낸 경우 무시함
        return None
    #TODO 전역변수가 추가되면 이곳에도 추가할 것
    global chatLogList, isUtilOnline, generalID, generalName, isGeneralInput, banList, chatLog
    userID = message.author.id  #id == 메세지를 보낸사람의 ID (str (예시 = 283788425264365569))
    channelID = message.channel   #channelID == 메세지를 받은 채널의 ID (채널 이름)

    # 내 계정(댕댕이) id == 169596780579782658
    # 내 계정 id 변수명 == adminID

    ##########################################################################################
    #TODO 대신 전해드립니다 기능 보완하기
    if message.channel.is_private :
        try : #TODO 관리자 권한 확인하기 / 혹은 나인지 확인하기
            if userID==adminID:
                if message.content.startswith("k!show") :
                    #TODO log파일 보여주기 -> 검색해서 보여주기 또는 숫자로 보여주기?
                    # 파일로 오픈해서 저장하던 것을 변수로만 저장하는 것으로 수정하기
                    searchText = message.content[7:]
                    for i in range(len(chatLogList) - 1, -1, -1) :
                        if searchText in chatLogList[i].chat or searchText in chatLogList[i].id or \
                                searchText in chatLogList[i].name:
                            await client.send_message(channelID, "User = %s // ID = %s\n%s"%(
                            chatLogList[i].name,chatLogList[i].id, chatLogList[i].chat))
                    return
                if message.content.startswith("k!id"):
                    searchText = message.content[5:]
                    searchUser = await client.get_user_info(searchText)
                    await client.send_message(channelID, searchUser.name)
                    return
                if message.content.startswith("k!"):
                    await client.send_message(channelID, "커맨드는 k!help를 제외하고\n여기서 동작할 수 없습니다.")
                    return
                if message.content.startswith("!"):
                    await client.send_message(channelID, "커맨드는 k!help를 제외하고\n여기서 동작할 수 없습니다.")
                    return
            if isUtilOnline :
                for i in range(len(banList)):
                    if userID == banList[i].id:
                        await client.send_message(channelID, "귀하는 일정시간 유동계정 사용이 불가능합니다.")
                        return
                user = await client.get_user_info(userID)
                userName = user.name
                if len(chatLogList) > logSize : #선언부 명시 : 디폴트 200줄까지
                    while len(chatLogList) > logSize :
                        del chatLogList[0]
                for i in range(len(banList)):
                    banList[i].banChatCount -= 1
                    if banList[i].banChatCount < 0:
                        del banList[i]
                if message.content.startswith("http") :
                    await client.send_message(channelID, "http링크는 송신할 수 없습니다.")
                    return
                chatLogList.append(chatLog(name=userName, id=userID, chat=message.content))
                await client.send_message(discord.Object(id=generalID), message.content)
            else:
                await client.send_message(channelID, "현재 기능이 꺼져 있습니다. 관리자에게 문의하세요")
            return
        except discord.errors.HTTPException as e :
            #이미지 송신 시
            await client.send_message(channelID, "이미지는 송신할 수 없습니다.")
            return
        except Exception as e:
            dmAdmin = await client.get_user_info(adminID)
            await client.send_message(dmAdmin, e.__str__())
            print(e.__str__())
            return

    #대략 200줄마다 리셋하게 동작 -> 데이터 아끼기

    ##################################################################
    ##################################################################
    else :
        #################################################3
        # TODO k!help 추가하기
        # dm으로 명령어 보내주기
        # 나에게는 비밀 커맨드도 같이 보내줄 것
        if message.content == "k!help":
            embed = discord.Embed(title="BamBooBot이 대신 전해드립니다!", color=0xFFC4FF)
            if isGeneralInput:
                embed.description = ("BambooBot에게 DM을 보내면\n%s채널에 전달됩니다\n\n" % (generalName)
                                     + "봇 제작자는 KongKaChu입니다."
                                     + "\n 절하 쉽 sio Human...\n"
                                     + "봇 제작에 큰 도움을 주신 gosmajunior 님에게\n"
                                     + "진심으로 감사를 표합니다.")
                if message.author.server_permissions.administrator:
                    embed.description += ("\n\n관리자용 특별 커맨드입니다.\n\n"
                                          + "k!start\n"
                                          + "유동계정을 활성화합니다.\n\n"
                                          + "k!stop\n"
                                          + "유동계정을 활성화합니다.\n\n"
                                          + "k!ban 채팅내용\n"
                                          + "해당채팅을 사용한 유저를\n10분가량 기능 이용을 막습니다.\n"
                                          + "**꼭 내용을 정확하게 입력해주세요**\n"
                                          + "복붙을 하세요 차라리\n\n"
                                          )
                    if userID == adminID:  # TODO 기능 추가될 때마다 커맨드 적어놓기
                        embed.description += ("\n\n콩카츄용 특별 커맨드입니다.\n\n"
                                              + "k!show 검색할 메세지 또는 id, 유저 이름\n"
                                              + "로그에서 유동계정을 이용한 자를 검색합니다.\n"
                                              + "DM채널에서만 작동합니다.\n\n"
                                              + "k!id id번호\n"
                                              + "id를 통해 유저의 이름을 알아냅니다. DM채널에서만 작동합니다.\n\n"
                                              )
            else:
                embed.description = ("BambooBot은 제네럴 ID를 입력해야 작동됩니다."
                                     + "\n익명봇을 사용할 채널에서 k!set general을 입력해"
                                     + "\n봇을 사용할 채널을 설정하세요")
            dmUser = await client.get_user_info(userID)
            await client.send_message(dmUser, embed=embed)
            return
    ############
        #TODO 커맨드 추가하기
        ####################################################
        #제네럴 설정하기
        if message.content == "k!set general" :
            if message.author.server_permissions.administrator:
                generalName = channelID
                generalID = channelID.id
                isGeneralInput = True
                with open(setupRoute, mode="w", encoding="utf-8") as f :
                    f.write("True\n%s\n%s" %(generalName,generalID))
                return
            else :
                client.send_message(channelID, "권한이 없습니다. 관리자에게 문의하세요")
                return
        #####################################################################
        #밴 기능
        if message.content.startswith("k!ban") :
            if userID == adminID or message.author.server_permissions.administrator:
                try :
                    searchText = message.content[6:]
                    #TODO ban검색도 바꿔주기
                    for i in range(len(chatLogList) - 1, -1, -1) :
                        if searchText in chatLogList[i].chat :
                            banList.append(BanUser(id=chatLogList[i].id))
                            print(chatLogList[i].name)
                    await client.send_message(channelID, "밴 겁니다 수고링 옥토링 잉클링~")
                except Exception as e:
                    print(e)
                    await client.send_message(channelID, "ERRORcode : indexError")
            else :
                await client.send_message(channelID, "권한이 없습니다.")
            return
        #####################################################################
        # 대신 전해드립니다 시작
        if message.content == "k!start":
            if message.author.server_permissions.administrator:
                isUtilOnline = True
                await client.send_message(discord.Object(id=generalID), "유동계정이 활성화됩니다.")
            else:
                client.send_message(channelID, "권한이 없습니다. 관리자에게 문의하세요")
            return
        # 대신 전해드립니다 멈추기
        if message.content == "k!stop":
            if message.author.server_permissions.administrator:
                isUtilOnline = False
                await client.send_message(discord.Object(id=generalID), "유동계정이 비활성화됩니다.")
            else:
                client.send_message(channelID, "권한이 없습니다. 관리자에게 문의하세요")
            return
        ############################################################################################
        #TODO 셀프 이모지 추가하기
        if message.content == "뉴비에오~와우" :
            if adminID==userID :
                await client.send_file(destination=channelID, fp="noob.png")
                return
        if message.content == "오와우~!" :
            if adminID == userID:
                await client.send_file(destination=channelID, fp="OhWow.png")
                return
        if message.content == "우워우..." :
            if adminID == userID:
                await client.send_file(destination=channelID, fp="UhWah.png")
                return
        ###########################################################################################
access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
