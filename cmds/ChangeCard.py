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

class ChangeCard(Cog_Extension):
  @commands.command()
  async def 交換卡片(self,message, card: str):
    ID = str(message.author.id)
    if(check_user(ID)):
        c = read_file("change")
        if ("user1" in str(c)):
          await message.channel.send("有其他玩家在交換中，請稍等")
          return
        t = get_user(ID)
        cc = t['re']
        tcard = t['card']
        filename = "NameData.json"
        with open(filename, 'r', encoding='utf-8') as file:
          data = json.load(file)
          no = data[card]
          if (str(no) in str(tcard)):
            mydict = {'user1': message.author.id, 'card1': no}
            write_file("change",mydict)
            await message.channel.send('<@' + str(message.author.id) +'> 請要交換的玩家輸入 回應交換 [卡片]')
            await message.channel.send("提醒：請在60秒內交換完成")
            await asyncio.sleep(60)
            data = read_file("change")
            if ("user1" in str(data)):
              await message.channel.send("使用者回應逾時")
              mydict = {}
              write_file("change",mydict)
          else:
              await message.channel.send('<@' + str(message.author.id) +'> 您沒有這張卡啦 <:mumi5:610498110120132679>  ')
    else:
      await message.channel.send('<@' + str(message.author.id) +'> 請先輸入 註冊 完成註冊<:mumi:609708401513070602> ')
  @commands.command()
  async def 回應交換(self,message, card: str):
    ID = str(message.author.id)
    if(check_user(ID)):
      t = get_user(ID)
      tcard = t['card']
      filename = "NameData.json"
      with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
      no = data[card]
      if (str(no) in str(tcard)):
        c = read_file("change")
        try:
          user1 = c['user1']
        except KeyError:
          await message.channel.send("請要交換的玩家，先輸入 交換卡片 [卡片]")
          return
        if (str(user1) == str(message.author.id)):
          mydict = {}
          write_file("change",mydict)
          await message.channel.send("交換失敗，不能跟自己交換拉")
          return
        card1 = c['card1']
        d = get_user(str(user1))
        dcard = d['card']
        one = str(no)
        two = str(card1)
        tttcard = tcard.replace(one, two)
        dddcard = dcard.replace(two, one)
        t['card'] = tttcard
        d['card'] = dddcard
        ta = t['assistant']
        da = d['assistant']
        if (str(one) == str(ta)):
          t['assistant'] = "0"
        if (str(two) == str(da)):
          d['assistant'] = "0"
        put_user(ID,t)
        put_user(str(user1),d)
        await message.channel.send('交換成功')
        mydict = {}
        write_file("change",mydict)
      else:
        await message.channel.send('<@' + str(message.author.id) +'> 您沒有這張卡啦')
    else:
      await message.channel.send('<@' + str(message.author.id) +'> 請先輸入 註冊 完成註冊<:mumi:609708401513070602> ')
      



    

def setup(bot):
  bot.add_cog(ChangeCard(bot))