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

class Cog_Extension(commands.Cog):
  def __init__ (self,bot):
    self.bot = bot
    