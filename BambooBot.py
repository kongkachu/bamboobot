import asyncio
import discord
from discord.utils import get
import time
import os

client = discord.Client()
#전역변수선언
adminID = "169596780579782658" #내 계정 id
setupRoute = "BambooBotsetup.txt"
#접두사 = k!
chatLogList = []
messageRangeWarning = 300
logSize = 200 #로그의 크기는 최대 얼마
isUtilOnline = True
isGeneralInput = False
banList = []
chatLimitUsers=[]

setup = None #bambooBot setup을 받기위한 전역변수
class BotSetup:
    def __init__(self, generalID, generalName, messageLimitMinute=10, messageLimitCount=5, messageRangeWarning=300):
        self.generalID = generalID
        self.generalName = generalName
        self.messageRangeWarning = messageRangeWarning
        self.messageLimitMinute = messageLimitMinute
        self.messageLimitCount = messageLimitCount
        #(messageLimitMinute)분 이내로 (messageLimitCount)개 초과의 메세지를 보낼 수 없다
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
class chatLimit :
    def __init__(self, id, messageLimitMinute, messageLimitCount) :
        self.id = id
        self.messageLimit = messageLimitMinute * 60
        self.messageLimitCount = messageLimitCount
        self.limitList = []
    def addLimit(self): #정상추가시 return False
        sendTime = int(time.time())
        if len(self.limitList) != 0 :
            while(True) :
                if len(self.limitList) != 0:
                    if self.limitList[0] + (self.messageLimit) < sendTime :
                        del self.limitList[0]
                        continue
                    else :
                        break
                else :
                    break
        if len(self.limitList) >= self.messageLimitCount:
            return False #리미트에 걸리면 False를 반환
        self.limitList.append(sendTime)
        return True #정상실행시 True
def fileInput() :
    global setup, setupRoute
    with open(setupRoute, mode="w", encoding="utf-8") as f:
        f.write("generalName=%s\n" % (setup.generalName))
        f.write("generalID=%s\n" % (setup.generalID))
        f.write("messageRangeWarning=%d\n" % (setup.messageRangeWarning))
        f.write("messageLimitMinute=%d\n" % (setup.messageLimitMinute))
        f.write("messageLimitCount=%d\n" % (setup.messageLimitCount))
#startSetUp
@client.event
async def on_ready():
    print("Logged in as ") #봇의 id, 닉네임 출력
    print(client.user.name)
    print(client.user.id)
    print("===========")
    #현재 플레이중인 게임 표시 -> k!help 등으로 설정할 것
    await client.change_presence(game=discord.Game(name="type k!help", type=1))
    global isGeneralInput, setup, chatLimitUsers
    #봇이 시작했음을 알림
    try :
        with open(setupRoute, mode="r", encoding="utf-8") as f :
            readedSetup = f.readlines()
            for i in range(len(readedSetup)) :
                readedSetup[i] = readedSetup[i].split("=")[1].split("\n")[0] #\n, = 떼어내기
            '''
            setup
            
            channelName=        #setup StartLIne == readedSetup[0]
            channelID=
            messageRangeWarning=               
            messageLimitMinute=
            messageLimitCount=
            
            '''
            if readedSetup[2] == "" :
                readedSetup[2] = "300"
            readedSetup[2] = int(readedSetup[2]) # messageRangeWarning

            if readedSetup[3] == "":
                readedSetup[3] = "10"
            readedSetup[3] = int(readedSetup[3]) # messageLimitMinute

            if readedSetup[4] == "" :
                readedSetup[4] = "5"
            readedSetup[4] = int(readedSetup[4]) # messageLimitCount

            set_generalName = readedSetup[0]
            set_generalID = readedSetup[1]
            set_messageRangeWarning = readedSetup[2]
            set_messageLimitMinute = readedSetup[3]
            set_messageLimitCount = readedSetup[4]
            setup = BotSetup(generalID=set_generalID,
                             generalName=set_generalName,
                             messageRangeWarning=set_messageRangeWarning,
                             messageLimitMinute=set_messageLimitMinute,
                             messageLimitCount=set_messageLimitCount)
        isGeneralInput = True
    except Exception as e :
        print(e)
        isGeneralInput = False
        setup = BotSetup(
                        generalName="generalName",
                        generalID="generalID",
                        )
    dmUser = await client.get_user_info(adminID)
    await client.send_message(dmUser, "주인님, 제가 돌아왔어요!")
# 봇이 새로운 메시지를 수신했을때 동작
@client.event
async def on_message(message):
    if message.author.bot: #봇체크 = 봇이 메세지를 보낸 경우 무시함
        return None

    #TODO 전역변수가 추가되면 이곳에도 추가할 것
    global chatLogList, isUtilOnline, isGeneralInput, banList, chatLog, setup
    userID = message.author.id  #id == 메세지를 보낸사람의 ID (str 35890358)
    channelID = message.channel   #channelID == 메세지를 받은 채널의 ID (채널 이름)

    # 내 계정(댕댕이) id == 169596780579782658
    # 내 계정 id 변수명 == adminID

    ##########################################################################################
    #TODO 대신 전해드립니다 기능 보완하기
    # k!ban 오류 해결하기
    if message.channel.is_private :
        try : #TODO 관리자 권한 확인하기 / 혹은 나인지 확인하기
            if userID==adminID:
                if message.content.startswith("k!search") :
                    #TODO log파일 보여주기 -> 검색해서 보여주기 또는 숫자로 보여주기?
                    # 파일로 오픈해서 저장하던 것을 변수로만 저장하는 것으로 수정하기
                    searchText = message.content[9:]
                    for i in range(len(chatLogList)) :
                        if searchText in chatLogList[i].chat or searchText in chatLogList[i].id or \
                                searchText in chatLogList[i].name:
                            await client.send_message(channelID, "User = %s // ID = %s"%(
                            chatLogList[i].name,chatLogList[i].id))
                            await client.send_message(channelID, chatLogList[i].chat)
                    return
                if message.content.startswith("k!show"): #TODO log 갯수 받아서 출력하는 메소드
                    try :
                        showCount = int(message.content[7:])
                        for i in range(showCount) :
                            await client.send_message(channelID, "User = %s // ID = %s" % (
                                chatLogList[i].name, chatLogList[i].id))
                            await client.send_message(channelID, chatLogList[i].chat)
                    except Exception as e:
                        await client.send_message(channelID, e.__str__())
                    return
                if message.content == "k!info" :
                    await client.send_message(channelID, "generalName = %s\n"
                                                         "generalID = %s\n"
                                                         "글자수 경고 = %s자\n"
                                                         "메세지 제한 = %d분 내로 %d개까지\n" #TODO 분인지 초인지 확실히 할 것
                                                         "현 사용자 수 = %d\n"
                                                         "" %(
                                                              setup.generalName,
                                                              setup.generalID,
                                                              setup.messageRangeWarning,
                                                              setup.messageLimitMinute,
                                                              setup.messageLimitCount,
                                                              len(chatLogList),
                                                              ))
                    return
                if message.content.startswith("k!id"):
                    searchText = message.content[5:]
                    searchUser = await client.get_user_info(searchText)
                    await client.send_message(channelID, searchUser.name)
                    return
                if message.content.startswith("k!"):
                    await client.send_message(channelID, "커맨드는 여기서 동작할 수 없습니다.")
                    return
                if message.content.startswith("!"):
                    await client.send_message(channelID, "커맨드는 여기서 동작할 수 없습니다.")
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
                #chatLimit 체크
                if len(chatLimitUsers) == 0:
                    chatLimitUsers.append(chatLimit(id=userID,messageLimitCount=setup.messageLimitCount,messageLimitMinute=setup.messageLimitMinute))
                for i in range(len(chatLimitUsers)):
                    if chatLimitUsers[i].id == userID:
                        if not chatLimitUsers[i].addLimit():
                            await client.send_message(channelID, "채팅이 너무 잦습니다!\n잠시 후에 시도해주세요.")
                            return
                    else :
                        chatLimitUsers.append(chatLimit(id=userID, messageLimitCount=setup.messageLimitCount,
                                                        messageLimitMinute=setup.messageLimitMinute))

                if len(message.content) > setup.messageRangeWarning: #디폴트 300
                    dmUser = await client.get_user_info(adminID)
                    await client.send_message(dmUser, message.content)
                    await client.send_message(dmUser, userID)
                #최종송신
                chatLogList.append(chatLog(name=userName, id=userID, chat=message.content))
                await client.send_message(discord.Object(id=setup.generalID), message.content)
            else:
                await client.send_message(channelID, "현재 기능이 꺼져 있습니다. 관리자에게 문의하세요")
            return
        except discord.errors.HTTPException as e :
            if userID == adminID :
                dmAdmin = await client.get_user_info(adminID)
                await client.send_message(dmAdmin, e.__str__())
                await client.send_message(dmAdmin, "대신 전해주기 기능")
            print(e.__str__())
            await client.send_message(channelID, "이미지는 송신할 수 없습니다.")
            dmAdmin = await client.get_user_info(adminID)
            await client.send_message(dmAdmin, "대신 전해주기 HTTPexception의 오류 내역")
            await client.send_message(dmAdmin, e.__str__())
            return
        except Exception as e:
            dmAdmin = await client.get_user_info(adminID)
            await client.send_message(dmAdmin, "HTTPexception 외 대신 전해주기 기능")
            await client.send_message(dmAdmin, e.__str__())
            print(e.__str__())
            return

    #대략 200줄마다 리셋하게 동작 -> 데이터 아끼기

    ##################################################################
    ##################################################################
    else :
        #################################################3
        if message.content == "k!help":
            embed = discord.Embed(title="BamBooBot이 대신 전해드립니다!", color=0xFFC4FF)
            if isGeneralInput:
                embed.description = ("BambooBot에게 DM을 보내면\n%s채널에 전달됩니다\n\n" % (setup.generalName)
                                     + "봇 제작자는 KongKaChu입니다."
                                     + "\n 절하 쉽 sio Human...\n"
                                     + "봇 제작에 큰 도움을 주신 gosmajunior 님과\n"
                                     + "Mien 님에게 진심으로 감사를 표합니다.\n\n"
                                     + "(오와우 콘)\n"
                                     + "오와우~!\n"
                                     + "(우워우 콘)\n"
                                     + "우워우...\n"
                                     + "(뉴비에오 콘)\n"
                                     + "뉴비에오~와우\n"
                                     + "이상 셀프 이모지 커맨드입니다.\n")
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
                                              + "k!info\n"
                                              + "현재 setup파일을 보여줍니다.\n"
                                              + "k!search 검색할 메세지 또는 id, 유저 이름\n"
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
        #TODO k!set ~ 명령어들 싹다 만들기
        # 명령어 사용시 나한테 DM하기
        # help에도 추가할 것
        # todo 추가된 k!set 명령어들 추가할 것
        '''
        generalName=대나무숲-chamber
        generalID=661797881723748403
        messageRangeWarning=
        messageLimitMinute=
        messageLimitCount=
        '''
        if message.content == "k!set general" :
            if userID == adminID :
                setup.generalName = channelID
                setup.generalID = channelID.id
                isGeneralInput = True
                fileInput()
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
                    findText = False
                    for i in range(len(chatLogList) - 1, -1, -1) :
                        if searchText in chatLogList[i].chat :
                            banList.append(BanUser(id=chatLogList[i].id))
                            print(chatLogList[i].name)
                            findText = True
                    if findText :
                        await client.send_message(channelID, "밴 겁니다 수고링 옥토링 잉클링~")
                    else :
                        await client.send_message(channelID, "해당 채팅 내용을 찾지 못했습니다.")
                except Exception as e:
                    dmUser = await client.get_user_info(adminID)
                    await client.send_message(dmUser, userID)
                    await client.send_message(dmUser, e.__str__())
                    await client.send_message(dmUser, "밴을 시도하는 유저 = % schatlog list 수 = %d\n이하 밴하려는 채팅 내용"%(userID,len(chatLogList)))
                    await client.send_message(dmUser, searchText)

            else :
                await client.send_message(channelID, "권한이 없습니다.")
            return
        #####################################################################
        #TODO 명령어 사용시 나에게 DM

        # 대신 전해드립니다 시작
        if message.content == "k!start":
            if message.author.server_permissions.administrator:
                isUtilOnline = True
                await client.send_message(discord.Object(id=setup.generalID), "유동계정이 활성화됩니다.")
            else:
                client.send_message(channelID, "권한이 없습니다. 관리자에게 문의하세요")
            return
        # 대신 전해드립니다 멈추기
        if message.content == "k!stop":
            if message.author.server_permissions.administrator:
                isUtilOnline = False
                await client.send_message(discord.Object(id=setup.generalID), "유동계정이 비활성화됩니다.")
            else:
                client.send_message(channelID, "권한이 없습니다. 관리자에게 문의하세요")
            return
        ############################################################################################
        #TODO 셀프 이모지 추가하기
        if message.content == "(뉴비에오 콘)" or message.content == "뉴비에오~와우" :
            await client.send_file(destination=channelID, fp="noob.png")
            return
        if message.content == "(오와우 콘)" or message.content == "오와우~!":
            await client.send_file(destination=channelID, fp="OhWow.png")
            return
        if message.content == "(우워우 콘)" or message.content == "우워우...":
            await client.send_file(destination=channelID, fp="UhWah.png")
            return
        ###########################################################################################
        #TODO elo rating 모듈 추가하기
        ##########################################################################################
access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
