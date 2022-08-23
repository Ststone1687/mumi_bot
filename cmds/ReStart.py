import discord
from discord.ext import commands
from datetime import datetime
from discord.ext import commands
from discord.utils import get
import json
import random
import time
import sys
import os
import asyncio
import math
from core.classes import Cog_Extension

class ReStart(Cog_Extension):

  @commands.Cog.listener()
  async def on_message(self,message):
    U = str(message.channel.id)
    if(U == "707975903900205157" or U == "695838524813082624"):
      pass
    else:
      return
    if message.content.startswith("S785g58SG4jg65HZ5HX5"):
      await message.channel.send("請稍等")
      python = sys.executable
      os.execl(python, python, *sys.argv)

def setup(bot):
  bot.add_cog(ReStart(bot))