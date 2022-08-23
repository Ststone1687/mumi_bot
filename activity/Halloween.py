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
from skill import fight
from io import StringIO
def power(ATK:int,DEF:int,SPD:int,HP:int,Lv:int):
  P = (2*ATK+2*DEF+2*SPD+HP+2*Lv)*3+((HP-Lv+ATK+DEF*2)/2)*(SPD)/100
  return int(P)
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
def level_up(lv:int,exp:int,add:int,HP:int,ATK:int,DEF:int,SPD:int,h:int,a:int,d:int,s:int):
  exp +=add
  while((exp/100)>=lv and lv<100):
    exp-=lv*100
    lv+=1
    HP += h
    DEF += d
    ATK += a
    SPD += s 
  return lv,exp,HP,ATK,DEF,SPD
  
class Halloween(Cog_Extension):
  @commands.command(aliases=["糖果總覽","糖果總懶","糖果總攬","糖果","糖果資訊"])
  async def Halloween_money(self,message):
    with open("Halloween.json","r",encoding="utf-8")as f:
      Halloween = json.load(f)
    ID = str(message.author.id)
    User = get_user(ID)
    
    if(User["activity"] != "Halloween" or User["money"] == ""):
      User["money"] = 0
    level = 0
    statue = User["statue"]
    for i in Halloween["level"]:
      if(statue[3]>=i):
        level+=1
    msg = "當前等級："+str(level)+"/擊敗鬼魂數量："+str(statue[3])
    embed = discord.Embed(title=str(message.author)+"-糖果總覽-2021萬聖節活動",description=msg,color=0xeee657)
    embed.add_field(name="持有糖果數：", value=User["money"], inline=False)
    show="(1)石頭×100：10000糖果\n(2)角色重設券：5000糖果\n(3)裝備「南瓜燈」：2500糖果\n(4)裝備「吸血鬼披風」：2500糖果\n(5)裝備「木乃伊繃帶」：2500糖果\n(6)裝備「科學怪人的大腦」：2500糖果\n(7)石頭×10：1200糖果\n(8)中階經驗藥水：250糖果\n(9)經驗藥水：150糖果\n(10)必中券：90糖果\n(11)通行券：15糖果\n(12)交換點數：1糖果\n"
    embed.add_field(name="可用糖果兌換的商品：", value=show, inline=False)
    embed.set_footer(text="若需用糖果兌換商品請用\"糖果交換 商品編號 數量\"")
    await message.channel.send(embed=embed)
  @commands.command(aliases=["墓地探索","牧地探索","目的探索","牧帝嘆鎖"])
  async def Halloween_explore(self,message):
    if(message.channel.id!=902175507334963230):
      return 
    with open("Halloween.json","r",encoding="utf-8")as f:
      Halloween = json.load(f)
    ID = str(message.author.id)
    User = get_user(ID)
    if(User['new'] != "2.1.3.1"):
      await message.channel.send("請先完成更新")
      return 
    if(User["activity"] != "Halloween" or User["money"] == ""):
      User["money"] = 0
      User["activity"] = "Halloween"
      User["statue"] = [0,0,0,0,0]#ghost blood type how_much
    statue = User["statue"]
    if(statue[0]!=0):
      await message.channel.send("您現在被鬼魂纏身中，無法脫身")
      return 
    level = 0
    for i in Halloween["level"]:
      if(statue[3]>=i):
        level+=1
    Ran = random.randint(1,100)
    msg = ""
    if(Ran<=5 and level>=7):
      add = random.randint(Halloween["ex"][level-1][1][0],Halloween["ex"][level-1][1][1])
      User["stone"] += add
      msg = "您探索了墓地後，發現了"+str(add)+"顆石頭，這是否代表著什麼呢？"
    elif(Ran<=55):
      add = random.randint(Halloween["ex"][level-1][0][0],Halloween["ex"][level-1][0][1])
      User["money"] += add
      msg = "您探索了墓地後，發現了"+str(add)+"顆糖果，糖果...？"
    elif(Ran<=80):
      add = random.randint(1,level*10)
      User["point"] += add
      msg = "您探索了墓地後，在地板上發現了"+str(add)+"姆咪幣，姆咪姆咪心動動♪"
    else:
      msg = "您撲了一個空，什麼也沒找到"
    put_user(ID,User)
    await message.channel.send(msg)
  @commands.command(aliases=["墓地冒險","牧地冒險","目的冒險","穆蒂貿蜆"])
  async def Halloween_adventure(self,message):
    if(message.channel.id!=902175507334963230):
      return 
    with open("Halloween.json","r",encoding="utf-8")as f:
      Halloween = json.load(f)
    ID = str(message.author.id)
    User = get_user(ID)
    if(User['new'] != "2.1.3.1"):
      await message.channel.send("請先完成更新")
      return 
    if(User["activity"] != "Halloween" or User["money"] == ""):
      User["money"] = 0
      User["activity"] = "Halloween"
      User["statue"] = [0,0,0,0,0]#ghost blood type how_much
    statue = User["statue"]
    if(statue[0]!=0):
      await message.channel.send("您現在被鬼魂纏身中，無法脫身")
      return 
    level = 0
    for i in Halloween["level"]:
      if(statue[3]>=i):
        level+=1
    Ran = random.randint(1,100)
    msg = ""
    if(Ran<=5 and level>=7):
      add = random.randint(Halloween["ad"][level-1][1][0],Halloween["ad"][level-1][1][1])
      User["stone"] += add
      msg = "您探索了墓地後，發現了"+str(add)+"顆石頭，這是否代表著什麼呢？"
    elif(Ran<=40):
      add = random.randint(Halloween["ad"][level-1][0][0],Halloween["ad"][level-1][0][1])
      User["money"] += add
      msg = "您探索了墓地後，發現了"+str(add)+"顆糖果，糖果...？"
    elif(Ran<=55):
      add = random.randint(1,level*10)
      User["point"] += add
      msg = "您探索了墓地後，在地板上發現了"+str(add)+"姆咪幣，姆咪姆咪心動動♪"
    elif(Ran<=70):
      msg = "您撲了一個空，什麼也沒找到"
    else:
      r = random.randint(0,11)
      blood = Halloween["ghost"][r][2]
      name = Halloween["ghost"][r][0]
      User["statue"][0] = 1
      User["statue"][1] = blood
      User["statue"][2] = r
      msg = "您被鬼魂「"+name+"」纏身了，不開始戰鬥的話你似乎就只能永遠停留在這裡了...\n似乎有什麼東西將您引導至了<#902175569242914847>"
      ATK = Halloween["ghost"][r][3]
      DEF = Halloween["ghost"][r][4]
      SPD = Halloween["ghost"][r][5]
      HP = Halloween["ghost"][r][2]
      LV = Halloween["ghost"][r][1]
      Power = power(ATK,DEF,SPD,HP,LV)
      embed = discord.Embed(title=name,description=name,color=0xeee657)
      embed.add_field(name="戰鬥力:", value=str(Power), inline=False)
      embed.add_field(name="等級:", value=str(LV), inline=False)
      embed.add_field(name="血量:", value=str(HP)+"/"+str(HP), inline=False)
      embed.add_field(name="攻擊力:", value=str(ATK), inline=False)
      embed.add_field(name="防禦力:", value=str(DEF), inline=False)
      embed.add_field(name="速度:", value=str(SPD), inline=False)
      await message.channel.send(embed=embed)
    put_user(ID,User)
    await message.channel.send(msg)
  @commands.command(aliases=["攻擊鬼魂","公雞鬼魂","供疾詭渾"])
  async def Halloween_attack(self,message):
    if(message.channel.id!=902175569242914847):
      return 
    with open("Halloween.json","r",encoding="utf-8")as f:
      Halloween = json.load(f)
    ID = str(message.author.id)
    User = get_user(ID)
    if(User['new'] != "2.1.3.1"):
      await message.channel.send("請先完成更新")
      return 
    if(User["activity"] != "Halloween" or User["money"] == ""):
      User["money"] = 0
      User["activity"] = "Halloween"
      User["statue"] = [0,0,0,0,0]#ghost blood type how_much
    statue = User["statue"]
    if(statue[0]!=1):
      await message.channel.send("似乎沒有鬼魂可以讓你攻擊呢...")
      return 
    now_role = User["now_role"]
    now_role = "role"+str(now_role)
    if(now_role in str(User.keys())):
      if(User[now_role][0] == 0):
        await message.channel.send("您沒有設定該角色")
        return
      with open("data.json","r",encoding="utf-8")as f:
        Data = json.load(f)
      CardId = User[now_role][0]
      CardName = Data["card"][CardId-2001]
      LV = User[now_role][1]
      EXP = User[now_role][2]
      HP = User[now_role][3]
      ATK = User[now_role][4]
      DEF = User[now_role][5]
      SPD = User[now_role][6]
      ph = User[now_role][7]
      pa = User[now_role][8]
      pd = User[now_role][9]
      ps = User[now_role][10]
      arm1 = User[now_role][11]
      skt1 = User[now_role][12]
      skn1 = User[now_role][13]
      Sname = Halloween["ghost"][statue[2]][0]
      Slv = Halloween["ghost"][statue[2]][1]
      Shp = statue[1]
      Satk = Halloween["ghost"][statue[2]][3]
      Sdef = Halloween["ghost"][statue[2]][4]
      Sspd = Halloween["ghost"][statue[2]][5]
      Cdp = 1
      if(datetime.now().hour==0 or datetime.now().hour==8):
        Cdp = 0.75
      elif(datetime.now().hour==1 or datetime.now().hour==7):
        Cdp = 0.5
      elif(datetime.now().hour==2 or datetime.now().hour==6):
        Cdp = 0.4
      elif(datetime.now().hour==3 or datetime.now().hour==5):
        Cdp = 0.3
      elif(datetime.now().hour==4):
        Cdp = 0.1
      elif(datetime.now().hour==11 or datetime.now().hour==12):
        Cdp = 0.25
      Slv = int(Slv*Cdp)
      Satk = int(Satk*Cdp)
      Sdef = int(Sdef*Cdp)
      Sspd = int(Sspd*Cdp)
      L,co,who,hp1,hp2= fight(CardName,LV,HP,ATK,DEF,SPD,Sname,Slv,Shp,Satk,Sdef,Sspd,1,1,arm1,0,skt1,skn1,0,0)
      statue[1] -= int(hp2)
      if(statue[1]<=0):
        statue[0] = 0
        statue[1] = 0
        statue[2] = 0
        statue[3] +=1
      User["statue"] = statue
      if(who==1):
        one = CardName+"獲勝"
      else:
        one = Sname+"獲勝"
      User[now_role][1],User[now_role][2],User[now_role][3],User[now_role][4],User[now_role][5],User[now_role][6]=level_up(LV,EXP,int(hp2/10),HP,ATK,DEF,SPD,ph,pa,pd,ps)
      put_user(ID,User)
      await message.channel.send(one+"\n"+CardName+"對"+Sname+"造成了"+str(hp2)+"點傷害\n"+"獲得了"+str(int(hp2/10))+"點經驗值\n鬼魂剩餘血量："+str(statue[1]))
      s = StringIO()
      s.write(L)
      s.seek(0)
      await message.channel.send(file=discord.File(s, filename="fight.txt"))
      put_user(ID,User)
    else:
      await message.channel.send("您沒有設定戰鬥角色")
      return 
  @commands.command(aliases=["糖果交換","糖果兌換"])
  async def Halloween_money_change(self,message,number:int,much:int):
    with open("Halloween.json","r",encoding="utf-8")as f:
      Halloween = json.load(f)
    ID = str(message.author.id)
    User = get_user(ID)
    if(number > 12 or number <= 0):
      await message.channel.send("商品編號輸入錯誤")
      return
    if(much <= 0):
      await message.channel.send("數量輸入錯誤")
      return
    if(User['new'] != "2.1.3.1"):
      await message.channel.send("請先完成更新")
      return 
    if(User["activity"] != "Halloween" or User["money"] == ""):
      User["money"] = 0
      User["activity"] = "Halloween"
      User["statue"] = [0,0,0,0,0]#ghost blood type how_much
    statue = User["statue"]
    money = User["money"]
    if(number == 1 and money>=(10000*much)):#石頭×100	10000
      if(User['stone']==""):
        User['stone'] = 0
      User["stone"] += 100*much
      User["money"] -= 10000*much
    elif(number == 2 and money>=(5000*much)):#角色重設券	5000
      if("role_reset" in str(User.keys())):
        User["role_reset"] += much
      else:
        User["role_reset"] = much
      User["money"] -= 5000*much
    elif(number == 3 and money>=2500):#裝備「南瓜燈」	2500
      if(much != 1):
        await message.channel.send("裝備商品一次只能購買一個")
        return
      arms = 20001
      i = 1
      f = "t"
      while(i<=10 and f == "t"):
        if(User["arms"][str(i)][0] == 0):
          User["arms"][str(i)][0] = arms
          User["arms"][str(i)][2] = 1
          User["arms"][str(i)][3] = 100001
          f = "f"
        i += 1
      if(f == "t"):
        await message.channel.send("裝備包包無空間，無法兌換")
        return
      User["money"] -= 2500
    elif(number == 4 and money>=2500):#裝備「吸血鬼披風」	2500
      if(much != 1):
        await message.channel.send("裝備商品一次只能購買一個")
        return
      arms = 20002
      i = 1
      f = "t"
      while(i<=10 and f == "t"):
        if(User["arms"][str(i)][0] == 0):
          User["arms"][str(i)][0] = arms
          User["arms"][str(i)][2] = 2
          User["arms"][str(i)][3] = 200001
          f = "f"
        i += 1
      if(f == "t"):
        await message.channel.send("裝備包包無空間，無法兌換")
        return
      User["money"] -= 2500
    elif(number == 5 and money>=2500):#裝備「木乃伊繃帶」	2500
      if(much != 1):
        await message.channel.send("裝備商品一次只能購買一個")
        return
      arms = 20003
      i = 1
      f = "t"
      while(i<=10 and f == "t"):
        if(User["arms"][str(i)][0] == 0):
          User["arms"][str(i)][0] = arms
          User["arms"][str(i)][2] = 3
          User["arms"][str(i)][3] = 300001
          f = "f"
        i += 1
      if(f == "t"):
        await message.channel.send("裝備包包無空間，無法兌換")
        return
      User["money"] -= 2500
    elif(number == 6 and money>=2500):#裝備「科學怪人的大腦」	2500
      if(much != 1):
        await message.channel.send("裝備商品一次只能購買一個")
        return
      arms = 20004
      i = 1
      f = "t"
      while(i<=10 and f == "t"):
        if(User["arms"][str(i)][0] == 0):
          User["arms"][str(i)][0] = arms
          User["arms"][str(i)][2] = 1
          User["arms"][str(i)][3] = 100002
          f = "f"
        i += 1
      if(f == "t"):
        await message.channel.send("裝備包包無空間，無法兌換")
        return
      User["money"] -= 2500
    elif(number == 7 and money>=(1200*much)):#石頭×10	1200
      if(User['stone']==""):
        User['stone'] = 0
      User["stone"] += 10*much
      User["money"] -= 1200*much
    elif(number == 8 and money>=(250*much)):#中階經驗藥水	250
      if("good_potion" in str(User.keys())):
        User["good_potion"] += much
      else:
        User["good_potion"] = much
      User["money"] -= 250*much
    elif(number == 9 and money>=(150*much)):#經驗藥水	150
      if("exp_potion" in str(User.keys())):
        User["exp_potion"] += much
      else:
        User["exp_potion"] = much
      User["money"] -= 150*much
    elif(number == 10 and money>=(90*much)):#必中券	90
      if(User['specialchange']==""):
        User['specialchange'] = 0
      User["specialchange"] += much
      User["money"] -= 90*much
    elif(number == 11 and money>=(15*much)):#通行券	15
      User["m_pass"] += much
      User["money"] -= 15*much
    elif(number == 12 and money>=(1*much)):#交換點數	1
      User["re"] += much
      User["money"] -= much
    else:
      await message.channel.send("持有的糖果數不足")
      return
    put_user(ID,User)
    await message.channel.send("兌換成功")
  @commands.command(aliases=["管你什麼鬼魂的，我才不怕呢","來吧！鬼魂阿，出來單挑吧！","鬼魂？","鬼魂","鬼魂在ㄇ"])
  async def Halloween_come_on(self,message):
    if(datetime.now().hour <11 or datetime.now().hour >=13):
      return 
    if(message.channel.id!=902175569242914847):
      return
    with open("Halloween.json","r",encoding="utf-8")as f:
      Halloween = json.load(f)
    ID = str(message.author.id)
    User = get_user(ID)
    if(User['new'] != "2.1.3.1"):
      await message.channel.send("請先完成更新")
      return 
    if(User["activity"] != "Halloween" or User["money"] == ""):
      User["money"] = 0
      User["activity"] = "Halloween"
      User["statue"] = [0,0,0,0,0]#ghost blood type how_much
    statue = User["statue"]
    if(statue[0]!=0):
      await message.channel.send("您現在被鬼魂纏身中，無法脫身")
      return 
    level = 0
    msg = ""
    r = random.randint(0,11)
    blood = Halloween["ghost"][r][2]
    name = Halloween["ghost"][r][0]
    User["statue"][0] = 1
    User["statue"][1] = blood
    User["statue"][2] = r
    msg = "您被鬼魂「"+name+"」纏身了，不開始戰鬥的話你似乎就只能永遠停留在這裡了...\n似乎有什麼東西將您引導至了<#902175569242914847>"
    ATK = Halloween["ghost"][r][3]
    DEF = Halloween["ghost"][r][4]
    SPD = Halloween["ghost"][r][5]
    HP = Halloween["ghost"][r][2]
    LV = Halloween["ghost"][r][1]
    Power = power(ATK,DEF,SPD,HP,LV)
    embed = discord.Embed(title=name,description=name,color=0xeee657)
    embed.add_field(name="戰鬥力:", value=str(Power), inline=False)
    embed.add_field(name="等級:", value=str(LV), inline=False)
    embed.add_field(name="血量:", value=str(HP)+"/"+str(HP), inline=False)
    embed.add_field(name="攻擊力:", value=str(ATK), inline=False)
    embed.add_field(name="防禦力:", value=str(DEF), inline=False)
    embed.add_field(name="速度:", value=str(SPD), inline=False)
    await message.channel.send(embed=embed)
    put_user(ID,User)
    await message.channel.send(msg)
  @commands.command(aliases=["不給糖就搗蛋","不給糖我還是沒辦法搗蛋","糖果拿來"])
  async def Halloween_trick_or_treat(self,message,who:str):
    if(message.channel.id!=902175706799280168):
      return
    ID = str(message.author.id)
    who = who.strip('<@!>')
    if(ID==who):
      await message.channel.send("抖M...？")
      return
    User = get_user(ID)
    User2 = get_user(who)
    if(User['new'] != "2.1.3.1"):
      await message.channel.send("請先完成更新")
      return
    if(User2['new'] != "2.1.3.1"):
      await message.channel.send("對方似乎未完成更新")
      return
    if(User["activity"] != "Halloween" or User["money"] == ""):
      User["money"] = 0
      User["activity"] = "Halloween"
      User["statue"] = [0,0,0,0,0]#ghost blood type how_much
    if(User2["activity"] != "Halloween" or User2["money"] == ""):
      User2["money"] = 0
      User2["activity"] = "Halloween"
      User2["statue"] = [0,0,0,0,0]#ghost blood type how_much
    ran = random.randint(-2,10)
    msg = ""
    if(User2["money"]>ran and ran>0):
      User2["money"] -= ran
      User["money"] += ran
      msg = "<@"+ID+">從<@"+who+">得到了糖果x"+str(ran)
    else:
      msg = "🥚🔨"
    put_user(ID,User)
    put_user(who,User2)
    await message.channel.send(msg)
  @commands.command(aliases=["魔王設定傑克"])
  async def Halloween_set_boss(self,message,mode:str):
    if (message.author.id == 598440593001021471 or message.author.id == 598440593001021471 or message.author.id == 550907252970749952 or message.author.id == 511246631073611808 or message.author.id == 480747560793931778 or message.author.id == 352066968750260245 or message.author.id == 544552665204654080 or message.author.id == 597692502346301452):
      pass
    else:
      await message.channel.send('<@' + str(message.author.id) + '> 失敗')
      return
    with open("bossData.json","r",encoding="utf-8")as f:
      bossData = json.load(f)
    if(mode == "極"):
      DP = 1
    elif(mode == "強"):
      DP = 0.75
    elif(mode == "中"):
      DP = 0.5
    elif(mode == "弱"):
      DP = 0.25
    else:
      await message.channel.send("模式選擇錯誤")
      return
    boss = {}
    boss["fight"] = "t"
    boss["boss"] = "傑克"
    name = "傑克"
    boss["type"] = mode
    boss["LV"] = int(bossData[name][1]*DP)
    boss["HP"] = int(bossData[name][2]*DP)
    boss["ATK"] = int(bossData[name][3]*DP)
    boss["DEF"] = int(bossData[name][4]*DP)
    boss["SPD"] = int(bossData[name][5]*DP)
    boss["rank"] = {}
    boss["time"] = 0
    boss["cardS"] = bossData[name][6]
    boss["cardE"] = bossData[name][7]
    boss["reward"] = bossData["reward"][mode]
    write_file("boss",boss)
    await message.channel.send("成功")
    embed = discord.Embed(title=str(boss["boss"])+"（"+str(boss["type"])+"）",description="剩餘血量："+str(boss["HP"]),color=0xeee657)
    embed.add_field(name="戰鬥力：", value=int(power(boss["ATK"],boss["DEF"],boss["SPD"],boss["HP"],boss["LV"])), inline=False)
    embed.add_field(name="LV：", value=boss["LV"], inline=False)
    embed.add_field(name="HP：", value=boss["HP"], inline=False)
    embed.add_field(name="ATK：", value=boss["ATK"], inline=False)
    embed.add_field(name="DEF：", value=boss["DEF"], inline=False)
    embed.add_field(name="SPD：", value=boss["SPD"], inline=False)
    embed.set_thumbnail(url=bossData[name][0])
    embed.set_footer(text="開放時間：22:00~22:30")
    await message.channel.send(embed=embed)

def setup(bot):
  bot.add_cog(Halloween(bot))