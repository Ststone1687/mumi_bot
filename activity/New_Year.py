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
def power(ATK:int,DEF:int,SPD:int,HP:int,Lv:int):
  P = (2*ATK+2*DEF+2*SPD+HP+2*Lv)*3+((HP-Lv+ATK+DEF*2)/2)*(SPD)/100
  return int(P)

class New_Year(Cog_Extension):
  @commands.command(aliases=["創建小隊","創建隊伍"])
  async def New_Year_create_a_new_party(self,message,name:str):
    ID = message.author.id
    User = get_user(str(ID))
    filename = str(ID)+".json"
    activity = read_file("activity")
    if(str(ID) in str(activity["list"].keys())):
      await message.channel.send("您目前已加入小隊")
      return
    if(User["point"] < 100):
      await message.channel.send("持有的姆咪幣不足")
      return
    User["point"] -= 100
    new_party = {
      "leader":ID,
      "name":name,
      "list":str(ID)+",",
      "reward":[0,0,0],#紅包,經驗藥水,回復藥水
      "status":"t",
      "monster":["",0,0,0,0,0,0,0],#名稱,等級,現HP,原HP,ATK,DEF,SPD,獎勵(0:紅包,1:回復藥水,2:經驗藥水)
      "power":0,
      "people":1
    }
    new_party[str(ID)] = {"add":[]}
    activity["number"]+=1
    activity["list"][str(ID)] = activity["number"]
    Nfile = "New_Year_"+str(activity["number"])
    all_file = read_file("all_file")
    all_file[Nfile] = new_party
    write_file("all_file",all_file)
    write_file("activity",activity)
    put_user(str(ID),User)
    await message.channel.send("成功，隊伍編號為"+str(activity["number"]))
  @commands.command(aliases=["加入小隊","加入隊伍"])
  async def New_Year_join_a_party(self,message,number:int):
    ID = message.author.id
    activity = read_file("activity")
    if(str(ID) in str(activity["list"].keys())):
      await message.channel.send("您目前已加入小隊")
      return
    all_file = read_file("all_file")
    Nfile = "New_Year_"+str(number)
    #print(all_file)
    #print(activity)
    if(Nfile not in str(all_file.keys())):
      await message.channel.send("搜尋不到此編號的隊伍")
      return
    N_a = all_file[Nfile]
    if(N_a["status"] != "t" or N_a["people"] >=5):
      await message.channel.send("此隊伍已不開放加入")
      return
    N_a["list"] += str(ID)+","
    N_a[str(ID)] = {"add":[]}
    activity["list"][str(ID)] = number
    write_file("activity",activity)
    all_file[Nfile] = N_a
    write_file("all_file",all_file)
    await message.channel.send("成功")
  @commands.command(aliases=["退出小隊","退出隊伍"])
  async def New_Year_leave_a_party(self,message):
    ID = message.author.id
    activity = read_file("activity")
    if(str(ID) not in str(activity["list"].keys())):
      await message.channel.send("您目前無加入小隊")
      return
    party_number = activity["list"][str(ID)]
    Nfile = "New_Year_"+str(party_number)
    all_file = read_file("all_file")
    if(str(Nfile) not in str(all_file.keys())):
      del activity["list"][str(ID)]
      write_file("activity",activity)
      await message.channel.send("成功")
      return
    N_a = all_file[Nfile]
    if(N_a["status"] != "t"):
      await message.channel.send("無法退出，您的隊伍已經出發了")
      return
    i = 1
    while(i<=6):
      role = str(i)
      if(role in (N_a[str(ID)].keys())):
        User = N_a[str(ID)][role]
        LV = User[1]
        HP1 = User[2]#實際
        HP2 = User[3]
        ATK = User[4]
        DEF = User[5]
        SPD = User[6]
        Power = power(ATK,DEF,SPD,HP2,LV)
        N_a["power"] -= Power
      i += 1
    del activity["list"][str(ID)]
    del N_a[str(ID)]
    N_a["list"] = N_a["list"].replace(str(ID),"")
    N_a["people"] -= 1
    if(ID == N_a["leader"]):
      L = N_a["list"]
      L = L.split(",")
      i = 0
      while(i<len(L)):
        if(L[i]!=""):
          del activity["list"][str(L[i])]
        i += 1
      del all_file[Nfile]
      write_file("all_file",all_file)
      await message.channel.send("成功")
      return
    all_file[Nfile] = N_a
    write_file("all_file",all_file)
    write_file("activity",activity)
    await message.channel.send("成功")
  @commands.command(aliases=["加入角色"])
  async def New_Year_add_a_role(self,message,number:int):
    ID = message.author.id
    User = get_user(str(ID))
    activity = read_file("activity")
    if(str(ID) not in str(activity["list"].keys())):
      await message.channel.send("您目前無加入小隊")
      return
    if("role"+str(number) not in str(User.keys()) or User["role"+str(number)][0]==0):
      await message.channel.send("您沒有該角色")
      return
    party_number = activity["list"][str(ID)]
    Nfile = "New_Year_"+str(party_number)
    all_file = read_file("all_file")
    N_a = all_file[Nfile]
    ok = 0
    #print(N_a[str(ID)])
    for i in N_a[str(ID)]["add"]:
      #print(i)
      if(str(i)==str(number)):
        ok = 1
    if(ok==1):
      await message.channel.send("您已經設定過該角色了")
      return
    if(N_a["status"] != "t"):
      await message.channel.send("已不開放加入")
      return
    role = "role"+str(number)
    NAME = User[role][0]
    LV = User[role][1]
    HP = User[role][3]
    ATK = User[role][4]
    DEF = User[role][5]
    SPD = User[role][6]
    arm1 = User[role][11]
    skt1 = User[role][12]
    skn1 = User[role][13]
    ARM = 0
    if(User[role][11] != 0):
      ARM = User[role][11]
      HP,ATK,DEF,SPD = arms(HP,ATK,DEF,SPD,ARM)
    P = power(ATK,DEF,SPD,HP,LV)
    N_a[str(ID)][str(number)] = [NAME,LV,HP,HP,ATK,DEF,SPD,0,skt1,skn1]
    N_a[str(ID)]["add"].append(str(number))
    N_a["power"] += P
    all_file[Nfile] = N_a
    write_file("all_file",all_file)
    await message.channel.send("成功")
  @commands.command(aliases=["查看角色"])
  async def New_Year_roles(self,message,number:int):
    ID = message.author.id
    activity = read_file("activity")
    if(str(ID) not in str(activity["list"].keys())):
      await message.channel.send("您目前無加入小隊")
      return
    party_number = activity["list"][str(ID)]
    with open("data.json","r",encoding="utf-8")as f:
      Data = json.load(f)
    Nfile = "New_Year_"+str(party_number)
    all_file = read_file("all_file")
    N_a = all_file[Nfile]
    if(str(number) in str(N_a[str(ID)].keys())):
      User = N_a[str(ID)][str(number)]
      CardId = User[0]
      CardName = Data["card"][CardId-2001]
      LV = User[1]
      HP1 = User[2]#實際
      HP2 = User[3]
      ATK = User[4]
      DEF = User[5]
      SPD = User[6]
      Power = power(ATK,DEF,SPD,HP2,LV)
      embed = discord.Embed(title=CardName,description=str(message.author),color=0xeee657)
      embed.add_field(name="戰鬥力:", value=str(Power), inline=False)
      embed.add_field(name="等級:", value=str(LV), inline=False)
      embed.add_field(name="血量:", value=str(HP1)+"/"+str(HP2), inline=False)
      embed.add_field(name="攻擊力:", value=str(ATK), inline=False)
      embed.add_field(name="防禦力:", value=str(DEF), inline=False)
      embed.add_field(name="速度:", value=str(SPD), inline=False)
      if(User[7] != 0):
        with open("arms.json","r",encoding="utf-8")as f:
          ARM = json.load(f)
        embed.add_field(name="裝備:", value=ARM[str(User[7])][0], inline=False)
      embed.set_thumbnail(url=Data["link"][CardId-2001])
      await message.channel.send(embed=embed)
    else:
      await message.channel.send("您沒有設定該角色或該角色已死亡")
      return 
  @commands.command(aliases=["我的隊伍","我的小隊"])
  async def New_Year_my_party(self,message):
    ID = message.author.id
    filename = str(ID)
    User = get_user(str(ID))
    activity = read_file("activity")
    if(str(ID) not in str(activity["list"].keys())):
      await message.channel.send("您目前無加入小隊")
      return
    party_number = activity["list"][str(ID)]
    Nfile = "New_Year_"+str(party_number)
    all_file = read_file("all_file")
    N_a = all_file[Nfile]
    embed = discord.Embed(title=N_a["name"],description="隊長：<@"+str(N_a["leader"])+">",color=0xeee657)
    L = N_a["list"]
    L = L.split(",")
    i = 0
    show = ""
    while(i<len(L)):
      if(L[i]!=""):
        show += "<@"+L[i]+">\n"
      i+=1
    P = N_a["power"]
    a = N_a["reward"][0]
    b = N_a["reward"][1]
    c = N_a["reward"][2]
    embed.add_field(name="總戰力：", value=P, inline=False)
    embed.add_field(name="成員：", value=show, inline=False)
    embed.add_field(name="紅包數(個/每人)：", value=a, inline=False)
    embed.add_field(name="經驗藥水數(個/每人)：", value=b, inline=False)
    embed.add_field(name="回復藥水數：", value=c, inline=False)
    await message.channel.send(embed=embed)
  @commands.command(aliases=["進入地城"])
  async def New_Year_enter(self,message):
    ID = message.author.id
    activity = read_file("activity")
    if(str(ID) not in str(activity["list"].keys())):
      await message.channel.send("您目前無加入小隊")
      return
    party_number = activity["list"][str(ID)]
    Nfile = "New_Year_"+str(party_number)
    all_file = read_file("all_file")
    N_a = all_file[Nfile]
    if(N_a["status"] != "t"):
      await message.channel.send("您的隊伍已經出發了")
      return
    if(N_a["leader"] != message.author.id):
      return
    guild = self.bot.get_guild(782593702455279616)
    P = N_a["power"]
    if(P>100000):
      mode = "極"
      new_role = guild.get_role(938077968712990801)
    elif(P>50000):
      mode = "強"
      new_role = guild.get_role(938078032676143104)
    elif(P>30000):
      mode = "中"
      new_role = guild.get_role(938078081502036019)
    else:
      mode = "弱"
      new_role = guild.get_role(938078117162004490)
    L = N_a["list"]
    L = L.split(",")
    i = 0
    show = ""
    while(i<len(L)):
      if(L[i]!=""):
        AID = int(L[i])
        member = guild.get_member(AID)
        await member.add_roles(new_role)
      i+=1
    N_a["status"] = "f"
    N_a["mode"] = mode
    all_file[Nfile] = N_a
    write_file("all_file",all_file)
    await message.channel.send("成功")
  @commands.command(aliases=["結束地城探索","結束探索地城"])
  async def New_Year_leave(self,message):
    if(message.channel.id == 897696095734497330 or message.channel.id == 938077684393709568 or message.channel.id == 938077714970206298 or message.channel.id == 938077741201383424 or message.channel.id == 938077778027376701):
      pass
    else:
      return
    ID = message.author.id
    activity = read_file("activity")
    if(str(ID) not in str(activity["list"].keys())):
      await message.channel.send("您目前無加入小隊")
      return
    party_number = activity["list"][str(ID)]
    Nfile = "New_Year_"+str(party_number)
    all_file = read_file("all_file")
    N_a = all_file[Nfile]
    if(N_a["status"] != "f"):
      await message.channel.send("您的隊伍還未出發")
      return
    if(N_a["leader"] != message.author.id):
      return
    guild = self.bot.get_guild(782593702455279616)
    mode = N_a["mode"]
    if(mode == "極"):
      mode = 1
      role_ID = 938077968712990801
    elif(mode == "強"):
      mode = 0.75
      role_ID = 938078032676143104
    elif(mode == "中"):
      mode = 0.5
      role_ID = 938078081502036019
    elif(mode == "弱"):
      mode = 0.25
      role_ID = 938078117162004490
    L = N_a["list"]
    L = L.split(",")
    i = 0
    show = ""
    a = N_a["reward"][0]
    b = N_a["reward"][1]
    await message.channel.send("本次探索讓所有人獲得了紅包"+str(a)+"個，經驗藥水"+str(b)+"瓶")
    while(i<len(L)):
      if(L[i]!=""):
        User = get_user(str(L[i]))
        if("exp_potion" in str(User.keys())):
          User["exp_potion"] += b
        else:
          User["exp_potion"] = b
        if(User["activity"] != "New_Year"):
          User["activity"] = "New_Year"
          User["money"] = a
        else:
          User["money"] += a
        put_user(str(L[i]),User)
        AID = int(L[i])
        member = guild.get_member(AID)
        new_role = guild.get_role(role_ID)
        await member.remove_roles(new_role)
      i+=1
    activity = read_file("activity")
    i = 0
    while(i<len(L)):
      if(L[i]!=""):
        del activity["list"][str(L[i])]
      i+=1
    del all_file[Nfile]
    write_file("all_file",all_file)
    write_file("activity",activity)
    await message.channel.send("獎勵頒發完成")
  @commands.command(aliases=["地城探索","探索地城"])
  async def New_Year_search(self,message):
    if(message.channel.id == 897696095734497330 or message.channel.id == 938077684393709568 or message.channel.id == 938077714970206298 or message.channel.id == 938077741201383424 or message.channel.id == 938077778027376701):
      pass
    else:
      return
    ID = message.author.id
    activity = read_file("activity")
    if(str(ID) not in str(activity["list"].keys())):
      await message.channel.send("您目前無加入小隊")
      return
    party_number = activity["list"][str(ID)]
    Nfile = "New_Year_"+str(party_number)
    all_file = read_file("all_file")
    N_a = all_file[Nfile]
    mode = N_a["mode"]
    name = N_a["name"]
    if(N_a["monster"][0]!=""):
      await message.channel.send("目前遭遇的野怪尚未解決，無法繼續往前探索")
      return
    if(mode == "極"):
      mode = 0.5
    elif(mode == "強"):
      mode = 0.35
    elif(mode == "中"):
      mode = 0.25
    elif(mode == "弱"):
      mode = 0.1
    if(N_a["leader"] != message.author.id):
      return
    R = random.randint(1,10)
    if(R == 9):
      N_a["reward"][2]+=int(10*mode)
      await message.channel.send("喔！隊伍"+name+"發現了"+str(int(10*mode))+"瓶回復藥水")
    elif(R == 10):
      N_a["reward"][0]+=int(10*mode)
      await message.channel.send("喔！隊伍"+name+"每個人發現了"+str(int(10*mode))+"包紅包")
    else:
      with open("activity_data.json","r",encoding="utf-8")as f:
        activity_data = json.load(f)
      ALL = activity_data["all"]
      ALL = random.randint(1,ALL)
      N_a["monster"][0] = NAME = activity_data[str(ALL)][0]
      N_a["monster"][1] = LV =int(activity_data[str(ALL)][1]*mode)
      N_a["monster"][2] = HP =int(activity_data[str(ALL)][2]*mode)
      N_a["monster"][3] = int(activity_data[str(ALL)][2]*mode)
      N_a["monster"][4] = ATK =int(activity_data[str(ALL)][3]*mode)
      N_a["monster"][5] = DEF =int(activity_data[str(ALL)][4]*mode)
      N_a["monster"][6] = SPD =int(activity_data[str(ALL)][5]*mode)
      N_a["monster"][7] = activity_data[str(ALL)][6]
      Power = power(ATK,DEF,SPD,HP,LV)
      embed = discord.Embed(title=NAME,description=name,color=0xeee657)
      embed.add_field(name="戰鬥力:", value=str(Power), inline=False)
      embed.add_field(name="等級:", value=str(LV), inline=False)
      embed.add_field(name="血量:", value=str(HP)+"/"+str(HP), inline=False)
      embed.add_field(name="攻擊力:", value=str(ATK), inline=False)
      embed.add_field(name="防禦力:", value=str(DEF), inline=False)
      embed.add_field(name="速度:", value=str(SPD), inline=False)
      await message.channel.send(embed=embed)
    all_file[Nfile] = N_a
    write_file("all_file",all_file)
  @commands.command(aliases=["我來攻擊","交給我吧"])
  async def New_Year_fight(self,message,number:int):
    if(message.channel.id == 897696095734497330 or message.channel.id == 938077684393709568 or message.channel.id == 938077714970206298 or message.channel.id == 938077741201383424 or message.channel.id == 938077778027376701):
      pass
    else:
      return
    ID = message.author.id
    activity = read_file("activity")
    User = get_user(str(ID))
    if(str(ID) not in str(activity["list"].keys())):
      await message.channel.send("您目前無加入小隊")
      return
    party_number = activity["list"][str(ID)]
    Nfile = "New_Year_"+str(party_number)
    all_file = read_file("all_file")
    N_a = all_file[Nfile]
    if(N_a["monster"][0]==""):
      await message.channel.send("目前未遭遇野怪")
      return
    if(str(number) not in str(N_a[str(ID)].keys())):
      await message.channel.send("您沒有設定該角色")
      return
    name = N_a["name"]
    mode = N_a["mode"]
    if(mode == "極"):
      mode = 0.5
    elif(mode == "強"):
      mode = 0.35
    elif(mode == "中"):
      mode = 0.25
    elif(mode == "弱"):
      mode = 0.1
    User = N_a[str(ID)][str(number)]
    Monster = N_a["monster"]
    CardId = User[0]
    with open("data.json","r",encoding="utf-8")as f:
      Data = json.load(f)
    MNAME = Data["card"][CardId-2001]
    MLV = User[1]
    MEXP = User[2]
    MHP = User[3]
    MATK = User[4]
    MDEF = User[5]
    MSPD = User[6]
    arm1 = User[7]
    skt1 = User[8]
    skn1 = User[9]
    mNAME = Monster[0]
    mLV = Monster[1]
    mHP = Monster[2]
    mATK = Monster[4]
    mDEF = Monster[5]
    mSPD = Monster[6]
    reward = Monster[7]
    L,co,who,hp1,hp2= fight(MNAME,MLV,MHP,MATK,MDEF,MSPD,mNAME,mLV,mHP,mATK,mDEF,mSPD,1,1,0,0,skt1,skn1,0,0)
    s = StringIO()
    s.write(L)
    s.seek(0)
    await message.channel.send(file=discord.File(s, filename="fight.txt"))
    hp1 += random.randint(5,int(100*mode))
    if(hp1<0):
      hp1 = int(random.randint(1,50)*mode)
    show = MNAME+"對"+mNAME+"造成了"+str(hp2)+"點傷害\n"+mNAME+"對"+MNAME+"造成了"+str(hp1)+"點傷害\n"
    N_a[str(ID)][str(number)][2] -= hp1
    MHP = N_a[str(ID)][str(number)][2]
    N_a["monster"][2] -= hp2
    mHP = N_a["monster"][2]
    if(MHP<=0):
      show += MNAME+"戰敗，血量歸零死亡\n"
      del N_a[str(ID)][str(number)]
    if(mHP<=0):
      show += mNAME+"戰敗，血量歸零死亡\n"
      N_a["monster"][0] = ""
      if(reward == 0):
        R = random.randint(10,30)
        R = int(R*mode)
        N_a["reward"][0] += R
        show += "隊伍"+name+"每個人獲得了紅包"+str(R)+"個\n"
      elif(reward == 1):
        N_a["reward"][1] += 1
        show += "隊伍"+name+"每個人獲得了經驗藥水1瓶\n"
      elif(reward == 2):
        R = random.randint(1,5)
        N_a["reward"][2] += R
        show += "隊伍"+name+"獲得了回復藥水"+str(R)+"瓶\n"
    else:
      show += mNAME+"剩餘血量"+str(mHP)+"\n"
    all_file[Nfile] = N_a
    write_file("all_file",all_file)
    await message.channel.send(show)
  @commands.command(aliases=["恢復藥水","恢復","使用恢復藥水","回復藥水","使用回復藥水","回復"])
  async def New_Year_re(self,message,number:int):
    if(message.channel.id == 897696095734497330 or message.channel.id == 938077684393709568 or message.channel.id == 938077714970206298 or message.channel.id == 938077741201383424 or message.channel.id == 938077778027376701):
      pass
    else:
      return
    ID = message.author.id
    activity = read_file("activity")
    if(str(ID) not in str(activity["list"].keys())):
      await message.channel.send("您目前無加入小隊")
      return
    party_number = activity["list"][str(ID)]
    Nfile = "New_Year_"+str(party_number)
    all_file = read_file("all_file")
    N_a = all_file[Nfile]
    if(N_a["reward"][2]<=0):
      await message.channel.send("持有的回復藥水不足")
      return
    if(str(number) not in str(N_a[str(ID)].keys())):
      await message.channel.send("您沒有設定該角色")
      return
    N_a[str(ID)][str(number)][2]+=10
    N_a["reward"][2] -= 1
    if(N_a[str(ID)][str(number)][2]>N_a[str(ID)][str(number)][3]):
      N_a[str(ID)][str(number)][2] = N_a[str(ID)][str(number)][3]
    all_file[Nfile] = N_a
    write_file("all_file",all_file)
    await message.channel.send("成功")
  @commands.command(aliases=["紅包總覽","紅包總懶","紅包總攬","紅包","紅包資訊"])
  async def New_Year_money(self,message):
    ID = str(message.author.id)
    User = get_user(str(ID))
    embed = discord.Embed(title="紅包總覽-2022新年活動",description=str(message.author),color=0xeee657)
    if(User["activity"] != "New_Year" or User["money"] == ""):
      User["money"] = 0
    embed.add_field(name="持有紅包數：", value=User["money"], inline=False)
    show="(1)石頭×100：10000紅包\n(2)角色重設券：5000紅包\n(3)石頭×10：1200紅包\n(4)裝備「打虎棒」：1500紅包\n(5)裝備「刮刮樂」：1500紅包\n(6)裝備「新衣」：1500紅包\n(7)裝備「煙火」：1500紅包\n(8)經驗藥水：500紅包\n(9)姆咪幣×1000：170紅包\n(10)必中券：90紅包\n(11)通行券：15紅包\n(12)交換點數×1：1紅包"
    embed.add_field(name="可用紅包兌換的商品：", value=show, inline=False)
    embed.set_footer(text="若需用紅包兌換商品請用\"紅包交換 商品編號 數量\"")
    await message.channel.send(embed=embed)
  @commands.command(aliases=["紅包交換","紅包兌換"])
  async def New_Year_money_change(self,message,number:int,much:int):
    ID = str(message.author.id)
    User = get_user(str(ID))
    if(number >= 13 or number <= 0):
      await message.channel.send("商品編號輸入錯誤")
      return
    if(much <= 0):
      await message.channel.send("數量輸入錯誤")
      return
    if(User["activity"] != "New_Year" or User["money"] == ""):
      User["money"] = 0
    money = User["money"]
    if(number == 1 and money>=(10000*much)):
      if(User['stone']==""):
        User['stone'] = 0
      User["stone"] += 100*much
      User["money"] -= 10000*much
    elif(number == 2 and money>=(5000*much)):
      if("role_reset" in str(User.keys())):
        User["role_reset"] += much
      else:
        User["role_reset"] = much
      User["money"] -= 5000*much
    elif(number == 3 and money>=(1200*much)):
      if(User['stone']==""):
        User['stone'] = 0
      User["stone"] += 10*much
      User["money"] -= 1200*much
    elif(number == 4 and money>=1500):
      if(much != 1):
        await message.channel.send("裝備商品一次只能購買一個")
        return
      arms = 20005
      i = 1
      f = "t"
      while(i<=10 and f == "t"):
        if(User["arms"][str(i)][0] == 0):
          User["arms"][str(i)][0] = arms
          User["arms"][str(i)][2] = 1
          User["arms"][str(i)][3] = 100003
          f = "f"
        i += 1
      if(f == "t"):
        await message.channel.send("裝備包包無空間，無法兌換")
        return
      User["money"] -= 1500
    elif(number == 5 and money>=1500):
      if(much != 1):
        await message.channel.send("裝備商品一次只能購買一個")
        return
      arms = 20006
      i = 1
      f = "t"
      while(i<=10 and f == "t"):
        if(User["arms"][str(i)][0] == 0):
          User["arms"][str(i)][0] = arms
          User["arms"][str(i)][2] = 1
          User["arms"][str(i)][3] = 100004
          f = "f"
        i += 1
      if(f == "t"):
        await message.channel.send("裝備包包無空間，無法兌換")
        return
      User["money"] -= 1500
    elif(number == 6 and money>=1500):
      if(much != 1):
        await message.channel.send("裝備商品一次只能購買一個")
        return
      arms = 20007
      i = 1
      f = "t"
      while(i<=10 and f == "t"):
        if(User["arms"][str(i)][0] == 0):
          User["arms"][str(i)][0] = arms
          User["arms"][str(i)][2] = 1
          User["arms"][str(i)][3] = 100005
          f = "f"
        i += 1
      if(f == "t"):
        await message.channel.send("裝備包包無空間，無法兌換")
        return
      User["money"] -= 1500
    elif(number == 7 and money>=1500):
      if(much != 1):
        await message.channel.send("裝備商品一次只能購買一個")
        return
      arms = 20008
      i = 1
      f = "t"
      while(i<=10 and f == "t"):
        if(User["arms"][str(i)][0] == 0):
          User["arms"][str(i)][0] = arms
          User["arms"][str(i)][2] = 1
          User["arms"][str(i)][3] = 100006
          f = "f"
        i += 1
      if(f == "t"):
        await message.channel.send("裝備包包無空間，無法兌換")
        return
      User["money"] -= 1500
    elif(number == 8 and money>=(500*much)):
      if("exp_potion" in str(User.keys())):
        User["exp_potion"] += much
      else:
        User["exp_potion"] = much
      User["money"] -= 500*much
    elif(number == 9 and money>=(170*much)):
      User["point"] += 1000*much
      User["money"] -= 170*much
    elif(number == 10 and money>=(90*much)):
      if(User['specialchange']==""):
        User['specialchange'] = 0
      User["specialchange"] += much
      User["money"] -= 90*much
    elif(number == 11 and money>=(15*much)):
      User["m_pass"] += much
      User["money"] -= 15*much
    elif(number == 12 and money>=(1*much)):
      User["re"] += much
      User["money"] -= much
    else:
      await message.channel.send("持有的紅包數不足")
      return
    put_user(str(ID),User)
    await message.channel.send("兌換成功")
  @commands.command(aliases=["魔王設定年獸"])
  async def New_Year_set_boss(self,message,mode:str):
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
    boss = {}
    boss["fight"] = "t"
    boss["boss"] = "年獸"
    name = "年獸"
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
  '''@commands.command(aliases=["過年野怪"])
  async def New_Year_monster(self,message,number:int):
    with open("wild_monster.json","r",encoding="utf-8")as f:
      W = json.load(f)
    W["mode"] = number
    with open("wild_monster.json","w",encoding="utf-8")as f:
      json.dump(W,f)
    await message.channel.send("成功")'''
  @commands.command(aliases=["紅包測試"])
  async def New_Year_money_test(self,message):
    if(message.author.id!=550907252970749952):
      return
    ID = str(message.author.id)
    User = get_user(str(ID))
    User["money"] = 1000000000000
    put_user(ID,User)
    await message.channel.send("成功")
def setup(bot):
  bot.add_cog(New_Year(bot))