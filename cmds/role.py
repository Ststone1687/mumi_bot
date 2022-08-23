import discord
from discord.ext import commands
from datetime import datetime
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

def damage(MLv:int,MATK:int,YDEF:int,MSPD:int,DP:int):
  Ran = random.randint(50,150)
  Ran = Ran/100
  Dam = ((((2*MLv+10)/250)*(MATK/YDEF)*(Ran))*(MLv+MSPD+20)/4*DP)+random.randint(0,2)
  #print(Dam)
  return Dam,Ran
  #(((2*MLv+10)/250)*(MATK/YDEF)*(Ran))*(MLv+MSPD+20)/4*DP

def stevetk(MLv:int,YLv:int,MATK:int,YDEF:int,MSPD:int,YSPD:int):
  Ra = 0.3
  Rb = 0.6
  Dam = (math.log(MLv+1)/math.log(10))*MATK*(math.log(Ra+1)/math.log(10))*(math.log(MSPD)/math.log(10))-(math.log(YLv+1)/math.log(10))*YDEF*(math.log(Rb+1)/math.log(10))*(math.log(YSPD)/math.log(10))
  #  logL+1 * A*log(R+1) * logS  -  logYL+1 * YDlog(YR+1) *logYS       				

def sentence(A:int,Atk:str,Def:str,R:float):
  if(A == 0):
    return Def+"閃避了"+Atk+"的攻擊"
  elif(R>=1.25):
    return "暴擊！ "+Atk+"對"+Def+"造成了"+str(A)+"點傷害"
  else:
    return Atk+"對"+Def+"造成了"+str(A)+"點傷害"

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
  
def power(ATK:int,DEF:int,SPD:int,HP:int,Lv:int):
  P = (2*ATK+2*DEF+2*SPD+HP+2*Lv)*3+((HP-Lv+ATK+DEF*2)/2)*(SPD)/100
  return int(P)
  #(2*ATK+2*DEF+2*SPD+HP+2*Lv)*3+((HP-Lv+ATK+DEF*2)/2)*(SPD)/100

def power_record(UserID:int,power:int,number:int):
  p_r = read_file("power_rank")
  if(str(UserID) not in str(p_r[str(number)].keys())):
    p_r[str(number)][str(UserID)] = power
  else:
    if(p_r[str(number)][str(UserID)] < power):
      p_r[str(number)][str(UserID)] = power
  if(number == 0):
    p_r["0"][str(UserID)] = power
  write_file("power_rank",p_r)

def arms(HP:int,ATK:int,DEF:int,SPD:int,number:int):
  with open("arms.json","r",encoding="utf-8")as f:
    data = json.load(f)
  L = data[str(number)]
  if("." in str(L[1])):
    HP *= L[1]
  else:
    HP += L[1]
  if("." in str(L[2])):
    ATK *= L[2]
  else:
    ATK += L[2]
  if("." in str(L[3])):
    DEF *= L[3]
  else:
    DEF += L[3]
  if("." in str(L[4])):
    SPD *= L[4]
  else:
    SPD += L[4]
  return int(HP),int(ATK),int(DEF),int(SPD)



class role(Cog_Extension):
  @commands.command(aliases=["設定角色","角色設定"],help="用來設定戰鬥角色，格式為[設定角色 設定位置 卡片名稱][ex:設定角色 1 雷姆](此意義為將角色1空間設定為雷姆卡片)")
  async def set_role(self,message,place:str,card:str):
    ID = str(message.author.id)
    if(check_user(ID)):
      User = get_user(ID)
      with open("NameData.json","r",encoding="utf-8")as f:
        NameData = json.load(f)
      with open("role.json","r",encoding = "utf-8")as f:
        Role = json.load(f)
      if(card not in str(NameData.keys())):
        await message.channel.send("搜尋不到此卡")
        return 
      CardID = NameData[card]
      CardList = User["card"]
      if(str(CardID) not in CardList):
        await message.channel.send("您未擁有此卡")
        return
      R = "role"+place
      if(R in str(User.keys())):
        T = User[R][0]
        if(T!=0):
          await message.channel.send("此空間已有設定角色")
          return
        if(str(CardID) not in str(Role.keys())):
          await message.channel.send("此卡未開放")
          return
        msg1 = await message.channel.send("您確定要將"+card+"設成戰鬥角色"+place+"嗎？（一旦設定成功，此位置將無法更動，且此卡將會從卡片包包中移除）")
        await msg1.add_reaction("⭕")
        await msg1.add_reaction("❌")
        def confirmCheck(reaction, user):
          if user != message.author:
            return
          else:
            if(str(reaction.emoji) == "⭕"):
              return "O"
            elif(str(reaction.emoji) == "❌"):
              return "X"
        try:
          user = await self.bot.wait_for("reaction_add", timeout=10, check = confirmCheck)
          if("⭕")in str(user):
            User["card"] = User["card"].replace(str(CardID)+",","")
            if(User["assistant"] == CardID):
              User["assistant"] = 0
            HP = random.randint(0,2)
            ATK = random.randint(0,2)
            DEF = random.randint(0,2)
            SPD = random.randint(0,2)
            User[R][0] = CardID
            User[R][1] = 1
            User[R][2] = 0
            User[R][3] = Role[str(CardID)]["HP"][0]+HP
            User[R][4] = Role[str(CardID)]["ATK"][0]+ATK
            User[R][5] = Role[str(CardID)]["DEF"][0]+DEF
            User[R][6] = Role[str(CardID)]["SPD"][0]+SPD
            User[R][7] = Role[str(CardID)]["HP"][HP+2]
            User[R][8] = Role[str(CardID)]["ATK"][ATK+2]
            User[R][9] = Role[str(CardID)]["DEF"][DEF+2]
            User[R][10] = Role[str(CardID)]["SPD"][SPD+2]
            put_user(ID,User)
            await message.channel.send("設定成功")
          else:
            await message.channel.send("取消成功")
            return
        except asyncio.TimeoutError:
          await message.channel.send("使用者回應逾時")
          return
      else:
        await message.channel.send("找不到此空間，此空間可能已使用或尚未獲得")
        return
    else:
      await message.channel.send("<@"+str(message.author.id)+"> 請先輸入 註冊 完成註冊<:mumi:609708401513070602>")
  @commands.command(aliases=["角色總覽","我的角色","角色總攬"],help="用來查看戰鬥角色能力資訊，格式為[角色總覽 角色位置][ex:角色總覽 1](此意義為查看角色1位置的戰鬥角色能力資訊)")
  async def roles(self,message,number:int):
    ID = str(message.author.id)
    if(check_user(ID)):
      pass
    else:
      await message.channel.send("<@"+str(message.author.id)+"> 請先輸入 註冊 完成註冊<:mumi:609708401513070602>")
      return
    User = get_user(ID)
    with open("data.json","r",encoding="utf-8")as f:
      Data = json.load(f)
    now_role = User["now_role"]
    now_role = "role"+str(number)
    if(now_role in str(User.keys())):
      if(User[now_role][0] == 0):
        await message.channel.send("您沒有設定該角色")
        return
      CardId = User[now_role][0]
      CardName = Data["card"][CardId-2001]
      LV = User[now_role][1]
      EXP = User[now_role][2]
      HP = User[now_role][3]
      ATK = User[now_role][4]
      DEF = User[now_role][5]
      SPD = User[now_role][6]
      if(User[now_role][11] != 0):
        HP,ATK,DEF,SPD = arms(HP,ATK,DEF,SPD,User[now_role][11])
      Power = power(ATK,DEF,SPD,HP,LV)
      embed = discord.Embed(title=CardName,description=str(message.author),color=0xeee657)
      embed.add_field(name="戰鬥力:", value=str(Power), inline=False)
      embed.add_field(name="等級:", value=str(LV)+"(經驗值:"+str(EXP)+")", inline=False)
      embed.add_field(name="血量:", value=str(HP), inline=False)
      embed.add_field(name="攻擊力:", value=str(ATK), inline=False)
      embed.add_field(name="防禦力:", value=str(DEF), inline=False)
      embed.add_field(name="速度:", value=str(SPD), inline=False)
      if(User[now_role][11] != 0):
        with open("arms.json","r",encoding="utf-8")as f:
          ARM = json.load(f)
        embed.add_field(name="裝備:", value=ARM[str(User[now_role][11])][0], inline=False)
      if(CardId==2126):#stevetk
        member = self.bot.get_guild(782593702455279616).get_member(480747560793931778)
        embed.set_thumbnail(url=member.avatar_url)
      elif(CardId==2125):#Ststone
        member = self.bot.get_guild(782593702455279616).get_member(550907252970749952)
        embed.set_thumbnail(url=member.avatar_url)
      elif(CardId==2128):#koyoto
        member = self.bot.get_guild(609019622162825216).get_member(597692502346301452)
        embed.set_thumbnail(url=member.avatar_url)
      else:
        embed.set_thumbnail(url=Data["link"][CardId-2001])
      await message.channel.send(embed=embed)
      p_r = read_file("power_rank")
      if(str(message.author.id) not in str(p_r[str(number)].keys())):
        p_r[str(number)][str(message.author.id)] = Power
      else:
        if(p_r[str(number)][str(message.author.id)] < Power):
          p_r[str(number)][str(message.author.id)] = Power
      write_file("power_rank",p_r)
    else:
      await message.channel.send("您沒有設定該角色")
      return 
  @commands.command(aliases=["測試傷害"],help="用來測試傷害。")
  async def damage_test(self,message,n1:str,lv1:int,hp1:int,atk1:int,def1:int,spd1:int,n2:str,lv2:int,hp2:int,atk2:int,def2:int,spd2:int,dp1:float,dp2:float):
    if(message.author.id != 550907252970749952):
      return
    list,L,who,h1,h2 = fight(n1,lv1,hp1,atk1,def1,spd1,n2,lv2,hp2,atk2,def2,spd2,dp1,dp2,0,0)
    C = 0
    SS = "`"
    while(C<L):
      SS+=str(list[C])+"\n"
      C+=1
    SS += "`"
    if(who==1):
      await message.channel.send(SS+"\n"+n1+"獲勝")
    else:
      await message.channel.send(SS+"\n"+n2+"獲勝")
  @commands.command(aliases=["史萊姆","攻擊史萊姆","史萊姆去死","討伐史萊姆"],help="可於各史萊姆地城使用，用於攻擊史萊姆")
  async def monster(self,message):
    ID = str(message.author.id)
    if(message.channel.id == 897669224879767562):
      Sname = "普通史萊姆"
      Slv = 5
      Shp = 100
      Satk = 50
      Sdef = 50
      Sspd = 50
    elif(message.channel.id == 897669121225945108):
      Sname = "攻擊型史萊姆"
      Slv = 10
      Shp = 100
      Satk = 250
      Sdef = 50
      Sspd = 50
    elif(message.channel.id == 897669146710515763):
      Sname = "防禦型史萊姆"
      Slv = 5
      Shp = 100
      Satk = 50
      Sdef = 250
      Sspd = 50
    elif(message.channel.id == 897669201177739294):
      Sname = "速度型史萊姆"
      Slv = 5
      Shp = 100
      Satk = 50
      Sdef = 50
      Sspd = 250
    elif(message.channel.id == 897669177576419349):
      Sname = "肉盾型史萊姆"
      Slv = 5
      Shp = 500
      Satk = 50
      Sdef = 50
      Sspd = 50
    if(check_user(ID)):
      pass
    else:
      await message.channel.send("<@"+str(message.author.id)+"> 請先輸入 註冊 完成註冊<:mumi:609708401513070602>")
      return
    User = get_user(ID)
    with open("role.json","r",encoding="utf-8")as f:
      RoleData = json.load(f)
    with open("data.json","r",encoding="utf-8")as f:
      Data = json.load(f)
    now_role = User["now_role"]
    now_role = "role"+str(now_role)
    if(now_role in str(User.keys())):
      if(User[now_role][0] == 0):
        await message.channel.send("您沒有設定該角色")
        return
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
      #普通型史萊姆 5 100 50 50 50
      #防禦型史萊姆 10 100 50 250 50
      #攻擊型史萊姆 10 100 250 50 50
      #速度型史萊姆 10 100 50 50 250
      #肉盾型史萊姆 10 500 50 50 50
      L,co,who,hp1,hp2= fight(CardName,LV,HP,ATK,DEF,SPD,Sname,Slv,Shp,Satk,Sdef,Sspd,1,1,arm1,0,skt1,skn1,0,0)
      C = 0
      #while(C<co and mode==1):
        #await message.channel.send("`"+L[C]+"`")
        #C+=1
      if(who==1):
        one = CardName+"獲勝"
      else:
        one = Sname+"獲勝"
      User[now_role][1],User[now_role][2],User[now_role][3],User[now_role][4],User[now_role][5],User[now_role][6]=level_up(LV,EXP,int(hp2/10),HP,ATK,DEF,SPD,ph,pa,pd,ps)
      put_user(ID,User)
      await message.channel.send(one+"\n"+CardName+"對"+Sname+"造成了"+str(hp2)+"點傷害\n"+"獲得了"+str(int(hp2/10))+"點經驗值")
      s = StringIO()
      s.write(L)
      s.seek(0)
      await message.channel.send(file=discord.File(s, filename="fight.txt"))
    else:
      await message.channel.send("您沒有設定戰鬥角色")
      return 
  @commands.command(aliases=["攻擊","討伐","攻擊魔王","討伐魔王","魔王去死","魔王","討伐討伐","討伐."],help="可於魔王塔使用，攻擊魔王")
  async def fight(self,message):
    boss = read_file("boss")
    if(message.channel.id != 897419836131512370):
      if(message.channel.id==707975903338299462):
        pass
      else:
        return
    if(datetime.now().hour != 14 or datetime.now().minute>=30):
      if(message.channel.id != 707975903338299462):
        await message.channel.send("現在不在討伐時間內")
        return
    if(boss["fight"]!="t"):
      await message.channel.send("現在不在討伐時間內")
      return
    ID = str(message.author.id)
    if(check_user(ID)):
      pass
    else:
      await message.channel.send("<@"+str(message.author.id)+"> 請先輸入 註冊 完成註冊<:mumi:609708401513070602>")
      return
    User = get_user(ID)
    with open("data.json","r",encoding="utf-8")as f:
      Data = json.load(f)
    boss = read_file("boss")
    with open("bossData.json","r",encoding="utf-8")as f:
      bossData = json.load(f)
    if("now_role" not in str(User.keys())):
      await message.channel.send("您沒有設定該角色")
      return
    now_role = User["now_role"]
    now_role = "role"+str(now_role)
    if("now_role" in str(User.keys()) and User[now_role][0] != 0):
      CardId = User[now_role][0]
      CardName = Data["card"][CardId-2001]
      LV = User[now_role][1]
      EXP = User[now_role][2]
      HP = User[now_role][3]
      ATK = User[now_role][4]
      DEF = User[now_role][5]
      SPD = User[now_role][6]
      arm1 = User[now_role][11]
      skt1 = User[now_role][12]
      skn1 = User[now_role][13]
      BLV = boss["LV"]
      BHP = boss["HP"]
      BATK = boss["ATK"]
      BDEF = boss["DEF"]
      BSPD = boss["SPD"]
      BNAME = boss["boss"]
      dp1 = 1
      if(CardId>=boss["cardS"] and CardId<=boss["cardE"]):
        dp1 = 1.25
      List,LEN,who,hp1,hp2=fight(CardName,LV,HP,ATK,DEF,SPD,BNAME,BLV,BHP,BATK,BDEF,BSPD,dp1,1,arm1,0,skt1,skn1,0,0)
      #傷害公式計算變化
      for i in range(10):
        if(hp2<bossData["change_data"][i][0]):
          hp2 = bossData["change_data"][i][1] + int(hp2*bossData["change_data"][i][2])
          break
      if(hp2>2150):
        hp2 = 2200
      ###
      boss["HP"] -= hp2
      BHP = boss["HP"]
      if(str(message.author.id)not in str(boss["rank"].keys())):
        boss["rank"][str(message.author.id)] = hp2
      else:
         boss["rank"][str(message.author.id)] += hp2
      END = 0
      if(BHP <=0):
        END = 1
        boss["fight"] = "f"
      boss["time"] = datetime.now().minute
      write_file("boss",boss)
      hhh = "<@"+str(message.author.id)+">對"+str(BNAME)+"造成了"+str(hp2)+"點傷害\n"
      stone = random.randint(1,20)
      if("stone" in str(User.keys()) and stone == 20 and BNAME == "Ststone"):
        if(User["stone"] == ""):
          User["stone"] = 0
        User["stone"] += 1
        await message.channel.send(hhh+"<@"+str(message.author.id)+">喔！您發現了一顆石頭")
      reward = random.randint(1,100)
      if(reward <= 5):
        User["pis"] += 5
        await message.channel.send(hhh+"<@"+str(message.author.id)+">喔！您發現了金幣×5")
      elif(reward <= 15):
        User["point"] += 50
        await message.channel.send(hhh+"<@"+str(message.author.id)+">喔！您發現了姆咪幣×50")
      elif(reward <= 20):
        User["point"] += 30
        await message.channel.send(hhh+"<@"+str(message.author.id)+">喔！您發現了姆咪幣×30")
      elif(reward <= 25):
        User["point"] += 20
        await message.channel.send(hhh+"<@"+str(message.author.id)+">喔！您發現了姆咪幣×20")
      elif(reward <= 30):
        User["point"] += 10
        await message.channel.send(hhh+"<@"+str(message.author.id)+">喔！您發現了姆咪幣×10")
      else:
        await message.channel.send(hhh)
      put_user(ID,User)
      write_file("boss",boss)
      if(boss["HP"]<=0):
        boss["HP"] = 0
      embed = discord.Embed(title=str(boss["boss"])+"（"+str(boss["type"])+"）傷害總覽",description="剩餘血量："+str(boss["HP"]),color=0xeee657)
      k = boss["rank"]
      c = sorted(k.items(), key=lambda x:x[1])
      i = 0
      K = len(k)
      show = ""
      while(K-i >0):
        show = show+"NO."+str(i+1)+" <@"+str(c[K-i-1][0])+">:"+str(c[K-i-1][1])+"\n"
        i+=1
      embed.add_field(name="排行榜", value=str(show), inline=False)
      if("url" in str(boss.keys())):
        embed.set_thumbnail(url=boss["url"])
      else:
        embed.set_thumbnail(url=bossData[BNAME][0])
      await message.channel.send(embed=embed)
      if(END == 1):
        await message.channel.send("魔王已擊敗，請通知管理人員來做確認")
    else:
      await message.channel.send("您沒有設定該角色")
      return
  @commands.command(aliases=["魔王塔設定","設定魔王","魔王設定"])
  async def set_boss(self,message,mode:str):
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
    R = random.randint(1,bossData["list"][0])
    boss = {}
    boss["fight"] = "t"
    boss["boss"] = bossData["list"][R]
    name = bossData["list"][R]
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
  @commands.command(aliases=["魔王塔獎勵","魔王獎勵"])
  async def boss_reward(self,message):
    if (message.author.id == 598440593001021471 or message.author.id == 598440593001021471 or message.author.id == 550907252970749952 or message.author.id == 511246631073611808 or message.author.id == 480747560793931778 or message.author.id == 352066968750260245 or message.author.id == 544552665204654080 or message.author.id == 597692502346301452):
      pass
    else:
      await message.channel.send('<@' + str(message.author.id) + '> 失敗')
      return
    boss = read_file("boss")
    if("rank" not in str(boss.keys())):
      await message.channel.send("找不到可頒發獎勵的資料")
      return
    lost = "f"
    if(boss["fight"] == "t"):
      if(datetime.now().minute >= 30 and datetime.now().hour >= 14):
        lost = "t"
      else:
        if(message.author.id != 550907252970749952):
          await message.channel.send("找不到可頒發獎勵的資料")
          return
        else:
          lost = "t"
    time = boss["time"]
    if(lost == "t"):
      reward = boss["reward"]["lost"]
    elif(time < 10):
      reward = boss["reward"]["10"]
    elif(time < 20):
      reward = boss["reward"]["20"]
    elif(time < 30):
      reward = boss["reward"]["30"]
    k = boss["rank"]
    c = sorted(k.items(), key=lambda x:x[1])
    K = len(k)
    i = 0
    HP = 0
    P = 0
    while(K>i):
      HP += c[K-i-1][1]
      if(int(c[K-i-1][1]) == 0):
        P += 1
      i += 1
    K -= P
    NameList = ""
    count = 0
    channel = self.bot.get_channel(897418210629021716)
    with open("randomcard.json", 'r', encoding='utf-8') as file:
      randomcard = json.load(file)
    with open("data.json", 'r', encoding='utf-8') as file:
      data = json.load(file)
    #稀有卡片
    amount = reward[3]
    while(amount>0):
      who = random.randint(1,HP)
      i = 0
      Chp = 0
      while(Chp<who):
        UserID = c[K-i-1][0]
        Chp += c[K-i-1][1]
        i += 1
      if(UserID in NameList):
        pass
      else:
        amount -= 1
        NameList += ","+UserID
        ran = randomcard["act"][0]
        add = random.randint(1,ran)
        add = str(randomcard["act"][add])
        t = get_user(UserID)
        showadd = ""
        if(add not in t["card"]):
          t["card"] += add+","
        else:
          shop = read_file("shop")
          if(add not in shop.keys()):
            shop[add] = 1
          else:
            shop[add] += 1
          write_file("shop",shop)
          t["re"] += 30
          showadd = "已擁有的卡將轉換成交換點數×30"
        put_user(UserID,t)
        await channel.send("<:mumi01:897429705832169512> 玩家<@" +str(UserID)+ ">從魔王討伐戰中獲得了`"+str(data["card"][int(add)-2001])+"` <:mumi01:897429705832169512> \n"+showadd)
        count += 1
        if(count == K):
          count = 0
          NameList = ""
    #特殊卡片
    amount = reward[2]
    while(amount>0):
      who = random.randint(1,HP)
      i = 0
      Chp = 0
      while(Chp<who):
        UserID = c[K-i-1][0]
        Chp += c[K-i-1][1]
        i += 1
      if(UserID in NameList):
        pass
      else:
        amount -= 1
        NameList += ","+UserID
        add = str(random.randint(boss["cardS"],boss["cardE"]))
        t = get_user(UserID)
        showadd = ""
        if(add not in t["card"]):
          t["card"] += add+","
        else:
          shop = read_file("shop")
          if(add not in shop.keys()):
            shop[add] = 1
          else:
            shop[add] += 1
          write_file("shop",shop)
          t["re"] += 30
          showadd = "已擁有的卡將轉換成交換點數×30"
        put_user(UserID,t)
        await channel.send("<:mumi01:897429705832169512> 玩家<@" +str(UserID)+ ">從魔王討伐戰中獲得了`"+str(data["card"][int(add)-2001])+"` <:mumi01:897429705832169512> \n"+showadd)
        count += 1
        if(count == K):
          count = 0
          NameList = ""
    #石頭
    amount = reward[1]
    while(amount>0):
      who = random.randint(1,HP)
      i = 0
      Chp = 0
      while(Chp<who):
        UserID = c[K-i-1][0]
        Chp += c[K-i-1][1]
        i += 1
      if(UserID in NameList):
        pass
      else:
        amount -= 1
        NameList += ","+UserID
        t = get_user(UserID)
        if(t["stone"] == ""):
          t["stone"] = 0
        t["stone"] += reward[0]
        put_user(UserID,t)
        await channel.send("<:mumi01:897429705832169512> 玩家<@" +str(UserID)+ ">從魔王討伐戰中獲得了`石頭×"+str(reward[0])+"` <:mumi01:897429705832169512> \n")
        count += 1
        if(count == K):
          count = 0
          NameList = ""
    boss = {"fight": "f"}
    write_file("boss",boss)
    await message.channel.send('成功，已頒發完所有獎勵')
  @commands.command(aliases=["使用通行券","通行券使用"],help="可用於進入史萊姆地城，格式為[使用通行券 地城名稱][ex:使用通行券 普通](地城名稱處可填入:普通、攻擊、防禦、速度、肉盾)")
  async def using_pass_ticket(self,message,where:str):
    ID = str(message.author.id)
    User = get_user(ID)
    if(User["m_pass"] > 0):
      User["m_pass"] -=1
    else:
      await message.channel.send("您未擁有通行券")
      return
    if(where == "普通"):
      new_role = self.bot.get_guild(782593702455279616).get_role(897670174965121034)
    elif(where == "攻擊"):
      new_role = self.bot.get_guild(782593702455279616).get_role(897670230602567711)
    elif(where == "防禦"):
      new_role = self.bot.get_guild(782593702455279616).get_role(897670271807406090)
    elif(where == "速度"):
      new_role = self.bot.get_guild(782593702455279616).get_role(897670270972735530)
    elif(where == "肉盾"):
      new_role = self.bot.get_guild(782593702455279616).get_role(897670260772180018)
    else:
      await message.channel.send("格式錯誤")
      return
    await message.author.add_roles(new_role)
    put_user(ID,User)
    await message.channel.send("成功")
  @commands.command(aliases=["石頭總覽","石頭總攬","石頭資訊總覽","石頭資訊"],help="可用來查看石頭數量及其相關道具數量")
  async def my_stone_info(self,message):
    ID = str(message.author.id)
    User = get_user(ID)
    embed = discord.Embed(title="石頭總覽",description=str(message.author),color=0xeee657)
    stone = User["stone"]
    if(stone == ""):
      stone = 0
    embed.add_field(name="石頭數量：", value=stone, inline=False)
    if("exp_potion" in str(User.keys()) and User["exp_potion"]>0):
      embed.add_field(name="經驗藥水：",value=User["exp_potion"],inline=False)
    if("good_potion" in str(User.keys()) and User["good_potion"]>0):
      embed.add_field(name="中階經驗藥水：",value=User["good_potion"],inline=False)
    if("role_reset" in str(User.keys()) and User["role_reset"]>0):
      embed.add_field(name="角色重設券：",value=User["role_reset"],inline=False)
    #if("role_relive" in str(User.keys()) and User["role_reset"]>0):
      #embed.add_field(name="角色轉生券：",value=User["role_relive"],inline=False)
    if(stone >= 5):
      embed.add_field(name="可交換的商品：經驗藥水", value="5顆石頭", inline=False)
    if(stone >= 10 and "role2" not in str(User.keys())):
      embed.add_field(name="可交換的商品：角色2空間", value="10顆石頭", inline=False)
    if(stone >= 50 and "role2" in str(User.keys()) and "role3" not in str(User.keys())):
      embed.add_field(name="可交換的商品：角色3空間", value="50顆石頭", inline=False)
    if(stone >= 100 and "role3" in str(User.keys()) and "role4" not in str(User.keys())):
      embed.add_field(name="可交換的商品：角色4空間", value="100顆石頭", inline=False)
    if(stone >= 200 and "role4" in str(User.keys()) and "role5" not in str(User.keys())):
      embed.add_field(name="可交換的商品：角色5空間", value="200顆石頭", inline=False)
    if(stone >= 400 and "role5" in str(User.keys()) and "role6" not in str(User.keys())):
      embed.add_field(name="可交換的商品：角色6空間", value="400顆石頭", inline=False)
    if(stone >= 100):
      embed.add_field(name="可交換的商品：角色重設券", value="100顆石頭", inline=False)
    #if(stone >= 1000):
      #embed.add_field(name="可交換的商品：角色轉生券", value="1000顆石頭", inline=False)
    await message.channel.send(embed=embed)
  @commands.command(aliases=["石頭交換","石頭兌換"],help="可用於交換特定道具，格式為[石頭交換 欲交換物品名稱 數量][ex:石頭交換 經驗藥水 100]")
  async def stone_change(self,message,thing:str,a:int):
    ID = str(message.author.id)
    User = get_user(ID)
    stone = User["stone"]
    if(stone == ""):
      stone = 0
    if(thing == "經驗藥水" and a*5<=stone):
      if("exp_potion" in str(User.keys())):
        User["exp_potion"] += a
      else:
        User["exp_potion"] = a
      User["stone"] -= a*5
    elif(thing == "角色重設券" and a*100<=stone):
      if("role_reset" in str(User.keys())):
        User["role_reset"] += a
      else:
        User["role_reset"] = a
      User["stone"]-= a*100
    elif(thing == "角色2空間"):
      if(a!=1):
        await message.channel.send("只能買一個")
        return
      if(stone >= 10):
        pass
      else:
        await message.channel.send("購買商品不存在或所持有的餘額不足")
        return
      if("role2" not in str(User.keys())):
        User["role2"] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        User["stone"]-= 10
      else:
        await message.channel.send("您已經擁有角色2空間了")
        return
    elif(thing == "角色3空間"):
      if(a!=1):
        await message.channel.send("只能買一個")
        return
      if(stone >= 50):
        pass
      else:
        await message.channel.send("購買商品不存在或所持有的餘額不足")
        return
      if("role3" not in str(User.keys()) and "role2" in str(User.keys())):
        User["role3"] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        User["stone"]-= 50
      else:
        await message.channel.send("您已經擁有角色3空間了")
        return
    elif(thing == "角色4空間"):
      if(a!=1):
        await message.channel.send("只能買一個")
        return
      if(stone >= 100):
        pass
      else:
        await message.channel.send("購買商品不存在或所持有的餘額不足")
        return
      if("role4" not in str(User.keys()) and "role3" in str(User.keys())):
        User["role4"] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        User["stone"]-= 100
      else:
        await message.channel.send("您已經擁有角色4空間了")
        return
    elif(thing == "角色5空間"):
      if(a!=1):
        await message.channel.send("只能買一個")
        return
      if(stone >= 200):
        pass
      else:
        await message.channel.send("購買商品不存在或所持有的餘額不足")
        return
      if("role5" not in str(User.keys()) and "role4" in str(User.keys())):
        User["role5"] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        User["stone"]-= 200
      else:
        await message.channel.send("您已經擁有角色5空間了")
        return
    elif(thing == "角色6空間"):
      if(a!=1):
        await message.channel.send("只能買一個")
        return
      if(stone >= 400):
        pass
      else:
        await message.channel.send("購買商品不存在或所持有的餘額不足")
        return
      if("role6" not in str(User.keys()) and "role5" in str(User.keys())):
        User["role6"] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        User["stone"]-= 400
      else:
        await message.channel.send("您已經擁有角色6空間了")
        return
    #elif(thing == "角色轉生券" and a*1000<=stone):
      #if("role_relive" in str(User.keys())):
        #User["role_relive"] += a
      #else:
        #User["role_relive"] = a
      #User["stone"] -= a*1000
    else:
      await message.channel.send("購買商品不存在或所持有的餘額不足")
      return
    put_user(ID,User)
    await message.channel.send("成功")
  @commands.command(aliases=["開啟","打開"],help="可用來使用特定道具，格式為[開啟 欲使用的物品 欲使用的戰鬥角色位置 數量][ex:開啟 經驗藥水 1 1]")
  async def open(self,message,thing:str,roleNumber:str,monunt:int):
    ID = str(message.author.id)
    User = get_user(ID)
    roleNumber.split("角色")
    if(monunt<=0):
      await message.channel.send("使用失敗")
      return 
    roleNumber  = roleNumber[0]
    role = "role"+str(roleNumber)
    if(thing == "經驗藥水" and "exp_potion" in str(User.keys()) and User["exp_potion"]>=monunt):
      #lv,exp,HP,ATK,DEF,SPD
      User[role][1],User[role][2],User[role][3],User[role][4],User[role][5],User[role][6] = level_up(User[role][1],User[role][2],50*monunt,User[role][3],User[role][4],User[role][5],User[role][6],User[role][7],User[role][8],User[role][9],User[role][10])
      User["exp_potion"] -=monunt
      await message.channel.send("使用成功")
    elif(thing == "中階經驗藥水" and "good_potion" in str(User.keys()) and User["good_potion"]>=monunt):
      #lv,exp,HP,ATK,DEF,SPD
      User[role][1],User[role][2],User[role][3],User[role][4],User[role][5],User[role][6] = level_up(User[role][1],User[role][2],100*monunt,User[role][3],User[role][4],User[role][5],User[role][6],User[role][7],User[role][8],User[role][9],User[role][10])
      User["good_potion"] -=monunt
      await message.channel.send("使用成功")
    elif(thing == "角色重設券" and "role_reset" in str(User.keys()) and User["role_reset"]>0):
      User[role] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
      User["role_reset"] -=1
      await message.channel.send("角色"+str(roleNumber)+"已重置")
    #elif(thing == "角色轉生券" and "role_relive" in str(User.keys()) and User["role_relive"]>0):
      #pass
    else:
      await message.channel.send("輸入有誤，請再次檢查")
      return
    put_user(ID,User)
  @commands.command(aliases=["攻擊野怪","打野怪","野怪攻擊","野怪去死","討伐野怪","野怪"],help="可於動物區使用，用來攻擊小怪")
  async def wild_monster(self,message):
    ID = str(message.author.id)
    if(message.channel.id == 897419609240649759 or message.channel.id == 897419656091041843 or message.channel.id == 897419696452812852):
      pass
    else:
      return
    if(check_user(ID)):
      pass
    else:
      await message.channel.send("<@"+str(message.author.id)+"> 請先輸入 註冊 完成註冊<:mumi:609708401513070602>")
      return
    User = get_user(ID)
    with open("role.json","r",encoding="utf-8")as f:
      RoleData = json.load(f)
    with open("data.json","r",encoding="utf-8")as f:
      Data = json.load(f)
    with open("wild_monster.json","r",encoding="utf-8")as f:
      W = json.load(f)
    W_M = W
    if(message.channel.id == 897419609240649759):
      #可愛動物區
      W = W["easy"]
    elif(message.channel.id == 897419656091041843):
      #危險動物區
      W = W["normal"]
    elif(message.channel.id == 897419696452812852):
      #兇猛動物區
      W = W["hard"]
    if(W["total"][2] == 0 or W_M["mode"] == 0):
      R = random.randint(1,W["total"][1])
    else:
      R = random.randint(1,10)
      if(R<=4):
        R = random.randint(1,W["total"][1])
      else:
        R = random.randint(W["total"][1]+1,W["total"][2])
    R = str(R)
    Sname = W[R][0]
    Slv = W[R][1]
    Shp = W[R][2]
    Satk = W[R][3]
    Sdef = W[R][4]
    Sspd = W[R][5]
    now_role = User["now_role"]
    now_role = "role"+str(now_role)
    if(now_role in str(User.keys())):
      if(User[now_role][0] == 0):
        await message.channel.send("您沒有設定該角色")
        return
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
      Power = power(ATK,DEF,SPD,HP,LV)
      if(arm1 != 0):
        AH,AA,AD,AS = arms(HP,ATK,DEF,SPD,arm1)
        Power = power(AA,AD,AS,AH,LV)
      power_record(message.author.id,Power,0)
      power_record(message.author.id,Power,int(User["now_role"]))
      L,co,who,hp1,hp2= fight(CardName,LV,HP,ATK,DEF,SPD,Sname,Slv,Shp,Satk,Sdef,Sspd,1,1,arm1,0,skt1,skn1,0,0)
      C = 0
      #while(C<co and mode==1):
        #await message.channel.send("`"+L[C]+"`")
        #C+=1
      if(who==1):
        one = CardName+"獲勝"
      else:
        one = Sname+"獲勝"
      User[now_role][1],User[now_role][2],User[now_role][3],User[now_role][4],User[now_role][5],User[now_role][6]=level_up(LV,EXP,int(hp2/10),HP,ATK,DEF,SPD,ph,pa,pd,ps)
      add_stone = ''
      if(Sname == "石頭"):
        if(int(hp2/10) >= 1):
          add_stone = "獲得了"+str(int(hp2/10))+"顆石頭"
          User["stone"] += int(hp2/10)
        else:
          add_stone = Sname+"對"+CardName+"造成了"+str(hp1)+"點傷害"
      put_user(ID,User)
      await message.channel.send(one+"\n"+CardName+"對"+Sname+"造成了"+str(hp2)+"點傷害\n"+"獲得了"+str(int(hp2/10))+"點經驗值\n"+add_stone)
      s = StringIO()
      s.write(L)
      s.seek(0)
      await message.channel.send(file=discord.File(s, filename="fight.txt"))
    else:
      await message.channel.send("您沒有設定戰鬥角色")
      return 
  @commands.command(aliases=["打架","決鬥","對決","單挑"],help="可於勇者之塔使用，與一位玩家對決，格式為[打架 @一個人]")
  async def fight_with(self,message,who:str):
    ID = str(message.author.id)
    who = who.strip('<@!>')
    if(datetime.now().hour >= 14 and datetime.now().hour<16):
      await message.channel.send("本日積分戰已結束")
      return
    if(message.channel.id != 897671263433162802):
      return
    if (who == str(message.author.id)):
      await message.channel.send("不能與自己戰鬥")
      return
    User1 = get_user(ID)
    User2 = get_user(str(who))
    with open("data.json","r",encoding="utf-8")as f:
      Data = json.load(f)
    if("role1"not in str(User1.keys())):
      await message.channel.send("請先更新")
      return
    if("role1" not in str(User2.keys())):
      await message.channel.send("對方未設定角色")
      return
    now_role1 = User1["now_role"]
    now_role1 = "role"+str(now_role1)
    now_role2 = User2["now_role"]
    now_role2 = "role"+str(now_role2)
    if(User1[now_role1][0] == 0):
      await message.channel.send("您未設定角色")
      return
    if(User2[now_role2][0] == 0):
      await message.channel.send("對方未設定角色")
      return
    #player1
    CardId1 = User1[now_role1][0]
    CardName1 = Data["card"][CardId1-2001]
    LV1 = User1[now_role1][1]
    EXP1 = User1[now_role1][2]
    HP1 = User1[now_role1][3]
    ATK1 = User1[now_role1][4]
    DEF1 = User1[now_role1][5]
    SPD1 = User1[now_role1][6]
    arm1 = User1[now_role1][11]
    skt1 = User1[now_role1][12]
    skn1 = User1[now_role1][13]
    #player2
    CardId2 = User2[now_role2][0]
    CardName2 = Data["card"][CardId2-2001]
    LV2 = User2[now_role2][1]
    EXP2 = User2[now_role2][2]
    HP2 = User2[now_role2][3]
    ATK2 = User2[now_role2][4]
    DEF2 = User2[now_role2][5]
    SPD2 = User2[now_role2][6]
    arm2 = User2[now_role2][11]
    skt2 = User2[now_role2][12]
    skn2 = User2[now_role2][13]
    L,co,who,hp1,hp2= fight(CardName1,LV1,HP1,ATK1,DEF1,SPD1,CardName2,LV2,HP2,ATK2,DEF2,SPD2,1.1,1,arm1,arm2,skt1,skn1,skt2,skn2)
    C = 0
    ADD = ""
    if(who==1):
      D_R = read_file("day_rank")
      power1 = power(ATK1,DEF1,SPD1,HP1,LV1)
      power2 = power(ATK2,DEF2,SPD2,HP2,LV2)
      ADD = int(power2/power1)+random.randint(1,2)
      if(str(message.author.id) not in str(D_R.keys())):
        D_R[str(message.author.id)] = ADD
      else:
        D_R[str(message.author.id)] += ADD
      ADD = "獲得了"+str(ADD)+"排名積分"
      write_file("day_rank",D_R)
      add_show = CardName1+"獲勝\n"+ADD
    else:
      add_show = CardName2+"獲勝"
    await message.channel.send(CardName1+"對"+CardName2+"造成了"+str(hp2)+"點傷害\n"+CardName2+"對"+CardName1+"造成了"+str(hp1)+"點傷害\n"+add_show)
    s = StringIO()
    s.write(L)
    s.seek(0)
    await message.channel.send(file=discord.File(s, filename="fight.txt"))
  @commands.command(aliases=["積分排名","對戰積分","排名","積分"],help="可查看當日勇者之塔積分排名")
  async def rank(self,message):
    day_rank = read_file("day_rank")
    embed = discord.Embed(title="每日對戰積分排名總覽",description=str(datetime.now().year) + "/" + str(datetime.now().month) + "/" + str(datetime.now().day),color=0xeee657)
    k = day_rank
    c = sorted(k.items(), key=lambda x:x[1])
    i = 0
    K = len(k)
    show = ""
    while(K-i >0):
      show = show+"NO."+str(i+1)+" <@"+str(c[K-i-1][0])+">:"+str(c[K-i-1][1])+"\n"
      i+=1
    embed.add_field(name="排行榜", value=str(show), inline=False)
    await message.channel.send(embed=embed)
  @commands.command(aliases=["積分結算"])
  async def Srank(self,message):
    day_rank = read_file("day_rank")
    if (message.author.id == 598440593001021471 or message.author.id == 598440593001021471 or message.author.id == 550907252970749952 or message.author.id == 511246631073611808 or message.author.id == 480747560793931778 or message.author.id == 352066968750260245 or message.author.id == 544552665204654080 or message.author.id == 597692502346301452):
      pass
    else:
      return
    if(datetime.now().hour < 14 or datetime.now().hour >=16):
      if(message.author.id == 550907252970749952):
        pass
      else:
        await message.channel.send("尚未22點")
        return
    k = day_rank
    c = sorted(k.items(), key=lambda x:x[1])
    i = 0
    K = len(k)
    show = ""
    while(i<K):
      t = get_user(str(c[K-i-1][0]))
      if(t['stone']==""):
        t['stone'] = 0
      if(i<3):
        add = 10
      elif(i<5):
        add = 7
      elif(i<10):
        add = 5
      else:
        add = 1
      t['stone'] += add
      put_user(str(c[K-i-1][0]),t)
      i+=1
    D_R = {}
    day_rank = read_file("day_rank")
    embed = discord.Embed(title="每日對戰積分排名總覽",description=str(datetime.now().year) + "/" + str(datetime.now().month) + "/" + str(datetime.now().day),color=0xeee657)
    k = day_rank
    c = sorted(k.items(), key=lambda x:x[1])
    i = 0
    K = len(k)
    show = ""
    while(K-i >0):
      show = show+"NO."+str(i+1)+" <@"+str(c[K-i-1][0])+">:"+str(c[K-i-1][1])+"\n"
      i+=1
    embed.add_field(name="排行榜", value=str(show), inline=False)
    channel = self.bot.get_channel(897418210629021716)
    await channel.send('本日積分戰結果')
    await channel.send(embed=embed)
    write_file("day_rank",D_R)
    await message.channel.send('成功')
  @commands.command(aliases=["切換戰鬥角色"],help="可用來切換當前的戰鬥角色，格式為[切換戰鬥角色 要切換的角色數字(空間)][ex:切換戰鬥角色 1]")
  async def change_role(self,message,which:int):
    ID = str(message.author.id)
    User = get_user(ID)
    now_role = "role"+str(which)
    if(which == 1 and "role1" in str(User.keys())):
      User["now_role"] = 1
    elif(which == 2 and "role2" in str(User.keys())):
      User["now_role"] = 2
    elif(which == 3 and "role3" in str(User.keys())):
      User["now_role"] = 3
    elif(which == 4 and "role4" in str(User.keys())):
      User["now_role"] = 4
    elif(which == 5 and "role5" in str(User.keys())):
      User["now_role"] = 5
    elif(which == 6 and "role6" in str(User.keys())):
      User["now_role"] = 6
    else:
      await message.channel.send("您未擁有角色"+str(which)+"空間")
      return
    put_user(ID,User)
    await message.channel.send("成功")
  @commands.command(aliases=["魔王設定Ststone"])
  async def set_boss_Ststone(self,message,mode:str):
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
    boss["boss"] = "Ststone"
    name = "Ststone"
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
  @commands.command(aliases=["玩家戰力排名"])
  async def player_power_rank(self,message,which:int):
    day_rank = read_file("power_rank")
    k = day_rank[str(which)]
    c = sorted(k.items(), key=lambda x:x[1])
    i = 0
    K = len(k)
    show = ""
    while(K-i >0):
      j = 0
      show = ""
      while(j<20 and K-i-j >0):
        embed = discord.Embed(title="玩家戰力排名",description=str(datetime.now().year) + "/" + str(datetime.now().month) + "/" + str(datetime.now().day),color=0xeee657)
        show = show+"NO."+str(i+j+1)+" <@"+str(c[K-i-j-1][0])+">:"+str(c[K-i-j-1][1])+"\n"
        j+=1
      embed.add_field(name="排行榜", value=str(show), inline=False)
      await message.channel.send(embed=embed)
      i+=20
  @commands.command(aliases=["資質計算"],help="可用來鑑定自己角色的資質，格式為[資質計算 角色數字(空間)][ex:資質計算 1]")
  async def potential(self,message,which:int):
    ID = str(message.author.id)
    if(check_user(ID)):
      pass
    else:
      await message.channel.send("<@"+str(message.author.id)+"> 請先輸入 註冊 完成註冊<:mumi:609708401513070602>")
      return
    User = get_user(ID)
    with open("role.json","r",encoding="utf-8")as f:
      RoleData = json.load(f)
    with open("data.json","r",encoding="utf-8")as f:
      Data = json.load(f)
    with open("wild_monster.json","r",encoding="utf-8")as f:
      W = json.load(f)
    now_role = "role"+str(which)
    if(now_role in str(User.keys())):
      if(User[now_role][0] == 0):
        await message.channel.send("您沒有設定該角色")
        return
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
      HPl = RoleData[str(CardId)]["HP"][0]
      ATKl = RoleData[str(CardId)]["ATK"][0]
      DEFl = RoleData[str(CardId)]["DEF"][0]
      SPDl = RoleData[str(CardId)]["SPD"][0]
      star = (((HP-(ph*(LV-1)))+(ATK-(pa*(LV-1)))+(DEF-(pd*(LV-1)))+(SPD-(ps*(LV-1)))-HPl-ATKl-DEFl-SPDl+4)*0.5)-1
      show_star = star
      show = ""
      if(star < 0):
        star = 0
      while(star > 0):
        if(star-1 >= 0):
          show += "<:star:806055501958873099> "
          star -= 1
        elif(star-0.5 >= 0):
          show += "<:half_star:806056480809811968> "
          star -= 0.5
      await message.channel.send("您的"+str(CardName)+"資質是"+str(show_star)+"顆星\n"+show)
    else:
      await message.channel.send("您沒有設定該角色")
      return 
  @commands.command(aliases=["裝備包包","裝備總覽","裝備資訊"],help="可用來查看自己的所有裝備")
  async def arms_bag(self,message):
    ID = str(message.author.id)
    if(check_user(ID)):
      pass
    else:
      await message.channel.send("<@"+str(message.author.id)+"> 請先輸入 註冊 完成註冊<:mumi:609708401513070602>")
      return
    User = get_user(ID)
    with open("arms.json","r",encoding="utf-8")as f:
      data = json.load(f)
    if("arms" not in str(User.keys())):
      await message.channel.send("請先完成更新")
      return
    embed = discord.Embed(title="裝備包包資訊",description=str(message.author),color=0xeee657)
    i = 0
    while(i<10):
      embed.add_field(name="空間"+str(i+1), value=data[str(User["arms"][str(i+1)][0])][0], inline=False)
      i+=1
    embed.set_footer(text="若需查看單一裝備請用\"查看裝備\"")
    await message.channel.send(embed=embed)
  @commands.command(aliases=["查看裝備","我的裝備"],help="可用來看單一裝備的詳細資訊，格式為[查看裝備 裝備號碼][ex:查看裝備 1]")
  async def arms_number(self,message,number:int):
    ID = str(message.author.id)
    if(check_user(ID)):
      pass
    else:
      await message.channel.send("<@"+str(message.author.id)+"> 請先輸入 註冊 完成註冊<:mumi:609708401513070602>")
      return
    User = get_user(ID)
    with open("arms.json","r",encoding="utf-8")as f:
      data = json.load(f)
    if("arms" not in str(User.keys())):
      await message.channel.send("請先完成更新")
      return
    if(str(User["arms"][str(number)][0]) == "0"):
      await message.channel.send("此空間沒有裝備")
      return
    L = data[str(User["arms"][str(number)][0])]
    Sadd = ""
    if(User["arms"][str(number)][1] != 0):
      Sadd = "(角色"+str(User["arms"][str(number)][1])+")"
    embed = discord.Embed(title=L[0]+Sadd,description=L[5],color=0xeee657)
    if("." in str(L[1])):
      HP = str(int((L[1]*100)-100))+"%"
      if((L[1]*100)-100 >= 0):
        HP = "+"+HP
    else:
      if(L[1]>=0):
        HP = "+"+str(L[1])
      else:
        HP = str(L[1])
    if("." in str(L[2])):
      ATK = str(int((L[2]*100)-100))+"%"
      if((L[2]*100)-100 >= 0):
        ATK = "+"+ATK
    else:
      if(L[2]>=0):
        ATK = "+"+str(L[2])
      else:
        ATK = str(L[2])
    if("." in str(L[3])):
      DEF = str(int((L[3]*100)-100))+"%"
      if((L[3]*100)-100 >= 0):
        DEF = "+"+DEF
    else:
      if(L[3]>=0):
        DEF = "+"+str(L[3])
      else:
        DEF = str(L[3])
    if("." in str(L[4])):
      SPD = str(int((L[4]*100)-100))+"%"
      if((L[4]*100)-100 >= 0):
        SPD = "+"+SPD
    else:
      if(L[4]>=0):
        SPD = "+"+str(L[4])
      else:
        SPD = str(L[4])
    embed.add_field(name="血量:", value=HP, inline=False)
    embed.add_field(name="攻擊力:", value=ATK, inline=False)
    embed.add_field(name="防禦力:", value=DEF, inline=False)
    embed.add_field(name="速度:", value=SPD, inline=False)
    embed.set_footer(text="分類："+L[6])
    await message.channel.send(embed=embed)
  @commands.command(aliases=["裝備"],help="可裝備裝備在角色身上，格式為[裝備 裝備號碼 角色號碼][ex:裝備 10 1]")
  async def arms_on(self,message,number:int,role:int):
    ID = str(message.author.id)
    if(check_user(ID)):
      pass
    else:
      await message.channel.send("<@"+str(message.author.id)+"> 請先輸入 註冊 完成註冊<:mumi:609708401513070602>")
      return
    User = get_user(ID)
    with open("arms.json","r",encoding="utf-8")as f:
      data = json.load(f)
    if("arms" not in str(User.keys())):
      await message.channel.send("請先完成更新")
      return
    now_role = "role"+str(role)
    if(now_role in str(User.keys())):
      if(User[now_role][0] == 0):
        await message.channel.send("您沒有設定該角色")
        return
    else:
      await message.channel.send("此空間未獲得")
      return
    if(User[now_role][11] != 0):
      await message.channel.send("此角色已經有裝備，請先卸除才能再裝備")
      return
    if(User["arms"][str(number)][1] != 0):
      await message.channel.send("此裝備已使用，請先卸除才能再使用")
      return
    User["arms"][str(number)][1] = role
    User[now_role][11] = User["arms"][str(number)][0]
    User[now_role][12] = User["arms"][str(number)][2]
    User[now_role][13] = User["arms"][str(number)][3]
    put_user(ID,User)
    await message.channel.send("成功")
  @commands.command(aliases=["卸載裝備"],help="可從角色身上卸載裝備，格式為[卸載裝備 裝備號碼][ex:卸載裝備 10]")
  async def arms_down(self,message,number:int):
    ID = str(message.author.id)
    if(check_user(ID)):
      pass
    else:
      await message.channel.send("<@"+str(message.author.id)+"> 請先輸入 註冊 完成註冊<:mumi:609708401513070602>")
      return
    User = get_user(ID)
    with open("arms.json","r",encoding="utf-8")as f:
      data = json.load(f)
    if("arms" not in str(User.keys())):
      await message.channel.send("請先完成更新")
      return
    if(User["arms"][str(number)][1] <= 0):
      await message.channel.send("此裝備未使用，無法卸載")
      return
    role = User["arms"][str(number)][1]
    now_role = "role"+str(role)
    User["arms"][str(number)][1] = 0
    User[now_role][11] = 0
    User[now_role][12] = 0
    User[now_role][13] = 0
    put_user(ID,User)
    await message.channel.send("成功")
  @commands.command(aliases=["販賣裝備"],help="可販賣不要的裝備，獲得交換點數50，格式為[販賣裝備 裝備號碼][ex:販賣裝備 10]")
  async def sell_arms(self,message,number:int):
    ID = str(message.author.id)
    if(check_user(ID)):
      pass
    else:
      await message.channel.send("<@"+str(message.author.id)+"> 請先輸入 註冊 完成註冊<:mumi:609708401513070602>")
      return
    User = get_user(ID)
    with open("arms.json","r",encoding="utf-8")as f:
      data = json.load(f)
    if("arms" not in str(User.keys())):
      await message.channel.send("請先完成更新")
      return
    if(User["arms"][str(number)][1] != 0):
      await message.channel.send("此裝備已使用，請先卸除才能販賣")
      return
    if(User["arms"][str(number)][0] == 0):
      await message.channel.send("此空間無裝備，無法販賣")
      return
    User["arms"][str(number)][0] = 0
    User["arms"][str(number)][2] = 0
    User["arms"][str(number)][3] = 0
    User["re"] += 50
    put_user(ID,User)
    await message.channel.send("成功，獲得交換點數×50")
  @commands.command(aliases=["裝備上架"],help="可由玩家自行訂價，販賣不要的裝備，貨幣種類為1(姆咪幣)，2(石頭)，3(交換點數)，格式為[裝備上架 裝備號碼 價格 貨幣種類 簡介][ex:裝備上架 1 100 2 Hi](簡介可加可不加)")
  async def arms_on_sell(self,message,number:int,money:int,T:int):
    ID = str(message.author.id)
    ID = message.author.id
    if(money < 0):
      await message.channel.send("請勿開玩笑")
      return
    if(T == 1 or T == 2 or T == 3):
      pass
    else:
      await message.channel.send("貨幣種類錯誤")
      return
    if(check_user(str(ID))):
      pass
    else:
      await message.channel.send("<@"+str(message.author.id)+"> 請先輸入 註冊 完成註冊<:mumi:609708401513070602>")
      return
    User = get_user(str(ID))
    data = read_file("arms_shop")
    if("arms" not in str(User.keys())):
      await message.channel.send("請先完成更新")
      return
    if(User["arms"][str(number)][1] != 0):
      await message.channel.send("此裝備已使用，請先卸除才能販賣")
      return
    if(User["arms"][str(number)][0] == 0):
      await message.channel.send("此空間無裝備")
      return
    arm_number = User["arms"][str(number)][0]
    data["number"]+=1
    N = data["number"]
    channel = self.bot.get_channel(message.channel.id)
    li = [0]
    async for msg in channel.history(limit=20):
      print(msg.content)
      if(msg.content.startswith("裝備上架") and msg.author.id == message.author.id):
        li = str(msg.content).split()
        break
    if(len(li)>=5):
      li = li[4]
    else:
      li = 0
    data[str(N)] = [ID,arm_number,T,money,li,0,0]#賣家id,裝備編號,貨幣種類,貨幣金額,介紹,0,0
    User["arms"][str(number)][0] = 0
    User["arms"][str(number)][2] = 0
    User["arms"][str(number)][3] = 0
    put_user(str(ID),User)
    write_file("arms_shop",data)
    await message.channel.send("成功，販賣編號是："+str(N))
    new_channel = self.bot.get_channel(889791337292005386)
    await new_channel.send("```"+str(data)+"```")
  @commands.command(aliases=["裝備下架"],help="可下架自己販賣中的裝備，收取10姆咪幣手續費，格式為[裝備下架 販賣編號][ex:裝備下架 100000]")
  async def arms_down_sell(self,message,number:int):
    with open("arms.json","r",encoding="utf-8")as f:
      arms_data = json.load(f)
    ID = str(message.author.id)
    ID = message.author.id
    if(check_user(str(ID))):
      pass
    else:
      await message.channel.send("<@"+str(message.author.id)+"> 請先輸入 註冊 完成註冊<:mumi:609708401513070602>")
      return
    User = get_user(str(ID))
    data = read_file("arms_shop")
    if(str(number) not in str(data.keys())):
      await message.channel.send("搜尋不到此編號的商品")
      return
    if(data[str(number)][0] != ID):
      await message.channel.send("這裝備...不是您賣的吧")
      return
    else:
      arm_number = data[str(number)][1]
      i = 1
      f = "t"
      while(i<=10 and f == "t"):
        if(User["arms"][str(i)][0] == 0):
          User["arms"][str(i)][0] = arm_number
          User["arms"][str(i)][2] = arms_data[str(arm_number)][7]
          User["arms"][str(i)][3] = arms_data[str(arm_number)][8]
          f = "f"
        i += 1
      if(f == "t"):
        await message.channel.send("裝備包包無空間，無法收回裝備")
        return
      del data[str(number)]
      if(User["point"] >= 10):
        User["point"] -= 10
      else:
        await message.channel.send("持有姆咪幣不足")
        return
      put_user(str(ID),User)
      write_file("arms_shop",data)
      await message.channel.send("成功")
      new_channel = self.bot.get_channel(889791337292005386)
      await new_channel.send("```"+str(data)+"```")
  @commands.command(aliases=["裝備拍賣市場"],help="可隨機抽出10個正在販賣的裝備資訊")
  async def arms_market(self,message):
    data = read_file("arms_shop")
    with open("arms.json","r",encoding="utf-8")as f:
      a = json.load(f)
    L = sorted(data.keys())
    s = len(L)-1
    if(s == 0):
      await message.channel.send("目前無資料")
      return
    embed = discord.Embed(title="裝備拍賣市場",description="隨機抽出10個",color=0xeee657)
    i = 0
    li = ""
    #賣家id,裝備編號,貨幣種類,貨幣金額,0,0,0
    while(i<s and i<10):
      r = random.randint(0,s-1)
      if(L[r] not in li):
        li += L[r]+","
        ID = T = data[L[r]][0]
        _arm_ = data[L[r]][1]
        T = data[L[r]][2]
        much = data[L[r]][3]
        if(data[L[r]][4] == 0):
          show = "無"
        else:
          show = str(data[L[r]][4])
        _arm_ = a[str(_arm_)][0]
        if(T == 1):
          T = "姆咪幣"
        elif(T == 2):
          T = "石頭"
        elif(T == 3):
          T = "交換點數"
        embed.add_field(name=str(_arm_)+"("+str(L[r])+")", value="賣家：<@"+str(ID)+">\n價格："+str(T)+"×"+str(much)+"\n簡介："+show, inline=False)
        i+=1
    embed.set_footer(text="交易皆徵收10姆咪幣手續費")
    await message.channel.send(embed=embed)
  @commands.command(aliases=["購買裝備"],help="可購買市場上再販賣的裝備，收取10姆咪幣手續費，格式為[購買裝備 販賣編號][ex:購買裝備 100000]")
  async def buy_arms(self,message,number:int):
    with open("arms.json","r",encoding="utf-8")as f:
      arms_data = json.load(f)
    ID = str(message.author.id)
    if(check_user(ID)):
      pass
    else:
      await message.channel.send("<@"+str(message.author.id)+"> 請先輸入 註冊 完成註冊<:mumi:609708401513070602>")
      return
    User = get_user(ID)
    data = read_file("arms_shop")
    if("arms" not in str(User.keys())):
      await message.channel.send("請先完成更新")
      return
    User1 = get_user(ID)
    if(str(number) not in str(data.keys())):
      await message.channel.send("搜尋不到此編號的商品")
      return
    if(str(data[str(number)][0]) == ID):
      await message.channel.send("不能買自己販賣的裝備啦><")
      return
    sell_id = data[str(number)][0]
    arm_number = data[str(number)][1]
    T = data[str(number)][2]
    money = data[str(number)][3]
    User2 = get_user(str(sell_id))
    #賣家id,裝備編號,貨幣種類,貨幣金額,0,0,0
    if(User1['point']>=10):
      User1['point']-=10
    else:
      await message.channel.send("持有的貨幣不足")
      return
    if(T==1 and User1['point']>=money):
      User1['point']-=money
      User2['point']+=money
      pass
    elif(T==2 and User1['stone']>=money):
      User1['stone']-=money
      User2['stone']+=money
      pass
    elif(T==3 and User1['re']>=money):
      User1['re']-=money
      User2['re']+=money
      pass
    else:
      await message.channel.send("持有的貨幣不足")
      return
    i = 1
    f = "t"
    while(i<=10 and f == "t"):
      if(User1["arms"][str(i)][0] == 0):
        User1["arms"][str(i)][0] = arm_number
        User1["arms"][str(i)][2] = arms_data[str(arm_number)][7]
        User1["arms"][str(i)][3] = arms_data[str(arm_number)][8]
        f = "f"
      i += 1
    if(f == "t"):
      await message.channel.send("裝備包包無空間，無法購買裝備")
      return
    del data[str(number)]
    put_user(ID,User1)
    put_user(str(sell_id),User2)
    write_file("arms_shop",data)
    await message.channel.send("交易成功")
    new_channel = self.bot.get_channel(889791337292005386)
    await new_channel.send("```"+str(data)+"```")
  @commands.command(aliases=["魔王設定玩家"])
  async def set_boss_player(self,message,who:str,mode:str):
    if (message.author.id == 550907252970749952 or message.author.id == 511246631073611808 or message.author.id == 480747560793931778 or message.author.id == 352066968750260245 or message.author.id == 544552665204654080 or message.author.id == 597692502346301452):
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
    who = who.strip('<@!>')
    User = get_user(who)
    guild = self.bot.get_guild(782593702455279616)
    author = guild.get_member(int(who))
    now_role = User["now_role"]
    now_role = "role"+str(now_role)
    boss = {}
    boss["fight"] = "t"
    boss["boss"] = author.name
    name = author.name
    boss["url"] = str(author.avatar_url)
    boss["type"] = mode
    boss["LV"] = 100*DP
    boss["HP"] = int(20000*DP)
    boss["ATK"] = int(User[now_role][4]*(1+DP))
    boss["DEF"] = int(User[now_role][5]*(1+DP))
    boss["SPD"] = int(User[now_role][6]*(1+DP))
    boss["rank"] = {}
    boss["time"] = 0
    boss["cardS"] = User[now_role][0]
    boss["cardE"] = User[now_role][0]
    boss["reward"] = bossData["reward"][mode]
    #await message.channel.send(boss)
    write_file("boss",boss)
    await message.channel.send("成功")
    embed = discord.Embed(title=str(boss["boss"])+"（"+str(boss["type"])+"）",description="剩餘血量："+str(boss["HP"]),color=0xeee657)
    embed.add_field(name="戰鬥力：", value=int(power(boss["ATK"],boss["DEF"],boss["SPD"],boss["HP"],boss["LV"])), inline=False)
    embed.add_field(name="LV：", value=boss["LV"], inline=False)
    embed.add_field(name="HP：", value=boss["HP"], inline=False)
    embed.add_field(name="ATK：", value=boss["ATK"], inline=False)
    embed.add_field(name="DEF：", value=boss["DEF"], inline=False)
    embed.add_field(name="SPD：", value=boss["SPD"], inline=False)
    embed.set_thumbnail(url=author.avatar_url)
    embed.set_footer(text="開放時間：22:00~22:30")
    await message.channel.send(embed=embed)
  @commands.command(aliases=["查詢裝備"],help="可用來查看單一裝備的詳細資訊，格式為[查看裝備 裝備名稱][ex:查詢裝備 銀葉]")
  async def arms_search(self,message,arm_name:str):
    with open("arms_name.json","r",encoding="utf-8")as f:
      Names = json.load(f)
    if(arm_name not in str(Names.keys())):
      await message.channel.send("查詢不到此名稱之裝備")
      return
    with open("arms.json","r",encoding="utf-8")as f:
      data = json.load(f)
    L = data[Names[arm_name]]
    embed = discord.Embed(title=L[0],description=L[5],color=0xeee657)
    if("." in str(L[1])):
      HP = str(int((L[1]*100)-100))+"%"
      if((L[1]*100)-100 >= 0):
        HP = "+"+HP
    else:
      if(L[1]>=0):
        HP = "+"+str(L[1])
      else:
        HP = str(L[1])
    if("." in str(L[2])):
      ATK = str(int((L[2]*100)-100))+"%"
      if((L[2]*100)-100 >= 0):
        ATK = "+"+ATK
    else:
      if(L[2]>=0):
        ATK = "+"+str(L[2])
      else:
        ATK = str(L[2])
    if("." in str(L[3])):
      DEF = str(int((L[3]*100)-100))+"%"
      if((L[3]*100)-100 >= 0):
        DEF = "+"+DEF
    else:
      if(L[3]>=0):
        DEF = "+"+str(L[3])
      else:
        DEF = str(L[3])
    if("." in str(L[4])):
      SPD = str(int((L[4]*100)-100))+"%"
      if((L[4]*100)-100 >= 0):
        SPD = "+"+SPD
    else:
      if(L[4]>=0):
        SPD = "+"+str(L[4])
      else:
        SPD = str(L[4])
    embed.add_field(name="血量:", value=HP, inline=False)
    embed.add_field(name="攻擊力:", value=ATK, inline=False)
    embed.add_field(name="防禦力:", value=DEF, inline=False)
    embed.add_field(name="速度:", value=SPD, inline=False)
    embed.set_footer(text="分類："+L[6])
    await message.channel.send(embed=embed)
  @commands.command(aliases=["查詢賣家"],help="可隨機抽出10個特定賣家正在販賣的裝備資訊，格式為[查詢賣家 玩家ID][ex:查詢賣家 609796369405706240]")
  async def arms_market_search_user(self,message,who:str):
    who = who.strip('<@!>')
    data = {}
    change = read_file("arms_shop")
    L = sorted(change.keys())
    for i in L:
      if(str(i)!="number" and str(change[str(i)][0])==who):
        data[str(i)] = change[str(i)]
    with open("arms.json","r",encoding="utf-8")as f:
      a = json.load(f)
    L = sorted(data.keys())
    s = len(L)
    if(s == 0):
      await message.channel.send("目前無資料")
      return
    embed = discord.Embed(title="裝備拍賣市場",description="賣家<@"+who+"> 隨機抽取10個",color=0xeee657)
    i = 0
    li = ""
    #賣家id,裝備編號,貨幣種類,貨幣金額,0,0,0
    while(i<s and i<10):
      r = random.randint(0,s-1)
      if(L[r] not in li):
        li += L[r]+","
        ID = T = data[L[r]][0]
        _arm_ = data[L[r]][1]
        T = data[L[r]][2]
        much = data[L[r]][3]
        if(data[L[r]][4] == 0):
          show = "無"
        else:
          show = str(data[L[r]][4])
        _arm_ = a[str(_arm_)][0]
        if(T == 1):
          T = "姆咪幣"
        elif(T == 2):
          T = "石頭"
        elif(T == 3):
          T = "交換點數"
        embed.add_field(name=str(_arm_)+"("+str(L[r])+")", value="賣家：<@"+str(ID)+">\n價格："+str(T)+"×"+str(much)+"\n簡介："+show, inline=False)
        i+=1
    embed.set_footer(text="交易皆徵收10姆咪幣手續費")
    await message.channel.send(embed=embed)
  @commands.command(aliases=["裝備比價"],help="可隨機抽出10個相同裝備在市場上販賣的情形，格式為[裝備比價 裝備名稱][ex:裝備比價 銀葉]")
  async def arms_market_search_type(self,message,arm_name:str):
    with open("arms_name.json","r",encoding="utf-8")as f:
      Names = json.load(f)
    if(arm_name not in str(Names.keys())):
      await message.channel.send("查詢不到此名稱之裝備")
      return
    which_arm = str(Names[arm_name])
    data = {}
    change = read_file("arms_shop")
    L = sorted(change.keys())
    for i in L:
      if(str(i)!="number" and str(change[str(i)][1])==which_arm):
        data[str(i)] = change[str(i)]
    with open("arms.json","r",encoding="utf-8")as f:
      a = json.load(f)
    L = sorted(data.keys())
    s = len(L)
    if(s == 0):
      await message.channel.send("目前無資料")
      return
    embed = discord.Embed(title="裝備拍賣市場",description="裝備「"+arm_name+"」隨機抽取10個",color=0xeee657)
    i = 0
    li = ""
    #賣家id,裝備編號,貨幣種類,貨幣金額,0,0,0
    while(i<s and i<10):
      r = random.randint(0,s-1)
      if(L[r] not in li):
        li += L[r]+","
        ID = T = data[L[r]][0]
        _arm_ = data[L[r]][1]
        T = data[L[r]][2]
        much = data[L[r]][3]
        if(data[L[r]][4] == 0):
          show = "無"
        else:
          show = str(data[L[r]][4])
        _arm_ = a[str(_arm_)][0]
        if(T == 1):
          T = "姆咪幣"
        elif(T == 2):
          T = "石頭"
        elif(T == 3):
          T = "交換點數"
        embed.add_field(name=str(_arm_)+"("+str(L[r])+")", value="賣家：<@"+str(ID)+">\n價格："+str(T)+"×"+str(much)+"\n簡介："+show, inline=False)
        i+=1
    embed.set_footer(text="交易皆徵收10姆咪幣手續費")
    await message.channel.send(embed=embed)
def setup(bot):
  bot.add_cog(role(bot))