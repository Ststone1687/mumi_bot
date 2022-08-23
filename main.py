import discord
intents = discord.Intents.default()
intents.members = True
from discord.ext import commands
bot = commands.Bot(command_prefix='',intents=intents)
from discord.utils import get
from replit import db
import flask
from keep_alive import keep_alive
import json
import random
import time
import sys
import os
import asyncio
import math
import datetime


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

#db["User"] = move_file("all_user")
#db["User"] = {}

#db["daysign"] = {"list": "","today" : today}
#db["shop"] = move_file("shop")
#db["change"] = move_file("change")  
#db["sell"] = move_file("sell")
#db["fishing"] = move_file("fishing")
#db["Fish_market"] = move_file("Fish_market")
#db["power_rank"] = move_file("power_rank")
#db["boss"] = move_file("boss")
#db["day_rank"] = move_file("day_rank")
#db["arms_shop"] = move_file("arms_shop")

token = db["token"]

# add restart and wait
@bot.event  #登入成功
async def on_ready():
  print('Logged in as')
  print(bot.user.name)
  print(bot.user.id)
  print('------')
  #wait.json reset
  mydict = {'sec': "0"}
  write_file('wait',mydict)
  t = "t"
  while (t == "t"):
    if (int(datetime.datetime.now().minute) <= 10):
      data = read_file("restart")
      hour = data["hour"]
      if (str(hour) == str(datetime.datetime.now().hour)):
        pass
      else:
        data["hour"] = str(datetime.datetime.now().hour)
        write_file("restart",data)
    await asyncio.sleep(300)

@bot.command()
async def load(message, File):
  if(message.author.id != 550907252970749952):
    return
  bot.load_extension(F'cmds.{File}')
  await message.channel.send("load成功")


@bot.command()
async def unload(message, File):
  if(message.author.id != 550907252970749952):
    return
  bot.unload_extension(F'cmds.{File}')
  await message.channel.send("unload成功")


@bot.command()
async def reload(message, File):
  if(message.author.id != 550907252970749952):
    return
  bot.reload_extension(F'cmds.{File}')
  await message.channel.send("reload成功")

for Filename in os.listdir("./cmds"):
	if Filename.endswith(".py"):
		bot.load_extension(F'cmds.{Filename[:-3]}')

if __name__ == "__main__":
  keep_alive()
  bot.run(token)