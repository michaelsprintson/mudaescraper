
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
from threading import Event
load_dotenv()
# Grab the API token from the .env file.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN1")


from collections import defaultdict
import discum     
bot = discum.Client(token=DISCORD_TOKEN, log=False)
start_time = dt.now()
sleepcount = 0
last_roll = dt.now() - timedelta(minutes = 60)
import time
num_bots = 6
SPAM_CHANNEL = "980201775950868532"
admin_bot_id = "978030120734445628"
disabled_dict = json.load(open("../mudaegambling/storage_dicts/ser_dl.json"))
final_dict = None

bot_ids = [
    978105521754218547,
    981208263548866700,
    981228944743338074,
    981320875351605279,
    981323272887095366,
    981324103120224276,
]

bot_finish = Event()
pr_finish = Event()
reset_finish = Event()

@bot.gateway.command
def helloworld(resp):
    global start_time, sleepcount, last_roll, disabled_dict, final_dict
    
    if resp.event.message:
        m = resp.parsed.auto()
        if m['content'][0:8] == "$botecho":
            if m['channel_id'] == SPAM_CHANNEL:
                if m['author']['id'] == admin_bot_id:
                    bot.sendMessage(SPAM_CHANNEL, m['content'][9:])
        if m['content'] == "$allbotreset":

            bot.sendMessage(SPAM_CHANNEL,f"$specbotreset 1")
            reset_finish.wait(timeout = 60)

            for i in range(1,num_bots):
                sleep(1)
                bot.sendMessage(SPAM_CHANNEL,f"$givek {bot_ids[i]} 30000")
                time.sleep(2)
                bot.sendMessage(SPAM_CHANNEL,"y")
                time.sleep(2)
                bot.sendMessage(SPAM_CHANNEL,f"$specbotreset {i+1}")
                reset_finish.wait(timeout = 60)

                bot.sendMessage(SPAM_CHANNEL,f"$pr {bot_ids[i]}")
                pr_finish.wait(timeout = 30)
            bot.sendMessage(SPAM_CHANNEL,f"$pr {bot_ids[0]}")

        if "finished" == m['content'] and int(m['author']['id']) in bot_ids:
            print("bot finished, going to next")
            bot_finish.set()
            bot_finish.clear()
        if "prfinished" == m['content'] and int(m['author']['id']) in bot_ids:
            print("pr finished, going to next")
            pr_finish.set()
            pr_finish.clear()
        if "resetfinished" == m['content'] and int(m['author']['id']) in bot_ids:
            print("reset finished, going to next")
            reset_finish.set()
            reset_finish.clear()


    if resp.event.ready_supplemental: #ready_supplemental is sent after ready
        user = bot.gateway.session.user
        ids = bot.getRoleMemberIDs("887538091735257108","971968839959081020").json()
        print("Logged in as {}#{}".format(user['username'], user['discriminator']))
        # if final_dict is None:

        #     for id in ids:
        #         bot.sendMessage(SPAM_CHANNEL, f"$wlt {id}")
        #         sleep(2)
        #     final_dict = defaultdict(int)
        #     for d in disabled_dict.values():
        #         for k,v in d.items():
        #             final_dict[k] += v
        #     to_disable = sorted(final_dict, key = lambda x: final_dict[x])[-10:]
        #     inner_d = reduce(lambda a,b: a + b, [f" ${sername}" for sername in to_disable[1:]])
        #     command_to_run = f"$disable {to_disable[0]} {inner_d}"
        #     # bot.sendMessage(SPAM_CHANNEL, "$allbotecho " + "$enableall")
        #     bot.sendMessage(SPAM_CHANNEL, "$allbotecho " + command_to_run)
        while(1):
            while int((dt.now() -last_roll).seconds) < 3600:
                if int((dt.now() -last_roll).seconds) > 3000:
                    print(dt.now(), int((dt.now() -last_roll).seconds), "sleeping another 60")
                    sleep(60)
                else:
                    print(dt.now(), int((dt.now() -last_roll).seconds), "sleeping another 720")
                    sleep(720)
            

            sleepcount = 1-sleepcount
            last_roll = dt.now()
            print(f"betting, current time - {dt.now()}, {int((dt.now() -last_roll).seconds)} elapsed since last roll,  {sleepcount} elapsed since dk")
            for i in range(0,num_bots):
                print(f'calling autobet {i+1} {sleepcount}')
                sleep(1)
                bot.sendMessage(SPAM_CHANNEL,f"$givek {bot_ids[i]} 85000")
                time.sleep(2)
                bot.sendMessage(SPAM_CHANNEL,"y")
                time.sleep(2)

                bot.sendMessage(SPAM_CHANNEL, f'$autobet {i+1} {sleepcount}')
                bot_finish.wait(timeout = 300)

            for i in range(1,num_bots):
                bot.sendMessage(SPAM_CHANNEL,f"$pr {bot_ids[i]}")
                pr_finish.wait(timeout = 30)
            bot.sendMessage(SPAM_CHANNEL,f"$pr {bot_ids[0]}")
            

            
            # sleepcount += 7200
            # if sleepcount > 36000:
            #     bot.sendMessage("980201775950868532", '$dk') # change to make the indiv bots run this
            #     sleepcount = 0
    
   


bot.gateway.run(auto_reconnect=True)
