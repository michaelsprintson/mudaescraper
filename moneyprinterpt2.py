
# Import the os module.
from time import sleep
import re
import json
from discum.utils.button import Buttoner
from functools import reduce
import pickle
from dotenv import load_dotenv
import os
import numpy as np
from datetime import datetime as dt
from datetime import timedelta
load_dotenv()
# Grab the API token from the .env file.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN1")


from collections import defaultdict
import discum     
bot = discum.Client(token=DISCORD_TOKEN, log=False)
start_time = dt.now()
sleepcount = 0
last_roll = dt.now() - timedelta(hours = 2)
import time
num_bots = 6
SPAM_CHANNEL = "980201775950868532"
admin_bot_id = "978030120734445628"


@bot.gateway.command
def helloworld(resp):
    global start_time, sleepcount, last_roll
    
    if resp.event.message:
        m = resp.parsed.auto()
        if m['content'][0:8] == "$botecho":
            if m['channel_id'] == SPAM_CHANNEL:
                if m['author']['id'] == admin_bot_id:
                    bot.sendMessage(SPAM_CHANNEL, m['content'][9:])


    if resp.event.ready_supplemental: #ready_supplemental is sent after ready
        user = bot.gateway.session.user
        print("Logged in as {}#{}".format(user['username'], user['discriminator']))
        
        while(1):
            while int((dt.now() -last_roll).seconds) < 7200:
                sleep(720)
            last_roll = dt.now()
            print(f"betting, current time - {dt.now()}, {int((dt.now() -last_roll).seconds)} elapsed since last roll,  {sleepcount} elapsed since dk")
            for i in range(0,num_bots):
                print(f'calling autobet {i+1}')
                bot.sendMessage(SPAM_CHANNEL, f'$autobet {i+1}')
                time.sleep(80)
            

            
            # sleepcount += 7200
            # if sleepcount > 36000:
            #     bot.sendMessage("980201775950868532", '$dk') # change to make the indiv bots run this
            #     sleepcount = 0
    
   


bot.gateway.run(auto_reconnect=True)
