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


class Ststone(Cog_Extension):
    @commands.command(aliases=["好啦我跟你道歉，我補償東西給你這樣總可以了吧。這麼長的指令應該也沒有人想打吧。"],help="0姆咪幣；1交換點數；2金幣；3石頭；4必中券")
    async def st_sorry(self,message, who: str,thing:int,number:int):
        if(message.author.id!=550907252970749952):
            await message.channel.send("你還真的打了，笑死")
            return
        n = number
        ID = who.strip('<@!>')
        t = get_user(ID)
        if(thing==0):#姆咪幣
            t["point"] += n
            await message.channel.send("給予了"+who+str(n)+"姆咪幣")
        if(thing==1):#交換點數
            t["re"] += n
            await message.channel.send("給予了"+who+str(n)+"交換點數")
        if(thing==2):#金幣
            t["pis"] += n
            await message.channel.send("給予了"+who+str(n)+"金幣")
        if(thing==3):#石頭
            t["stone"] += n
            await message.channel.send("給予了"+who+str(n)+"石頭")
        if(thing==4):#必中券
            t["specialchange"] += n
            await message.channel.send("給予了"+who+str(n)+"必中券")
        put_user(ID,t)
        await message.channel.send("成功")
    @commands.command()
    async def download_f(self,message):
      database = str(db["User"])
      with open("all_user_bot.txt", 'w') as f:
        f.write(database)
      await message.channel.send("成功")
def setup(bot):
  bot.add_cog(Ststone(bot))