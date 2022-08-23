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

class Card(Cog_Extension):
  # arms.json for com
  @commands.command(aliases=["抽卡"])
  async def _Card_(self,message):
    ID = message.author.id
    User = get_user(str(ID))
    with open("data.json", 'r', encoding='utf-8') as file:
      data = json.load(file)
    if(message.channel.id == 897685629918400513):
      if(User["specialchange"] >= 1):
        User["specialchange"] -= 1
        pass
      else:
        await message.channel.send('<@'+str(ID)+'>持有的必中卷不足<:mumi8:610498200930877450>')
        return
    elif(message.channel.id == 897419002022871100 or message.channel.id == 897419037519249450):
      if(User["point"]>=100):
        User["point"] -= 100
        pass
      else:
        await message.channel.send('<@'+str(ID)+'>持有的姆咪幣不足<:mumi8:610498200930877450>')
        return
    else:
      await message.channel.send('<@'+str(ID)+'>此頻道不能抽卡啦 <:mumi5:610498110120132679>')
      return
    if(message.channel.id == 897685629918400513):
      card = random.randint(2129,2133)
      if(str(card) in User["card"]):
        await message.channel.send("已擁有的卡將轉換成交換點數×30")
        User["re"] += 30
      else:
        User["card"]+=str(card)+","
      put_user(str(ID),User)
      channel = self.bot.get_channel(897418210629021716)
      await channel.send("<:mumi01:897429705832169512> 玩家`"+str(message.author.name)+"`抽到了卡片`" +data["card"][card-2001]+"`<:mumi01:897429705832169512> ")
      datetime_now = datetime.datetime.now()
      time_range = datetime.timedelta(hours = 8)
      new_time = datetime_now+time_range
      await channel.send(" `time："+str(new_time)+"`")
      embed = discord.Embed(title=data["card"][card-2001], description="由玩家"+str(message.author.name)+"抽出",color=0xeee657)
      embed.set_image(url=data["link"][card-2001])
      await message.channel.send(embed=embed)
    elif(message.channel.id == 897419002022871100 or message.channel.id == 897419037519249450):
      R = random.randint(1,98)
      #抽卡品項：(100)
      #裝備(2)
      #卡片(2)
      #石頭(2)
      #經驗藥水(2)
      #金幣(15)
      #交換點數(77)
      if(R<=77):
        add = random.randint(5,15)
        User["re"] += add
        await message.channel.send("<@"+str(ID)+"> 抽到了交換點數×"+str(add))
        put_user(str(ID),User)
      elif(R<=92):
        add = random.randint(5,10)
        User["pis"] += add
        await message.channel.send("<@"+str(ID)+"> 抽到了金幣×"+str(add))
        put_user(str(ID),User)
      elif(R<=94):
        if("exp_potion" not in str(User.keys())):
          User["exp_potion"] = 1
        else:
          User["exp_potion"] += 1
        await message.channel.send("<@"+str(ID)+"> 抽到了經驗藥水×1")
        put_user(str(ID),User)
      elif(R<=96):
        add = random.randint(1,2)
        User["stone"] += add
        await message.channel.send("<@"+str(ID)+"> 抽到了石頭×"+str(add))
        put_user(str(ID),User)
      elif(R<=98):
        card = random.randint(2129,2133)
        if(str(card) in User["card"]):
          await message.channel.send("已擁有的卡將轉換成交換點數×30")
          User["re"] += 30
        else:
          User["card"]+=str(card)+","
        put_user(str(ID),User)
        channel = self.bot.get_channel(897418210629021716)
        await channel.send("<:mumi01:897429705832169512> 玩家`"+str(message.author.name)+"`抽到了卡片`" +data["card"][card-2001]+"`<:mumi01:897429705832169512> ")
        datetime_now = datetime.datetime.now()
        time_range = datetime.timedelta(hours = 8)
        new_time = datetime_now+time_range
        await channel.send(" `time："+str(new_time)+"`")
        embed = discord.Embed(title=data["card"][card-2001], description="由玩家"+str(message.author.name)+"抽出",color=0xeee657)
        embed.set_image(url=data["link"][card-2001])
        await message.channel.send(embed=embed)
      elif(R<=100):
        with open("arms.json","r",encoding="utf-8")as f:
          A = json.load(f)
        arms = random.randint(90022,90028)
        i = 1
        f = "t"
        while(i<=10 and f == "t"):
          if(User["arms"][str(i)][0] == 0):
            User["arms"][str(i)][0] = arms
            f = "f"
          i += 1
        if(f == "t"):
          await message.channel.send("裝備包包無空間，抽到的裝備將轉換成交換點數×30")
          User["re"] += 30
        put_user(str(ID),User)
        channel = self.bot.get_channel(897418210629021716)
        await channel.send("<:mumi01:897429705832169512> 玩家`"+str(message.author.name)+"`抽到了裝備`" +A[str(arms)][0]+"`<:mumi01:897429705832169512> ")
        datetime_now = datetime.datetime.now()
        time_range = datetime.timedelta(hours = 8)
        new_time = datetime_now+time_range
        await channel.send(" `time："+str(new_time)+"`")
        embed = discord.Embed(title=A[str(arms)][0], description=A[str(arms)][5]+"\n分類："+A[str(arms)][6],color=0xeee657)
        await message.channel.send(embed=embed)
    #備份用戶資料
    channel = self.bot.get_channel(740946306851143790)
    tsend = str(User)
    i_range = math.ceil(len(tsend)/1900) 
    for i in range(i_range):
      await channel.send("```" + tsend[(i*1900):(i+1)*1900] + "```")
    ###
  @commands.command(aliases=["我討厭石頭！我要姆咪幣啦！"])
  async def _no_stone_(self,message,c:int):
    ID = str(message.author.id)
    User = get_user(ID)
    if(User["stone"] >= c):
      pass
    else:
      await message.channel.send("不給你")
      return
    r = random.randint(1,10)
    if(r<6):
      User["stone"] -= c
      User["point"] += c*700
      await message.channel.send("好啦！"+str(c*700)+"姆咪幣拿去")
    else:
      await message.channel.send("不給你")
    put_user(ID,User)



def setup(bot):
  bot.add_cog(Card(bot))