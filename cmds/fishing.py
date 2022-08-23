import discord
from discord.ext import commands
from datetime import datetime
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



class Synchronize(Cog_Extension):

  @commands.command()
  async def 使用(self,message,thing:str):
    ID = str(message.author.id)
    User = get_user(ID)
    if("bag"not in str(User)):
      await message.channel.send("偵測到資料有誤，請先配合輸入\"Bag\"")
      return
    bag1 = User["bag1"]
    bag3 = User["bag3"]
    if(datetime.now().hour >= 15 and datetime.now().hour < 16):
      await message.channel.send("每日23點後為釣魚場休息時間，不可入場，請等待隔天")
      return
    if(thing == "釣魚券B" and bag1 == "BLUE"):
      role = self.bot.get_guild(782593702455279616).get_role(897665135877951498)
      await message.author.add_roles(role)
      await message.channel.send("<@"+str(message.author.id)+"> 已添加身分組 <@&897665135877951498>，並可進入<#897420197634400276>")
      User["bag1"] = ""
      put_user(ID,User)
    elif(thing == "釣魚券A" and bag3 == "Alpha"):
      role = self.bot.get_guild(782593702455279616).get_role(897665169273020438)
      await message.author.add_roles(role)
      await message.channel.send("<@"+str(message.author.id)+"> 已添加身分組 <@&897665169273020438>，並可進入<#897420159491375105>")
      User["bag3"] = ""
      put_user(ID,User)
    elif(thing == "VIP券" and bag1 == "VIP"):
      await message.channel.send("<@"+str(message.author.id)+"> 您已經可進入 <#742593521550229516>了")
    elif(thing == "魚餌"):
      fishing = read_file("fishing")
      if(datetime.now().min ==0):
        await message.channel.send("請勿在00分使用魚餌")
        return
      if("bug" in str(User)):
        pass
      else:
        await message.channel.send("您沒有魚餌")
        return
      bug = User["bug"]
      if(bug>= 1):
        User["bug"]-=1
        if(message.channel.id == 897420197634400276):
          fishing["BlueTime"] = 100
          if("BlueBug" in str(fishing)):
            BlueBug = fishing["BlueBug"]
            if(BlueBug == datetime.now().hour):
              await message.channel.send("目前已經有人使用了魚餌")
              return
          fishing["BlueBug"] = datetime.now().hour
        elif(message.channel.id == 742593521550229516):
          fishing["VIPTime"] = 100
          if("VIPBug" in str(fishing)):
            VIPBug = fishing["VIPBug"]
            if(VIPBug == datetime.now().hour):
              await message.channel.send("目前已經有人使用了魚餌")
              return
          fishing["VIPBug"] = datetime.now().hour
        elif(message.channel.id == 897420159491375105):
          fishing["AlphaTime"] = 100
          if("AlphaBug" in str(fishing)):
            VIPBug = fishing["AlphaBug"]
            if(VIPBug == datetime.now().hour):
              await message.channel.send("目前已經有人使用了魚餌")
              return
          fishing["AlphaBug"] = datetime.now().hour
        else:
          await message.channel.send("這裡不能用魚餌啦")
          return
        put_user(ID,User)
        write_file("fishing",fishing)
        await message.channel.send("使用成功")

    else:
      await message.channel.send("未擁有此物品或輸入格式錯誤")

  @commands.command()#改好了
  async def 下竿(self,message):
    ID = str(message.author.id)
    done = "f"
    fishing = read_file("fishing")
    if("BlueBug" in str(fishing)):
      a = fishing["BlueBug"]
      if(a != datetime.now().hour):
        fishing["BlueTime"] = 300
        done = "t"
        del fishing["BlueBug"]
    if("AlphaBug" in str(fishing)):
      a = fishing["AlphaBug"]
      if(a != datetime.now().hour):
        fishing["AlphaTime"] = 300
        done = "t"
        del fishing["AlphaBug"]
    if("VIPBug" in str(fishing)):
      a = fishing["VIPBug"]
      if(a != datetime.now().hour):
        fishing["VIPTime"] = 200
        done = "t"
        del fishing["VIPBug"]
    if(done == "t"):
      write_file("fishing",fishing)
    User = get_user(ID)
    channel = message.channel.id
    if(channel==897420159491375105 or channel == 897420197634400276):#可加or敘述
      fishing = read_file("fishing")
      if("tub" not in str(User)):
        await message.channel.send("您沒有桶子")
        return
      tub = User["tub"][0]
      space = fishing[tub][0]
      tub = fishing[tub][1]
      i = 1
      while(i<=space):
        F = User["tub"][i]
        if(F == ""):
          break
        i+=1
      if(i>space):
        await message.channel.send("桶子空間不足")
        return
      list = fishing["list"]
      if(ID in list or ID in str(fishing)):
        await message.channel.send("您已經下竿了")
        return
      else:
        list = list+","+ID
        fishing["list"] = list
        write_file("fishing",fishing)
        timepd = (random.randint(-100, 100))
        await message.channel.send("下竿成功")
        if(channel==897420197634400276):#藍色釣魚場
          Time = fishing["BlueTime"]
          Time += timepd
          fish = random.randint(0,140)
        elif(channel==742593521550229516):#VIP釣魚場
          Time = fishing["VIPTime"]
          Time += timepd
          fish = random.randint(40,300)
        #未完成
        elif(channel==897420159491375105):#Alpha釣魚場
          Time = fishing["AlphaTime"]
          Time += timepd
          fish = random.randint(151,300)
        t = 0
        while(t <= Time):
          await asyncio.sleep(1)
          fishing = read_file("fishing")
          List = fishing["list"]
          if(ID not in List):
            return
          t+=1

        #無東西：0~20
        #魚:21~70
        #熱帶魚:71~100
        #河豚:101~130
        #螃蟹:131~150
        #鯉魚王:151~170 (5~10)隻->中階經驗藥水*1
        #鯊魚: 171~180 石頭1~5
        #蝦子: 181~280 交換點數1~5
        #花枝: 281~300 金幣1~5
        fishing = read_file("fishing")
        List = fishing["list"]
        if(ID in List):
          await message.channel.send("<@"+str(message.author.id)+"> 似乎有東西上鉤了")
        else:
          return
        newlist = List.replace((","+ID),"")
        fishing["list"] = newlist
        if(fish<=20):#無東西：0~20
          fishing[ID] = ["none","F"]
        elif(fish<=70):#魚:21~70
          fishing[ID] = ["fish","F"]
        elif(fish<=100):#熱帶魚:71~100
          fishing[ID] = ["tropical_fish","F"]
        elif(fish<=130):#河豚:101~130
          fishing[ID] = ["blowfish","F"]
        elif(fish<=150):#螃蟹:131~150
          fishing[ID] = ["crab","F"]
        elif(fish<=170):#鯉魚王:151~170
          fishing[ID] = ["magikarp","F"]
        elif(fish<=180):#鯊魚: 171~180
          fishing[ID] = ["shark","F"]
        elif(fish<=280):#蝦子: 181~280
          fishing[ID] = ["shrimp","F"]
        elif(fish<=300):#花枝: 281~300
          fishing[ID] = ["squid","F"]
        write_file("fishing",fishing)
        wait = random.randint(10,20)
        await asyncio.sleep(wait)
        fishing = read_file("fishing")
        list = fishing["list"]
        if(ID in str(fishing) and ID not in list):
          del fishing[ID]
          list = list+","+ID
          fishing["list"] = list
          write_file("fishing",fishing)
      #List = data["list"]
			#newlist = List.replace(str(message.author.id), "")
			#data["list"] = newlist
      #del answer[str(msg5.id)]
      #await msg5.delete()
  
  @commands.command()#改好了
  async def 收竿(self,message):
    ID = str(message.author.id)
    fish = ""
    channel = message.channel.id
    if(channel==897420197634400276 or channel == 742593521550229516  or channel == 897420159491375105):#可加or敘述
      fishing = read_file("fishing")
      list = fishing["list"]
      if(ID in list):
        newlist = list.replace((","+ID),"")
        fishing["list"] = newlist
        await message.channel.send("<@"+str(message.author.id)+"> 收竿時機不對，沒有釣到任何東西")
        write_file("fishing",fishing)
      elif(ID in str(fishing)):
        fish = fishing[ID][0]
        del fishing[ID]
        write_file("fishing",fishing)
      else:
        return
      if(fish == "none"):
        await message.channel.send("您什麼也沒有釣到")
        return
      elif(fish == "fish"):
        await message.channel.send("恭喜您釣到了魚 :fish: ")
      elif(fish == "tropical_fish"):
        await message.channel.send("恭喜您釣到了熱帶魚 :tropical_fish: ")
      elif(fish == "blowfish"):
        await message.channel.send("恭喜您釣到了河豚 :blowfish: ")
      elif(fish == "crab"):
        await message.channel.send("恭喜您釣到了螃蟹 :crab: ")
      elif(fish == "magikarp"):
        await message.channel.send("恭喜您釣到了鯉魚王 <:magikarp:743296027381071875> ")
      elif(fish == "shark"):
        await message.channel.send("恭喜您釣到了鯊魚 🦈 ")
      elif(fish == "shrimp"):
        await message.channel.send("恭喜您釣到了蝦子 🦐 ")
      elif(fish == "squid"):
        await message.channel.send("恭喜您釣到了花枝 🦑 ")
      User = get_user(ID)
      tub = User["tub"][0]
      space = fishing[tub][0]
      tub = fishing[tub][1]
      i = 1
      while(i<=space):
        F = User["tub"][i]
        if(F == ""):
          User["tub"][i] = fish
          put_user(ID,User)
          return
        i+=1    
  
  @commands.command()#改好了
  async def 桶子(self,message):
    ID = str(message.author.id)
    User = get_user(ID)
    fishing = read_file("fishing")
    if("tub" in str(User)):
      pass
    else:
      await message.channel.send("您目前沒有桶子")
      return
    tub = User["tub"][0]
    space = fishing[tub][0]
    tub = fishing[tub][1]
    i = 1
    fish = 0
    tropical_fish = 0
    blowfish = 0
    crab = 0
    magikarp = 0
    shark = 0
    shrimp = 0
    squid = 0
    while(i<=space):
      F = User["tub"][i]
      if(F == "fish"):
        fish +=1
      elif(F == "tropical_fish"):
        tropical_fish +=1
      elif(F == "blowfish"):
        blowfish +=1
      elif(F == "crab"):
        crab +=1
      elif(F == "magikarp"):
        magikarp +=1
      elif(F == "shark"):
        shark +=1
      elif(F == "shrimp"):
        shrimp +=1
      elif(F == "squid"):
        squid +=1
      else:
        pass
      i+=1
    embed = discord.Embed(title=str(message.author.name)+"桶子資訊",description=tub+"空間："+str(space),color=0xeee657)
    embed.add_field(name="🐟魚",value=fish,inline=False)
    embed.add_field(name="🐠熱帶魚", value=tropical_fish,inline=False)
    embed.add_field(name="🐡河豚",value=blowfish,inline=False)
    embed.add_field(name="🦀螃蟹",value=crab,inline=False)
    embed.add_field(name="<:magikarp:743296027381071875>鯉魚王",value=magikarp,inline=False)
    embed.add_field(name="🦈鯊魚",value=shark,inline=False)
    embed.add_field(name="🦐蝦子",value=shrimp,inline=False)
    embed.add_field(name="🦑花枝",value=squid,inline=False)
    if("bug"in str(User)):
      bug = User["bug"]
      embed.add_field(name="魚餌(不占空間)",value=bug,inline=False)
    await message.channel.send(embed=embed)
  
  @commands.command()#改好了
  async def 魚市價格(self,message):
    Market = read_file("Fish_market")
    #price
    fish = Market["fish"][0]
    tropical_fish = Market["tropical_fish"][0]
    blowfish = Market["blowfish"][0]
    crab = Market["crab"][0]
    magikarp = Market["magikarp"][0]
    shark = Market["shark"][0]
    shrimp = Market["shrimp"][0]
    squid = Market["squid"][0]
    #quote change
    Qfish = Market["fish"][1]
    Qtropical_fish = Market["tropical_fish"][1]
    Qblowfish = Market["blowfish"][1]
    Qcrab = Market["crab"][1]
    Qmagikarp = Market["magikarp"][1]
    Qshark = Market["shark"][1]
    Qshrimp = Market["shrimp"][1]
    Qsquid = Market["squid"][1]
    Date = str(datetime.now().year)+"/"+str(datetime.now().month)+"/"+str(datetime.now().day)
    embed = discord.Embed(title="今日魚市",description=Date,color=0xeee657,inline=False)
    pfish="價格："+str(fish)+"交換點數/漲跌幅："+str(Qfish)
    ptropical_fish="價格："+str(tropical_fish)+"交換點數/漲跌幅："+str(Qtropical_fish)
    pblowfish="價格："+str(blowfish)+"交換點數/漲跌幅："+str(Qblowfish)
    pcrab="價格："+str(crab)+"交換點數/漲跌幅："+str(Qcrab)
    
    pmagikarp="價格："+str(magikarp)+"隻換一瓶中階經驗藥水/漲跌幅："+str(Qmagikarp)
    pshark="價格："+str(shark)+"石頭/漲跌幅："+str(Qshark)
    pshrimp="價格："+str(shrimp)+"交換點數/漲跌幅："+str(Qshrimp)
    psquid="價格："+str(squid)+"金幣/漲跌幅："+str(Qsquid)
    embed.add_field(name="🐟魚",value=pfish,inline=False)
    embed.add_field(name="🐠熱帶魚", value=ptropical_fish,inline=False)
    embed.add_field(name="🐡河豚",value=pblowfish,inline=False)
    embed.add_field(name="🦀螃蟹",value=pcrab,inline=False)
    embed.add_field(name="<:magikarp:743296027381071875>鯉魚王",value=pmagikarp,inline=False)
    embed.add_field(name="🦈鯊魚",value=pshark,inline=False)
    embed.add_field(name="🦐蝦子",value=pshrimp,inline=False)
    embed.add_field(name="🦑花枝",value=psquid,inline=False)
    await message.channel.send(embed=embed)

  @commands.command()#改好了
  async def 魚市結算(self,message):
    if(datetime.now().hour >= 23):
      if(message.author.id == 550907252970749952 or message.author.id == 559306021734973470 or message.author.id == 598440593001021471):
        pass
      else:
        return
    Market = read_file("Fish_market")
    Mdate = Market["date"]
    date = datetime.now().day
    if(date != Mdate):
      pass
    else:
      await message.channel.send("今日已結算過了")
      return
    #price
    fish = Market["fish"][0]
    tropical_fish = Market["tropical_fish"][0]
    blowfish = Market["blowfish"][0]
    crab = Market["crab"][0]

    magikarp = Market["magikarp"][0]
    shark = Market["shark"][0]
    shrimp = Market["shrimp"][0]
    squid = Market["squid"][0]
    #amount
    Afish = Market["fish"][2]
    Atropical_fish = Market["tropical_fish"][2]
    Ablowfish = Market["blowfish"][2]
    Acrab = Market["crab"][2]

    Amagikarp = Market["magikarp"][2]
    Ashark = Market["shark"][2]
    Ashrimp = Market["shrimp"][2]
    Asquid = Market["squid"][2]
    #before
    Bfish = Market["fish"][3]
    Btropical_fish = Market["tropical_fish"][3]
    Bblowfish = Market["blowfish"][3]
    Bcrab = Market["crab"][3]

    Bmagikarp = Market["magikarp"][3]
    Bshark = Market["shark"][3]
    Bshrimp = Market["shrimp"][3]
    Bsquid = Market["squid"][3]
    #fish
    if(Afish>Bfish):
      fishadd = random.randint(-2,0)
    else:
      fishadd = random.randint(-2,2)
    if((fish+fishadd)<1):
      fishadd = 1-fish
      fish = 1
    elif((fish+fishadd)>=10):
      fishadd = 10-fish
      fish = 10
    else:
      fish += fishadd
      
    #tropical_fish
    if(Atropical_fish>Btropical_fish):
      tropical_fishadd = random.randint(-2,0)
    else:
      tropical_fishadd = random.randint(-2,2)
    if((tropical_fish+tropical_fishadd)<10):
      tropical_fishadd = 10-tropical_fish
      tropical_fish = 10
    elif((tropical_fish+tropical_fishadd)>=20):
      tropical_fishadd = 20-tropical_fish
      tropical_fish = 20
    else:
      tropical_fish += tropical_fishadd
    
    #blowfish
    if(Ablowfish>Bblowfish):
      blowfishadd = random.randint(-2,0)
    else:
      blowfishadd = random.randint(-2,2)
    if((blowfish+blowfishadd)<10):
      blowfishadd = 10-blowfish
      blowfish = 10
    elif((blowfish+blowfishadd)>=20):
      blowfishadd = 20-blowfish
      blowfish = 20
    else:
      blowfish += blowfishadd
    
    #crab
    if(Acrab>Bcrab):
      crabadd = random.randint(-2,0)
    else:
      crabadd = random.randint(-2,2)
    if((crab+crabadd)<10):
      crabadd = 10-crab
      crab = 10
    elif((crab+crabadd)>=30):
      crabadd = 30-crab
      crab = 30
    else:
      crab += crabadd

    #magikarp
    if(Amagikarp>Bmagikarp):
      magikarpadd = random.randint(0,1)
    else:
      magikarpadd = random.randint(-1,1)
    if((magikarp+magikarpadd)<5):
      magikarpadd = 5-magikarp
      magikarp = 5
    elif((magikarp+magikarpadd)>=10):
      magikarpadd = 10-magikarp
      magikarp = 10
    else:
      magikarp += magikarpadd

    #shark
    if(Ashark>Bshark):
      sharkadd = random.randint(-1,0)
    else:
      sharkadd = random.randint(-1,1)
    if((shark+sharkadd)<1):
      sharkadd = 1-shark
      shark = 1
    elif((shark+sharkadd)>=5):
      sharkadd = 5-shark
      shark = 5
    else:
      shark += sharkadd
    
    #shrimp
    if(Ashrimp>Bshrimp):
      shrimpadd = random.randint(-1,0)
    else:
      shrimpadd = random.randint(-1,1)
    if((shrimp+shrimpadd)<1):
      shrimpadd = 1-shrimp
      shrimp = 1
    elif((shrimp+shrimpadd)>=5):
      shrimpadd = 5-shrimp
      shrimp = 5
    else:
      shrimp += shrimpadd
    
    #squid
    if(Asquid>Bsquid):
      squidadd = random.randint(-1,0)
    else:
      squidadd = random.randint(-1,1)
    if((squid+squidadd)<1):
      squidadd = 1-squid
      squid = 1
    elif((squid+squidadd)>=5):
      squidadd = 5-squid
      squid = 5
    else:
      squid += squidadd

    #change
    Market["fish"][0] = fish
    Market["tropical_fish"][0] = tropical_fish
    Market["blowfish"][0] = blowfish
    Market["crab"][0] = crab
    Market["magikarp"][0] = magikarp
    Market["shark"][0] = shark
    Market["shrimp"][0] = shrimp
    Market["squid"][0] = squid
    #quote change
    Market["fish"][1] = fishadd
    Market["tropical_fish"][1] = tropical_fishadd
    Market["blowfish"][1] = blowfishadd
    Market["crab"][1] = crabadd
    Market["magikarp"][1] = magikarpadd
    Market["shark"][1] = sharkadd
    Market["shrimp"][1] = shrimpadd
    Market["squid"][1] = squidadd
    #amount
    Market["fish"][2] = 0
    Market["tropical_fish"][2] = 0
    Market["blowfish"][2] = 0
    Market["crab"][2] = 0
    Market["magikarp"][2] = 0
    Market["shark"][2] = 0
    Market["shrimp"][2] = 0
    Market["squid"][2] = 0
    #before
    Market["fish"][3] = Afish
    Market["tropical_fish"][3] = Atropical_fish
    Market["blowfish"][3] = Ablowfish
    Market["crab"][3] = Acrab
    Market["magikarp"][3] = Amagikarp
    Market["shark"][3] = Ashark
    Market["shrimp"][3] = Ashrimp
    Market["squid"][3] = Asquid
    
    Market["date"] = datetime.now().day
    write_file("Fish_market",Market)
    await message.channel.send("成功")

    new_channel = self.bot.get_channel(889767325845295164)
    await new_channel.send("```"+str(Market)+"```")
  
  @commands.command()#改好了
  async def 販售(self,message,thing:str,amount:int):
    if(message.channel.id != 897418740684165120):
      await message.channel.send("請至 <#897418740684165120>")
      return
    ID = str(message.author.id)
    User = get_user(ID)
    fishing = read_file("fishing")
    Market = read_file("Fish_market")
    Thing = thing
    which_money = 0
    # 0交換點數 1石頭 2金幣 3中階經驗藥水 
    if(thing == "魚"):
      thing = "fish"
    elif(thing == "熱帶魚"):
      thing = "tropical_fish"
    elif(thing == "河豚"):
      thing = "blowfish"
    elif(thing == "螃蟹"):
      thing = "crab"
    elif(thing == "鯉魚王"):
      which_money = 3
      thing = "magikarp"
      price = Market[thing][0]
      if(amount%price!=0):
        await message.channel.send("數量不為"+str(price)+"之倍數")
        return 
    elif(thing == "鯊魚"):
      which_money = 1
      thing = "shark"
    elif(thing == "蝦子"):
      thing = "shrimp"
    elif(thing == "花枝"):
      which_money = 2
      thing = "squid"
    else:
    	await message.channel.send('您沒有這種魚啦')
    	return
    #copy
    if("tub" in str(User)):
      pass
    else:
      await message.channel.send("您目前沒有桶子")
      return
    tub = User["tub"][0]
    space = fishing[tub][0]
    tub = fishing[tub][1]
    i = 1
    fish = 0
    while(i<=space):
      F = User["tub"][i]
      if(F == thing):
        fish +=1
        User["tub"][i] = ""
      if(fish == amount):
        break
      i+=1
    
    if(thing not in str(Market)):
      return
    price = Market[thing][0]
    # 0交換點數 1石頭 2金幣 3中階經驗藥水 
    if(which_money == 0):
      User["re"]+=price*fish
    elif(which_money == 1):
      if("stone" not in str(User.keys())):
        await message.channel.send("請先更新")
        return 
      User["stone"]+=price*fish
    elif(which_money == 2):
      User["pis"]+=price*fish
    elif(which_money == 3):
      if("good_potion" not in str(User.keys())):
        await message.channel.send("請先更新")
        return 
      User["good_potion"]+=int(fish/price)
    Market[thing][2] +=fish
    put_user(ID,User)
    write_file("Fish_market",Market)
    
    if(which_money == 0):
      await message.channel.send("販賣了"+str(fish)+"隻"+Thing+"，獲得了交換點數×"+str(price*fish))
    elif(which_money == 1):
      await message.channel.send("販賣了"+str(fish)+"隻"+Thing+"，獲得了石頭×"+str(price*fish))
    elif(which_money == 2):
      await message.channel.send("販賣了"+str(fish)+"隻"+Thing+"，獲得了金幣×"+str(price*fish))
    elif(which_money == 3):
      await message.channel.send("販賣了"+str(fish)+"隻"+Thing+"，獲得了中階經驗藥水×"+str(int(fish/price)))
  @commands.command()
  async def  情報分析(self,message):
    if(message.author.id == 550907252970749952 or message.author.id == 559306021734973470 or message.author.id == 598440593001021471):
      pass
    else:
      return
    Market = read_file("Fish_market")
    #price
    fish = Market["fish"][0]
    tropical_fish = Market["tropical_fish"][0]
    blowfish = Market["blowfish"][0]
    crab = Market["crab"][0]
    magikarp = Market["magikarp"][0]
    shark = Market["shark"][0]
    shrimp = Market["shrimp"][0]
    squid = Market["squid"][0]
    #quote change
    Qfish = Market["fish"][1]
    Qtropical_fish = Market["tropical_fish"][1]
    Qblowfish = Market["blowfish"][1]
    Qcrab = Market["crab"][1]
    Qmagikarp = Market["magikarp"][1]
    Qshark = Market["shark"][1]
    Qshrimp = Market["shrimp"][1]
    Qsquid = Market["squid"][1]
    #amount
    Mfish = Market["fish"][2]
    Mtropical_fish = Market["tropical_fish"][2]
    Mblowfish = Market["blowfish"][2]
    Mcrab = Market["crab"][2]
    Mmagikarp = Market["magikarp"][2]
    Mshark = Market["shark"][2]
    Mshrimp = Market["shrimp"][2]
    Msquid = Market["squid"][2]
    #before
    Bfish = Market["fish"][3]
    Btropical_fish = Market["tropical_fish"][3]
    Bblowfish = Market["blowfish"][3]
    Bcrab = Market["crab"][3]
    Bmagikarp = Market["magikarp"][3]
    Bshark = Market["shark"][3]
    Bshrimp = Market["shrimp"][3]
    Bsquid = Market["squid"][3]
    Date = str(datetime.now().year)+"/"+str(datetime.now().month)+"/"+str(datetime.now().day)
    embed = discord.Embed(title="今日魚市(情報分析)",description=Date,color=0xeee657,inline=False)
    
    pfish="價格："+str(fish)+"交換點數/漲跌幅："+str(Qfish)+"/購入數量："+str(Mfish)+"/昨日購入數量："+str(Bfish)
    ptropical_fish="價格："+str(tropical_fish)+"交換點數/漲跌幅："+str(Qtropical_fish)+"/購入數量："+str(Mtropical_fish)+"/昨日購入數量："+str(Btropical_fish)
    pblowfish="價格："+str(blowfish)+"交換點數/漲跌幅："+str(Qblowfish)+"/購入數量："+str(Mblowfish)+"/昨日購入數量："+str(Bblowfish)
    pcrab="價格："+str(crab)+"交換點數/漲跌幅："+str(Qcrab)+"/購入數量："+str(Mcrab)+"/昨日購入數量："+str(Bcrab)

    pmagikarp="價格："+str(magikarp)+"隻換一瓶中階經驗藥水/漲跌幅："+str(Qmagikarp)+"/購入數量："+str(Mmagikarp)+"/昨日購入數量："+str(Bmagikarp)
    pshark="價格："+str(shark)+"石頭/漲跌幅："+str(Qshark)+"/購入數量："+str(Mshark)+"/昨日購入數量："+str(Bshark)
    pshrimp="價格："+str(shrimp)+"交換點數/漲跌幅："+str(Qshrimp)+"/購入數量："+str(Mshrimp)+"/昨日購入數量："+str(Bshrimp)
    psquid="價格："+str(squid)+"金幣/漲跌幅："+str(Qsquid)+"/購入數量："+str(Msquid)+"/昨日購入數量："+str(Bsquid)
    embed.add_field(name="🐟魚",value=pfish,inline=False)
    embed.add_field(name="🐠熱帶魚", value=ptropical_fish,inline=False)
    embed.add_field(name="🐡河豚",value=pblowfish,inline=False)
    embed.add_field(name="🦀螃蟹",value=pcrab,inline=False)
    embed.add_field(name="<:magikarp:743296027381071875>鯉魚王",value=pmagikarp,inline=False)
    embed.add_field(name="🦈鯊魚",value=pshark,inline=False)
    embed.add_field(name="🦐蝦子",value=pshrimp,inline=False)
    embed.add_field(name="🦑花枝",value=psquid,inline=False)
    await message.channel.send(embed=embed)

  @commands.command()
  async def Bag(self,message):
    ID = str(message.author.id)
    User = get_user(ID)
    if("bag" not in str(User)):
      pass
    else:
      return
    User["bag1"] = ""
    User["bag2"] = ""
    User["bag3"] = ""
    User["bag4"] = ""
    User["bag5"] = ""
    User["level"] = ""
    User["experience"] = ""
    User["money"] = ""
    User["activity"] = ""
    put_user(ID,User)
    await message.channel.send("成功")
  @commands.command()
  async def stone_updata(self,message):
    if(message.author.id != 550907252970749952):
      return
    Market = read_file("Fish_market")
    Market["date"] = 8
    write_file("Fish_market",Market)
    
  
def setup(bot):
  bot.add_cog(Synchronize(bot))
