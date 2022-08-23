import discord
from discord.ext import commands
import datetime
from discord.ext import commands
from discord.utils import get
from replit import db
import json
import random
import time
import sys
import os
import asyncio
import math
from core.classes import Cog_Extension

def exp_up(exp:int,lv:int,add:int):
  exp += add
  if((exp/lv)>100):
    exp -= lv*100
    lv += 1
  return(exp,lv)


def read_file(name:str):
    return db[name]

def write_file(name:str,file_name):
    db[name] = file_name

def get_user(id:str):
    Users_data = db["User"]
    return dict(Users_data[id])

def put_user(id:str,User_data:dict):
    Users_data = db["User"]
    Users_data[id] = User_data
    db["User"] = Users_data
    #print(db["User"])

def check_user(id:str):
    Users_data = db["User"]
    flag = 0
    for i in Users_data.keys():
        if(i==id):
            flag = 1
            return 1
            break
    if(flag == 0):
        return 0

def move_file(file_name:str):
    with open(file_name+".json","r",encoding="utf-8")as f:
        XX = json.load(f)
        return XX

datetime_now = datetime.datetime.now()
time_range = datetime.timedelta(hours = 8)
new_time = datetime_now+time_range
class Common(Cog_Extension):
    #change yet
    @commands.command() #註冊
    async def 註冊(self,message):
        ID = str(message.author.id)
        if(check_user(ID)):
            await message.channel.send('<@'+ID+'>您已經註冊過啦<:mumi05:897429782529212436> ')
        else:
            mydict = {
                'UserID': message.author.id,
                'Username': message.author.name,
                'point': 1000,
                'assistant': 0,
                'card': '',
                're': 0,
                'new': '2.1.1',
                'specialchange': 0,
                'pis': 0,
                'key': 0,
                'box': 0,
                "bag1":"",
                "bag2":"",
                "bag3":"",
                "bag4" :"",
                "bag5": "",
                "level":1,
                "experience" :0,
                "money":"",
                "activity":"",
                "stone": 0,
                "role1":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                "now_role":1,
                "m_pass":0,
                "arms":{"1":[0,0,0,0,0],"2":[0,0,0,0,0],"3":[0,0,0,0,0],"4":[0,0,0,0,0],"5":[0,0,0,0,0],"6":[0,0,0,0,0],"7":[0,0,0,0,0],"8":[0,0,0,0,0],"9":[0,0,0,0,0],"10":[0,0,0,0,0]}
            }
            #write file
            put_user(ID,mydict)
            await message.channel.send('<@'+str(message.author.id)+'>註冊成功<:mumi01:897429705832169512> ')

            #備份用戶資料
            channel = self.bot.get_channel(740946306851143790)
            tsend = str(mydict)
            i_range = math.ceil(len(tsend)/1900) 
            for i in range(i_range):
                await channel.send("```" + tsend[(i*1900):(i+1)*1900] + "```")
            ###
    
    #data.json for com
    #change yet
    @commands.command()   #我的資訊
    async def 資訊總覽(self,message):
        ID = str(message.author.id)
        if check_user(ID):
            t = get_user(ID)
            coin = t['point']
            cc = t['re']
            ss = t['card']
            s = t['card']
            ver = t["new"]
            assistant = t['assistant']
            pis = t['pis']
            showname = '無'
            link = 't'
            title_str = "如需查看指令集，請輸入help_mumi"
            filename = "data.json"
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                Anumber = int(assistant) - (2000 + 1)
            if (int(assistant) == 0):
                pass
            else:
                showname = data["card"][Anumber]
                link = data["link"][Anumber]
            if("experience" in str(t)):
                level = t["level"]
                exp = t["experience"]
                if(level == ""):
                    level = 0
                if(exp == ""):
                    exp = 0
                title_str = "等級："+str(level)+"(exp:"+str(exp)+")"
            embed = discord.Embed(title=str(message.author.name) + "帳號資訊",description=title_str,color=0xeee657)
            embed.set_thumbnail(url=message.author.avatar_url)
            embed.add_field(name="姆咪幣", value=coin, inline=False)
            embed.add_field(name="交換點數", value=cc, inline=False)
            embed.add_field(name="金幣", value=pis, inline=False)
            embed.add_field(name="助手", value=showname, inline=False)
            embed.set_footer(text="@mumi_bot 2019 Version "+ver+" by:Ststone")
            if (link == 't'):
                pass
            else:
                if(int(assistant)==2126):#stevetk
                  member = self.bot.get_guild(782593702455279616).get_member(480747560793931778)
                  embed.set_image(url=member.avatar_url)
                elif(int(assistant)==2125):#Ststone
                  member = self.bot.get_guild(782593702455279616).get_member(550907252970749952)
                  embed.set_image(url=member.avatar_url)
                elif(int(assistant)==2128):#koyoto
                  member = self.bot.get_guild(609019622162825216).get_member(597692502346301452)
                  embed.set_image(url=member.avatar_url)
                else:
                  embed.set_image(url=link)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send('<@'+str(message.author.id)+'>請先輸入\"註冊\"完成註冊<:mumi:897429663549390868>')

    #change yet
    @commands.command()   #我的資訊
    async def 卡片總覽(self,message):
            ID = str(message.author.id)
            if (check_user(ID)):
                t = get_user(ID)
                ss = t['card']
                s = t['card']
                title=""
                shows = '卡片：\n'
                embed = discord.Embed(title="卡片總覽",description="請選擇系列",color=0xeee657,inline=False)
                embed.add_field(name="🇦", value="普通卡片",inline=False)
                embed.add_field(name="🇧", value="re:從零開始的異世界生活、五等分的新娘、不起眼女主角培育法",inline=False)
                embed.add_field(name="🇨", value="為美好的世界獻上祝福！、我們真的學不來！、請問您今天要來點兔子嗎？",inline=False)
                embed.add_field(name="🇩", value="戰鬥女子學園",inline=False)
                embed.add_field(name="🇪", value="約會大作戰、輝夜姬想讓人告白～天才們的戀愛頭腦戰～、歡迎來到實力至上主義的教室",inline=False)
                embed.add_field(name="🇫", value="hololive",inline=False)
                msg1 = await message.channel.send(embed=embed)
                await msg1.add_reaction("🇦")
                await msg1.add_reaction("🇧")
                await msg1.add_reaction("🇨")
                await msg1.add_reaction("🇩")
                await msg1.add_reaction("🇪")
                await msg1.add_reaction("🇫")
                def check(reaction, user):
                    return user == message.author
                try:
                    reaction,user = await self.bot.wait_for('reaction_add', timeout=30, check=check)
                except asyncio.TimeoutError:
                    await message.channel.send("使用者回應逾時")
                    return
                else:
                    await msg1.delete()
                    filename = "data.json"
                    with open(filename, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                    if(str(reaction.emoji) == '🇦'):
                        title = "普通卡片"
                        if ("1001" in ss):
                            addr = "01.村長,"
                            shows = str(shows) + str(addr)
                        if ("1002" in ss):
                            addr = "02.神父,"
                            shows = str(shows) + str(addr)
                        if ("1003" in ss):
                            addr = "03.江湖郎中,"
                            shows = str(shows) + str(addr)
                        if ("1004" in ss):
                            addr = "04.教員,"
                            shows = str(shows) + str(addr)
                        if ("1005" in ss):
                            addr = "05.麵包師傅,"
                            shows = str(shows) + str(addr)
                        if ("1006" in ss):
                            addr = "06.理髮師,"
                            shows = str(shows) + str(addr)
                        if ("1007" in ss):
                            addr = "07.司法官,"
                            shows = str(shows) + str(addr)
                        if ("1008" in ss):
                            addr = "08.酒吧老闆,"
                            shows = str(shows) + str(addr)
                        if ("1009" in ss):
                            addr = "09.城堡主人,"
                            shows = str(shows) + str(addr)
                        if ("1010" in ss):
                            addr = "10.流浪漢,"
                            shows = str(shows) + str(addr)
                    elif(str(reaction.emoji) == '🇧'):
                        title = "re:從零開始的異世界生活、五等分的新娘、不起眼女主角培育法"
                        round = 2001
                        while (round < 2015):
                            if (str(round) in s):
                                Snumber = int(round) - (2000)
                                Anumber = int(round) - (2000 + 1)
                                addname = data["card"][Anumber]
                                if (Snumber < 10):
                                    addno = "00"
                                else:
                                    addno = "0"
                                addr = addno + str(Snumber) + "." + addname + ','
                                shows = str(shows) + str(addr)
                            round = round + 1
                    elif(str(reaction.emoji) == '🇨'):
                        title = "為美好的世界獻上祝福！、我們真的學不來！、請問您今天要來點兔子嗎？"
                        round = 2015
                        while (round < 2040):
                            if (str(round) in s):
                                Snumber = int(round) - (2000)
                                Anumber = int(round) - (2000 + 1)
                                addname = data["card"][Anumber]
                                if (Snumber < 10):
                                    addno = "00"
                                else:
                                    addno = "0"
                                addr = addno + str(Snumber) + "." + addname + ','
                                shows = str(shows) + str(addr)
                            round = round + 1
                    elif(str(reaction.emoji) == '🇩'):
                            title = "戰鬥女子學園"
                            round = 2040
                            while (round < 2059):
                                  if (str(round) in s):
                                        Snumber = int(round) - (2000)
                                        Anumber = int(round) - (2000 + 1)
                                        addname = data["card"][Anumber]
                                        if (Snumber < 10):
                                              addno = "00"
                                        else:
                                              addno = "0"
                                        addr = addno + str(Snumber) + "." + addname + ','
                                        shows = str(shows) + str(addr)
                                  round = round + 1
                    elif(str(reaction.emoji) == '🇪'):
                            title = "約會大作戰、輝夜姬想讓人告白～天才們的戀愛頭腦戰～、歡迎來到實力至上主義的教室"
                            round = 2059
                            while (round < 2081):
                                  if (str(round) in s):
                                        Snumber = int(round) - (2000)
                                        Anumber = int(round) - (2000 + 1)
                                        addname = data["card"][Anumber]
                                        if (Snumber < 10):
                                              addno = "00"
                                        else:
                                              addno = "0"
                                        addr = addno + str(Snumber) + "." + addname + ','
                                        shows = str(shows) + str(addr)
                                  round = round + 1
                    elif(str(reaction.emoji) == '🇫'):
                            title = "hololive"
                            round = 2081
                            while (round < 2123):
                                  if (str(round) in s):
                                        Snumber = int(round) - (2000)
                                        Anumber = int(round) - (2000 + 1)
                                        addname = data["card"][Anumber]
                                        if (Snumber < 10):
                                              addno = "00"
                                        else:
                                              addno = "0"
                                        addr = addno + str(Snumber) + "." + addname + ','
                                        shows = str(shows) + str(addr)
                                  round = round + 1
                    else:
                        await message.channel.send("錯誤")
                        return
                    embed = discord.Embed(title=str(message.author.name) + "卡片資訊",description=title,color=0xeee657,inline=False)
                    embed.add_field(name="cards", value=str(shows),inline=False)
                    await message.channel.send(embed=embed)
            else:
                await message.channel.send('<@'+str(message.author.id)+'>請先輸入\"註冊\"完成註冊<:mumi:897429663549390868>')
    
    # NameData.json for com
    #change yet
    @commands.command()
    async def 設定助手(self,message, card: str):
        ID = str(message.author.id)
        if(check_user(ID)):
            t = get_user(ID)
            coin = t['point']
            cc = t['re']
            tcard = t['card']
            showss = '>'
            shows = '>'
            addr = 'f'
            filename = "NameData.json"
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
            if (str(card) in str(data.keys())):
                ture = data[card]
                if (str(ture) in str(tcard)):
                    addr = data[card]
                else:
                    await message.channel.send('<@'+str(message.author.id)+'>您沒有這張卡片啦<:mumi05:897429782529212436> ')
            else:
                await message.channel.send('<@'+str(message.author.id)+'>您沒有這張卡片啦<:mumi05:897429782529212436> ')
            if (addr == 'f'):
                return
            else:
                t['assistant'] = int(addr)
            put_user(ID,t)
            await message.channel.send('<@'+str(message.author.id)+'>助手已上任<:mumi01:897429705832169512> ')
            
            #備份用戶資料
            channel = self.bot.get_channel(740946306851143790)
            tsend = str(t)
            i_range = math.ceil(len(tsend)/1900) 
            for i in range(i_range):
                await channel.send("```" + tsend[(i*1900):(i+1)*1900] + "```")
            ###
        else:
            await message.channel.send('<@'+str(message.author.id)+'>請先輸入\"註冊\"完成註冊<:mumi:897429663549390868>')

    # randomcard.json for com
    # no thing to change 
    @commands.command()
    async def 卡池資訊(self,message):
        filename = 'randomcard.json'
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        no = data['no']
        no = str(no)
        n = data[no][0]
        link = data[no][1]
        name = data[no][2]
        arms = data[no][3]
        embed = discord.Embed(title='卡池資訊', description="目前卡池：" + str(n), color=0xeee657,inline=False)
        embed.add_field(name="特殊卡片", value=str(name),inline=False)
        embed.add_field(name="特殊裝備", value=str(arms),inline=False)
        embed.set_image(url=link)
        await message.channel.send(embed=embed)

    # add daysign
    # change yet
    @commands.command()
    async def 簽到(self,message):
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
        datetime_now = datetime.datetime.now()
        time_range = datetime.timedelta(hours = 8)
        new_time = datetime_now+time_range
        today = str(new_time)[0:10]
        data_day_sign = read_file("daysign")
        if (data_day_sign["today"] != today):
            mydict = {"list": "","today" : today}
            write_file("daysign",mydict)
        t = read_file("daysign")
        li = t['list']
        ID = str(message.author.id)
        if (check_user(ID)):
            if (ID in str(li)):
                await message.channel.send('<@' + ID +'> 您今天已經簽到過啦 <:mumi:897429663549390868>  ')
                return
            else:
                t['list'] = li + ID + ','
                write_file("daysign",t)
                        
            #備份daysign.json
            channel = self.bot.get_channel(740959596335726633)
            tsend = str(t)
            await channel.send("```" + tsend + "```")
            ###
            d = get_user(ID)
            if("daysign" in str(d) and d["daysign"] == today):
              await message.channel.send('<@' + ID +'> 您今天已經簽到過啦 <:mumi:897429663549390868>  ')
              return
            d["daysign"] = today
            #print(d)
            coin = d['point']
            if (month == 6 and day == 3):
                coin = int(coin) + 630
            else:
                coin = int(coin) + 100
            d['point'] = coin
            if("experience" in str(d)):
                exp = d["experience"]
                if(exp == ""):
                    exp = 0
                lv = d["level"]
                if(lv == ""):
                    lv = 1
                exp,lv = exp_up(exp,lv,10)
                d["experience"] = exp
                d["level"] = lv
            put_user(ID,d)
            if (month == 6 and day == 3):
                await message.channel.send('<@' + ID +'> 6/3簽到成功，獲得姆咪幣×630<:mumi:897429663549390868> ')
            else:
                await message.channel.send('<@' + ID +'> 簽到成功，獲得姆咪幣×100 <:mumi:897429663549390868>')
            #備份用戶資料
            channel = self.bot.get_channel(740946306851143790)
            tsend = str(d)
            i_range = math.ceil(len(tsend)/1900) 
            for i in range(i_range):
                await channel.send("```" + tsend[(i*1900):(i+1)*1900] + "```")
            ###
        else:
            await message.channel.send('<@' + str(message.author.id) + '> 請先輸入 註冊 完成註冊<:mumi:897429663549390868>  ')

    #no thing to change
    @commands.command()
    async def 計時(self,message, time: int):
        await message.channel.send(str(time) + "秒")
        await asyncio.sleep(time)
        await message.channel.send("時間到")

    # add shop
    # NameData for com
    # change yet
    @commands.command()
    async def 購買(self,message, thing: str, am: int):
        u = str(message.channel.id)
        if (u != "897418292472467487"):
            await message.channel.send('<@' + str(message.author.id) +'>請至<#897418292472467487>')
            return
        ID = str(message.author.id)
        if(check_user(ID)):
            t = get_user(ID)
            re = t['re']
            ss = t['card']
            tcardt = "f"
            with open("NameData.json", 'r', encoding='utf-8') as file:
                data = json.load(file)
            shop = read_file("shop")
            #必中券
            if (str(thing) == "必中券"):
                if (int(am) > 0):
                    pass
                else:
                    return
                if (int(re) >= (100 * am)):
                    re = int(re) - (100 * am)
                    t['re'] = re
                    spe = t['specialchange']
                    spe = int(spe) + am
                    t['specialchange'] = spe
                    put_user(ID,t)
                    await message.channel.send("成功")
                    #備份用戶資料
                    channel = self.bot.get_channel(740946306851143790)
                    tsend = str(t)
                    i_range = math.ceil(len(tsend)/1900) 
                    for i in range(i_range):
                        await channel.send("```" + tsend[(i*1900):(i+1)*1900] + "```")
                    ###
                    return
                else:
                    await message.channel.send("持有交換點數不足")
                    return

            elif (str(thing) == "口罩" or str(thing) == "乾洗手" or str(thing) == "酒精"):
                await message.channel.send("目前缺貨中")

            elif (str(thing) == "鑰匙"):
                if (int(am) > 0):
                    pass
                else:
                    return
                if (int(re) >= (10 * am)):
                    key = t['key']
                    key = int(key) + am
                    t['key'] = key
                    re = int(re) - (10 * am)
                    t['re'] = re
                    put_user(ID,t)
                    await message.channel.send("成功")
                    #備份用戶資料
                    channel = self.bot.get_channel(740946306851143790)
                    tsend = str(t)
                    i_range = math.ceil(len(tsend)/1900) 
                    for i in range(i_range):
                        await channel.send("```" + tsend[(i*1900):(i+1)*1900] + "```")
                    ###
                    return
                else:
                    await message.channel.send("持有交換點數不足")
                    return
            
            elif (str(thing) == "釣魚券B"):
                if (int(am) == 1):
                    pass
                else:
                    return
                mumi=t["point"]
                if (int(mumi) >= (100 * am)):
                    mumi = int(mumi) - (100 * am)
                    t['point'] = mumi
                    if("bag" not in str(t.keys())):
                        await message.channel.send("偵測到資料有誤，請先配合輸入\"Bag\"")
                        return
                    bag1 = t["bag1"]
                    if(bag1 =="BLUE"):
                        await message.channel.send("您目前已經持有一張釣魚券B了")
                        return
                    else:
                        t["bag1"]="BLUE"
                    put_user(ID,t) 
                    await message.channel.send("購買成功")
                    #備份用戶資料
                    channel = self.bot.get_channel(740946306851143790)
                    tsend = str(t)
                    i_range = math.ceil(len(tsend)/1900) 
                    for i in range(i_range):
                        await channel.send("```" + tsend[(i*1900):(i+1)*1900] + "```")
                    ####
                    return
                else:
                    await message.channel.send("持有姆咪幣不足")
                    return
            
            elif (str(thing) == "釣魚券A"):
                if (int(am) == 1):
                    pass
                else:
                    return
                mumi=t["re"]
                if (int(mumi) >= (300 * am)):
                    mumi = int(mumi) - (300 * am)
                    t['re'] = mumi
                    if("bag" not in str(t.keys())):
                        await message.channel.send("偵測到資料有誤，請先配合輸入\"Bag\"")
                        return
                    bag3 = t["bag3"]
                    if(bag3 =="Alpha"):
                        await message.channel.send("您目前已經持有一張釣魚券A了")
                        return
                    else:
                        t["bag3"]="Alpha"
                    put_user(ID,t) 
                    await message.channel.send("購買成功")
                    #備份用戶資料
                    channel = self.bot.get_channel(740946306851143790)
                    tsend = str(t)
                    i_range = math.ceil(len(tsend)/1900) 
                    for i in range(i_range):
                        await channel.send("```" + tsend[(i*1900):(i+1)*1900] + "```")
                    ####
                    return
                else:
                    await message.channel.send("持有交換點數不足")
                    return
            
            elif (str(thing) == "通行券"):
                mumi=t["point"]
                if (int(mumi) >= (100 * am)):
                    mumi = int(mumi) - (100 * am)
                    t['point'] = mumi
                    if("m_pass" not in str(t.keys())):
                        await message.channel.send("請先更新")
                        return
                    m_pass = t["m_pass"]
                    t["m_pass"] += am
                    put_user(ID,t)
                    await message.channel.send("購買成功")
                    #備份用戶資料
                    channel = self.bot.get_channel(740946306851143790)
                    tsend = str(t)
                    i_range = math.ceil(len(tsend)/1900) 
                    for i in range(i_range):
                        await channel.send("```" + tsend[(i*1900):(i+1)*1900] + "```")
                    ####
                    return
                else:
                    await message.channel.send("持有姆咪幣不足")
                    return
            
            elif (str(thing) == "石頭"):
                mumi=t["point"]
                if (int(mumi) >= (1000 * am)):
                    mumi = int(mumi) - (1000 * am)
                    t['point'] = mumi
                    if("stone" not in str(t.keys())):
                        await message.channel.send("請先更新")
                        return
                    stone = t["stone"]
                    if(t["stone"] == ""):
                        t["stone"] = 0
                    t["stone"] += am 
                    put_user(ID,t)
                    await message.channel.send("購買成功")
                    #備份用戶資料
                    channel = self.bot.get_channel(740946306851143790)
                    tsend = str(t)
                    i_range = math.ceil(len(tsend)/1900) 
                    for i in range(i_range):
                        await channel.send("```" + tsend[(i*1900):(i+1)*1900] + "```")
                    ####
                    return
                else:
                    await message.channel.send("持有姆咪幣不足")
                    return
            
            elif(str(thing)=="魚餌"):
                mumi=t["point"]
                if (int(mumi) >= (500 * am)):
                    mumi = int(mumi) - (500 * am)
                    t['point'] = mumi
                else:
                    await message.channel.send("持有姆咪幣不足")
                    return
                if("bug" in str(t.keys())):
                    t['bug'] += am
                else:
                    t['bug'] = am
                put_user(ID,t)
                await message.channel.send("購買成功")
                #備份用戶資料
                channel = self.bot.get_channel(740946306851143790)
                tsend = str(t)
                i_range = math.ceil(len(tsend)/1900) 
                for i in range(i_range):
                    await channel.send("```" + tsend[(i*1900):(i+1)*1900] + "```")
                ###
                return
            
            elif (str(thing) == "木桶"):
                if (int(am) == 1):
                    pass
                else:
                    return
                mumi=t["point"]
                if (int(mumi) >= (200 * am)):
                    mumi = int(mumi) - (200 * am)
                    t['point'] = mumi
                    if("tub" in str(t.keys())):
                      tub = t["tub"][0]
                      if(tub == "wood"):
                          await message.channel.send("您已經有木桶啦")
                          return
                    else:
                        t["tub"]=["wood","","","","","","","","","","","","","","","","","","","",""]
                    put_user(ID,t)
                    await message.channel.send("購買成功")
                    #備份用戶資料
                    channel = self.bot.get_channel(740946306851143790)
                    tsend = str(t)
                    i_range = math.ceil(len(tsend)/1900) 
                    for i in range(i_range):
                        await channel.send("```" + tsend[(i*1900):(i+1)*1900] + "```")
                    ####
                    return
                else:
                    await message.channel.send("持有姆咪幣不足")
                    return

            elif (str(thing) in str(data)):
                things = data[thing]
                things = str(things)
                if (str(things) in str(shop)):
                    thingin = shop[things]
                    if (int(thingin) >= 1):
                        no = data[thing]
                        tcardt = "t"
                    if (tcardt == "t"):
                        if (am != 1):
                            await message.channel.send("數量設定錯誤")
                            return
                        if (str(no) in str(ss)):
                            await message.channel.send('<@' + str(message.author.id)+'> 您已經有這張卡了<:mumi:897429663549390868>  ')
                            return
                        elif (int(re) >= 100):
                            t['card'] = str(ss) + str(no) + ","
                            re = int(re) - 100
                            t['re'] = re
                            shop[things] = int(thingin) - 1
                            put_user(ID,t)
                            write_file("shop",shop)
                                        
                            #備份shop.json
                            channel = self.bot.get_channel(740947177009840158)
                            tsend = str(shop)
                            await channel.send("```" + tsend + "```")
                            ###
                                            
                            await message.channel.send( '<@' + str(message.author.id) + '> 購買成功 ')
                            #備份用戶資料
                            channel = self.bot.get_channel(740946306851143790)
                            tsend = str(t)
                            i_range = math.ceil(len(tsend)/1900) 
                            for i in range(i_range):
                                await channel.send("```" + tsend[(i*1900):(i+1)*1900] + "```")
                            ###
                            return

                        elif (int(re) < 100):
                            await message.channel.send('<@' + str(message.author.id) + '> 交換點數不足 ')
                            return
                    else:
                      await message.channel.send("此卡片未販售/缺貨中")
                      return
            else:
                await message.channel.send('<@' + str(message.author.id) +'> 沒有賣' + str(thing) + "啦")
        else:
            await message.channel.send('<@' + str(message.author.id) +'> 請先輸入 註冊 完成註冊(・∀・) ')

    #change yet
    @commands.command()
    async def 更新(self,message):
        ID = str(message.author.id)
        if((check_user(ID))==0):
            await message.channel.send("請先完成註冊")
            return 
        d = get_user(ID)
        if ("new" in d.keys()):
            new = d['new']
            if (str(new) == "2.1.3.1"):
                await message.channel.send("您已經更新到最新版本啦")
                return
        t = str(d.keys())
        if ("box" not in t):
            d['box'] = 0
        if ("key" not in t):
            d['key'] = 0
        if ("bag1" not in t):
            d['bag1'] = ""
        if ("bag2" not in t):
            d['bag2'] = ""
        if ("bag3" not in t):
            d['bag3'] = ""
        if ("bag4" not in t):
            d['bag4'] = ""
        if ("bag5" not in t):
            d['bag5'] = ""
        if ("level" not in t):
            d['level'] = 1
        if ("experience" not in t):
            d['experience'] = 0
        if ("money" not in t):
            d['money'] = 0
        if ("activity" not in t):
            d['activity'] = ""
        if ("stone" not in t or d['stone'] == ""):
            d['stone'] = 0
        if ("pis" not in t):
            d['pis'] = 0
        if ("specialchange" not in t):
            d['specialchange'] = 0
        if ("now_role" not in t):
            d["now_role"] = 1
        if ("role1" not in t):
            d['role1'] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]#number,level,exp,hp,atk,def,spd,php,patk,pdef,pspd,0,0,0,0
        if ("m_pass" not in t):
            d['m_pass'] = 0
        if ("arms" not in t):
            d["arms"] = {"1":[0,0,0,0,0],"2":[0,0,0,0,0],"3":[0,0,0,0,0],"4":[0,0,0,0,0],"5":[0,0,0,0,0],"6":[0,0,0,0,0],"7":[0,0,0,0,0],"8":[0,0,0,0,0],"9":[0,0,0,0,0],"10":[0,0,0,0,0]}
        if ("good_potion" not in t):
            d['good_potion'] = 0
        if ("statue" not in t):
            d['statue'] = [0,0,0,0,0]
        d['new'] = "2.1.3.1"
        #######增加########
        d["point"] += 1000
        #######增加########
        await message.channel.send("獲得姆咪幣×1000")
        put_user(ID,d)
        await message.channel.send("更新成功")  
        #備份用戶資料
        channel = self.bot.get_channel(740946306851143790)
        tsend = str(d)
        i_range = math.ceil(len(tsend)/1900) 
        for i in range(i_range):
            await channel.send("```" + tsend[(i*1900):(i+1)*1900] + "```")
        ###
        

    # change yet
    @commands.command()
    async def 商品總覽(self,message):
        embed = discord.Embed(title="商品總覽",description=str(datetime.datetime.now().year) + "/" + str(datetime.datetime.now().month) + "/" + str(datetime.datetime.now().day),color=0xeee657)
        embed.add_field(name="1.必中券", value="價格：100交換點數", inline=False)
        embed.add_field(name="2.鑰匙", value="價格：10交換點數", inline=False)
        embed.add_field(name="3.木桶", value="價格：200姆咪幣", inline=False)
        embed.add_field(name="4.釣魚券B", value="價格：100姆咪幣", inline=False)
        embed.add_field(name="5.釣魚券A", value="價格：300交換點數", inline=False)
        embed.add_field(name="6.魚餌", value="價格：500姆咪幣", inline=False)
        embed.add_field(name="7.通行券", value="價格：100姆咪幣", inline=False)
        embed.add_field(name="8.石頭", value="價格：1000姆咪幣", inline=False)
        shop = read_file("shop")
        filename = "data.json"
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        total = shop['total']
        times = 0
        time = 0
        while (time != 2200):
            timep = time + 2001
            if (str(timep) in str(shop)):
                timep = str(timep)
                shopnumber = shop[timep]
                if (int(shopnumber) >= 1):
                    addn = times + 9
                    addc = data['card'][time]
                    embed.add_field(name=str(addn) + "." + str(addc), value="價格：100交換點數", inline=False)
                    times = times + 1
            time = time + 1
        await message.channel.send(embed=embed)

        # not change
        # lock can't use now
    
    # change yet
    @commands.command()
    async def 物品總覽(self,message):
        ID = str(message.author.id)
        if(check_user(ID)):
            t = get_user(ID)
            key = t['key']
            box = t["box"]
            m_pass = t["m_pass"] 
            specialchange = t['specialchange']
            embed = discord.Embed(title=str(message.author.name) + "物品資訊",description="如需查看指令集，請輸入help_mumi",color=0xeee657)
            embed.add_field(name="必中券", value=specialchange,inline=False)
            embed.add_field(name="寶箱", value=box,inline=False)
            embed.add_field(name="鑰匙", value=key,inline=False)
            embed.add_field(name="通行券", value=m_pass,inline=False)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send('<@' + str(message.author.id) + '> 請先輸入 註冊 完成註冊<:mumi:897429663549390868> ')

        # change yet
    
    @commands.command()
    async def 開啟寶箱(self,message):
      #u = str(message.channel)
      #if (u != "寶箱領取頻道"):
      #await message.channel.send('<@'+str(message.author.id)+'> 請至<#676276525573603328>')
      #return
      ID = str(message.author.id)
      if(check_user(ID) == 0):
        await message.channel.send("請先完成註冊")
        return
      t = get_user(ID)
      box = t['box']
      coin = t['point']
      key = t['key']
      re = t['re']
      pis = t['pis']
      specialchange = t['specialchange']
      if (int(key) > 0 and int(box) > 0):
        key = int(key) - 1
        box = int(box) - 1
        t['key'] = key
        t['box'] = box
        nm = (random.randint(1, 100))
        if (nm > 40):
          run = (random.randint(100, 200))
          coin = int(coin) + run
          t['point'] = coin
          await message.channel.send("玩家`" + str(message.author.name) +"`獲得了`姆咪幣×" + str(run) + "`")
        elif (nm > 10 and nm <= 40):
          run = (random.randint(20, 100))
          pis = int(pis) + run
          t['pis'] = pis
          await message.channel.send("玩家`" + str(message.author.name) +"`獲得了`金幣×" + str(run) + "`")
        elif (nm > 1 and nm <= 10):
          run = (random.randint(20, 50))
          re = int(re) + run
          t['re'] = re
          await message.channel.send("玩家`" + str(message.author.name) +"`獲得了`交換點數×" + str(run) + "`")
        elif (nm == 1):
          specialchange = int(specialchange) + 1
          t['specialchange'] = specialchange
          await message.channel.send("玩家`" + str(message.author.name) +"`獲得了`必中券×1`")
        put_user(ID,t)
            
        #備份用戶資料
        channel = self.bot.get_channel(740946306851143790)
        tsend = str(t)
        i_range = math.ceil(len(tsend)/1900) 
        for i in range(i_range):
          await channel.send("```" + tsend[(i*1900):(i+1)*1900] + "```")
        ###
            
      else:
        await message.channel.send("持有的寶箱或鑰匙數量不足")

    # add sell
    # data.json for com
    # change yet
    @commands.command()
    async def 競標資訊(self,message):
      s = read_file("sell")
      date = s['date']
      # >= 22 <8
      # >= 14 <0
      if (int(datetime.datetime.now().hour) < 0 or int(datetime.datetime.now().hour) >= 14):
        await message.channel.send("本日競標時間已過")
        return
      no1 = s['no1']
      name1 = s['name1']
      id1 = s['id1']
      coin1 = s['coin1']
      no2 = s['no2']
      name2 = s['name2']
      id2 = s['id2']
      coin2 = s['coin2']
      filename = "data.json"
      with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
      Anumber = int(no1) - (2000 + 1)
      addr = data["card"][Anumber]
      if (no2 == 1):
        add2 = "必中券×10"
      if (no2 == 2):
        add2 = "寶箱×10"
      if (no2 == 3):
        add2 = "姆咪幣×1000"
      if (no2 == 4):
        add2 = "交換點數×200"
      if (no2 == 5):
        add2 = "鑰匙×30"
      if (no2 == 6):
        add2 = "石頭×10"
      embed = discord.Embed(title="競標資訊",description=str(datetime.datetime.now().year) + "/" + str(datetime.datetime.now().month) + "/" + str(datetime.datetime.now().day),color=0xeee657)
      one = "目前得標者(名字/id)：" + str(name1) + "/" + str(id1) + "\n目前出價：" + str(coin1) + "金幣"
      two = "目前得標者(名字/id)：" + str(name2) + "/" + str(id2) + "\n目前出價：" + str(coin2) + "金幣"
      embed.add_field(name="1." + str(addr), value=one, inline=False)
      embed.add_field(name="2." + str(add2), value=two)
      embed.add_field(name="競標場開放時間", value="08：00～22：00")
      await message.channel.send(embed=embed)

    # add sell
    # randomcard.json for com
    # change yet
    @commands.command()
    async def 結算(self,message):
      u = str(message.channel)
      s = read_file("sell")
      date = s['date']
      id1 = s['id1']
      no1 = s['no1']
      coin1 = s['coin1']
      id2 = s['id2']
      no2 = s['no2']
      coin2 = s['coin2']
      Ststone = "f"
      if (str(date) != str(datetime.datetime.now().day)):
        pass
      else:
        return
      # >= 22 <8
      # >= 14 <0
      if (int(datetime.datetime.now().hour) < 14):
        if (str(message.author.id) == "550907252970749952"):
          Ststone = "t"
        else:
          return
      if (str(message.author.id) == "550907252970749952"
          or str(message.author.id) == "544552665204654080"
          or str(message.author.id) == "480747560793931778"
          or str(message.author.id) == "352066968750260245"
          or str(message.author.id) == "511246631073611808"
          or str(message.author.id) == "597692502346301452"):
        pass
      else:
        return
      if (id1 == 'no'):
        pass
      else:
        a = get_user(str(id1))
        coin = a['pis']
        a['pis'] = int(coin) - int(coin1)
        card = a['card']
        a['card'] = str(card) + str(no1) + ","
        put_user(str(id1),a)
        #備份用戶資料
        #channel = bot.get_channel(740946306851143790)
        #tsend = str(a)
        #await channel.send("```" + tsend + "```")
        ###

      if (id2 == "no"):
        pass
      else:
        b = get_user(str(id2))
        coin = b['pis']
        b['pis'] = int(coin) - int(coin2)
        if (no2 == 1):
          specialchange = b["specialchange"]
          b["specialchange"] = int(specialchange) + 10
          #必中券×10
        elif (no2 == 2):
          box = b["box"]
          b["box"] = int(box) + 10
          #寶箱×10
        elif (no2 == 3):
          point = b['point']
          b['point'] = int(point) + 1000
          #姆咪幣×1000
        elif (no2 == 4):
          re = b['re']
          b['re'] = int(re) + 200
          #交換點數×100
        elif (no2 == 5):
          key = b['key']
          b['key'] = int(key) + 30
          #鑰匙×30
        elif (no2 == 6):
          stone = b['stone']
          if(stone == ""):
            stonee = 0
          b['stone'] = int(stone) + 10
          #石頭×10
        else:
          pass
        put_user(str(id2),b)
            
        #備份用戶資料
        #channel = bot.get_channel(740946306851143790)
        #tsend = str(b)
        #await channel.send("```" + tsend + "```")
        ###
      s = read_file("sell")
      date = s['date']
      no1 = s['no1']
      name1 = s['name1']
      id1 = s['id1']
      coin1 = s['coin1']
      no2 = s['no2']
      name2 = s['name2']
      id2 = s['id2']
      coin2 = s['coin2']
      filename = "data.json"
      with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
      Anumber = int(no1) - (2000 + 1)
      addr = data["card"][Anumber]
      if (no2 == 1):
        add2 = "必中券×10"
      if (no2 == 2):
        add2 = "寶箱×10"
      if (no2 == 3):
        add2 = "姆咪幣×1000"
      if (no2 == 4):
        add2 = "交換點數×200"
      if (no2 == 5):
        add2 = "鑰匙×30"
      if (no2 == 6):
        add2 = "石頭×10"
      channel = self.bot.get_channel(897418210629021716)
      one = ""
      f = 0
      if(str(id1)!="no"):
        one += "恭喜<@"+str(id1)+">以"+str(coin1)+"金幣得標了"+str(addr)+"\n"
        f = 1
      if(str(id2)!="no"):
        one +="恭喜<@"+str(id2)+">以"+str(coin2)+"金幣得標了"+str(add2)+"\n"
        f = 1
      if(f==0):
        one = "本日無人得標"
      await channel.send(one) 
      filename1 = 'randomcard.json'
      with open(filename1, 'r', encoding='utf-8') as file:
        randomNumber = json.load(file)
      rans = randomNumber['keepS']
      rane = randomNumber['keepE']
      no1 = (random.randint(rans, rane))
      no2 = (random.randint(1, 6))
      date = int(datetime.datetime.now().day) - 1
      if (Ststone == "t"):
        date = int(datetime.datetime.now().day) - 2
      mydict = {
          "date": str(date),
          "no1": no1,
          "id1": "no",
          "name1": "no",
          "coin1": "100",
          "no2": no2,
          "id2": "no",
          "name2": "no",
          "coin2": "200"
      }
      write_file("sell",mydict)
      await message.channel.send("成功")  
      #備份sell.json
      channel = self.bot.get_channel(740946913788035103)
      tsend = str(mydict)
      await channel.send("```" + tsend + "```")
      ###
        
    # add sell
    # change yet
    @commands.command()
    async def 出價(self,message, a: int, b: int):
      ID = str(message.author.id)
      u = str(message.channel.id)
      if (u != "677782055236403211" and u != "897418388048056360"):
        await message.channel.send('<@' + str(message.author.id) +'>請至<#897418388048056360>')
        return
      # >= 22 <8
      # >= 14 <0
      if (int(datetime.datetime.now().hour) >= 14 or int(datetime.datetime.now().hour) < 0):
        await message.channel.send("本日競標時間已過，請恰管理員結算")
        return
      if (a > 2):
        await message.channel.send("むみぃ><")
        return
      s = read_file("sell")
      date = s['date']
      id1 = s['id1']
      name1 = s['name1']
      coin1 = s['coin1']
      id2 = s['id2']
      name2 = s['name2']
      coin2 = s['coin2']
      t = get_user(ID)
      if("new"not in str(t.keys()) or t["new"]!="2.1.3.1"):
        await message.channel.send("請先更新")
        return
      pis = t['pis']

      if (a == 1 and int(pis) >= int(b) and int(b) > int(coin1)):
        if (str(id2) == str(message.author.id)):
          await message.channel.send("無法一次競標兩個物品")
          return
        s['id1'] = str(message.author.id)
        s['coin1'] = b
        s['name1'] = str(message.author.name)
      elif (int(pis) < int(b) and a == 1):
        await message.channel.send("持有的金幣不足")
        return
      elif (int(b) <= int(coin1) and a == 1):
        await message.channel.send("請出比當前價格更高的金額")
        return

      if (a == 2 and int(pis) >= int(b) and int(b) > int(coin2)):
        if (str(id1) == str(message.author.id)):
          await message.channel.send("無法一次競標兩個物品")
          return
        s['id2'] = str(message.author.id)
        s['coin2'] = b
        s['name2'] = str(message.author.name)
      elif (int(pis) < int(b) and a == 2):
        await message.channel.send("持有的金幣不足")
        return
      elif (int(b) <= int(coin2) and a == 2):
        await message.channel.send("請出比當前價格更高的金額")
        return
      write_file("sell",s)
      await message.channel.send("出價成功")  
      #備份sell.json
      channel = self.bot.get_channel(740946913788035103)
      tsend = str(s)
      await channel.send("```" + tsend + "```")
      ###

    # NameData.json for com
    # no thing to change
    @commands.command()
    async def 卡片編號總覽(self,message):
      u = str(message.channel.id)
      if (u == "695838524813082624"):
        pass
      else:
        return
      filename = 'NameData.json'
      with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
      await message.channel.send("```" + str(data) + "```")

    # no thing to change
    @commands.command()
    async def 抽籤(self,message, a: int, b: int, c: str):
      d = c
      while (str(d) in c):
        d = (random.randint(a, b))
      await message.channel.send(d)

    # no thing to change
    @commands.command()  #only for Ststone
    async def 標記(self,message,a: str,b:int):
      i =1
      if(str(message.author.id) == "550907252970749952"):
        pass
      else:
        return
      while (i<=b):
        await message.channel.send(a)
        await asyncio.sleep(1)
        i =i+1

    # NameData.json  for com
    # data.json for com
    # add change 
    # change yet
    @commands.command()
    async def 販賣(self,message, thing: str):
      ID = str(message.author.id)
      filename = 'NameData.json'
      with open(filename, 'r', encoding='utf-8') as file:
        NameData = json.load(file)
      filename = 'data.json'
      with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
      shop = read_file("shop")
      user = get_user(ID)
      number = NameData[thing]
      number = str(number)
      card = user['card']
      assistant = user['assistant']
      if (str(number) == str(assistant)):
        await message.channel.send("不能賣自己的助手啦")
        return
      c = read_file("change")
      if ("user1" in str(c)):
        await message.channel.send("請先完成交換")
        return
      if (str(number) in str(card)):
        pass
      else:
        return
      if (str(number) in str(shop)):
        a = shop[number]
        shop[number] = a + 1
      else:
        shop[number] = 1
      one = str(number) + ","
      two = ""
      ccard = card.replace(one, two)
      user['card'] = ccard
      re = user['re']
      re = int(re) + 70
      user['re'] = re
      write_file("shop",shop)
      put_user(ID,user)
      await message.channel.send("販賣成功，獲得交換點數×70")
      #備份shop.json
      channel = self.bot.get_channel(740947177009840158)
      tsend = str(shop)
      await channel.send("```" + tsend + "```")
      ### 
      #備份用戶資料
      channel = self.bot.get_channel(740946306851143790)
      tsend = str(user)
      i_range = math.ceil(len(tsend)/1900) 
      for i in range(i_range):
        await channel.send("```" + tsend[(i*1900):(i+1)*1900] + "```")
      ###

    # change yet
    @commands.command()
    async def 清庫存(self,message):
      print("111")
      if (str(message.author.id) == "550907252970749952"
          or str(message.author.id) == "597692502346301452"):
        pass
      else:
        return
      shop = read_file("shop")
      total = shop['total']
      shop['total'] = 200
      times = 0
      time = 0
      while (time != total):
        timep = time + 2001
        if (str(timep) in str(shop)):
          timep = str(timep)
          shopnumber = shop[timep]
          if (int(shopnumber) >= 1):
            newnumber = math.ceil(int(shopnumber) * 0.4)
            newtimep = int(shopnumber) - int(newnumber)
            shop[timep] = newtimep
        time = time + 1
      write_file("shop",shop)
      await message.channel.send("成功") 
      #備份shop.json
      channel = self.bot.get_channel(740947177009840158)
      tsend = str(shop)
      await channel.send("```" + tsend + "```")
      ###

    # change yet
    @commands.command()
    async def 謝謝姆咪(self,message):
      year = datetime.datetime.now().year
      month = datetime.datetime.now().month
      day = datetime.datetime.now().day
      t = read_file("daysign")
      li = t['list']
      if ("thanks" in str(t)):
        thanks = t['thanks']
      else:
        thanks = ""
      if (str(message.author.id) in str(thanks)):
        return
      else:
        if (str(message.author.id) in str(li)):
          pass
        else:
          return
        ID = str(message.author.id)
        t['thanks'] = thanks + str(message.author.id) + ','
        write_file("daysign",t) 
        await message.channel.send("<a:mumimumi:897429783619715072><a:mumimumi:897429783619715072><a:mumimumi:897429783619715072><a:mumimumi:897429783619715072><a:mumimumi:897429783619715072>")
        #備份daysign.json
        channel = self.bot.get_channel(740959596335726633)
        tsend = str(t)
        await channel.send("```" + tsend + "```")
        ###

    @commands.command()
    async def help_mumi(self,message):
        return
        await message.channel.send("test")


def setup(bot):
    bot.add_cog(Common(bot))