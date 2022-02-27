#!/usr/bin/env python3
import sys, re
from javascript import require, On
mineflayer = require('mineflayer')
pathfinder = require('mineflayer-pathfinder')

RANGE_GOAL = 1

bot = mineflayer.createBot({
    "host": "127.0.0.1",
    "port": "25565",
    "username": "xxxxx",
    "password": "xxxxx"
})

bot.loadPlugin(pathfinder.pathfinder)
print("Started mineflayer")
@On(bot, 'spawn')
def handle(*args):
  print("I spawned")
  mcData = require('minecraft-data')(bot.version)

def moveTo(xyz):
  pos = xyz.position
  try:
    bot.pathfinder.setMovements(pathfinder.Movements(bot, require('minecraft-data')(bot.version)))
    bot.pathfinder.setGoal(pathfinder.goals.GoalNear(pos.x, pos.y, pos.z, RANGE_GOAL))
  except:
    bot.chat("Too far away or in an unreachable area!")
    
@On(bot, 'chat')
def handleMsg(this, sender, message, *args):
  print("Got message", sender, message)
  if sender and (sender != bot.username):
    player = bot.players[sender]
    if 'come' in message:
      print("Target", player)
      target = player.entity
      if not target:
        bot.chat("I don't see you !")
        return
      moveTo(player.entity)
    if('goto' in message):
      try:
        x, y, z = map(lambda v: int(v), message.split("goto")[1].replace(",", " ").split())
        bot.pathfinder.setMovements(pathfinder.Movements(bot, require('minecraft-data')(bot.version)))
        bot.pathfinder.setGoal(pathfinder.goals.GoalNear(x, y, z, RANGE_GOAL))
      except Exception:
        bot.chat("Bad syntax")

@On(bot, "end")
def handle(*args):
  print("Bot ended!", args)
  sys.exit()

@On(bot, "kicked")
def kicked(this, reason, *a):
    print("I was kicked",reason,a)
    sys.exit()
