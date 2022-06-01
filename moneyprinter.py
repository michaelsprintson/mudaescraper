
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
import sys
load_dotenv()
# Grab the API token from the .env file.
bot_num =sys.argv[1]
DISCORD_TOKEN = os.getenv(f"DISCORD_TOKEN{bot_num}")
# demon's sword master of excalibur school.

srape_location = "big_scrape.json"
scrape_channel = None

from collections import defaultdict
import discum     
bot = discum.Client(token=DISCORD_TOKEN, log=False)

import asyncio
import time

roll_i = None
username = None

class roll_instance():
    def __init__(self):
        self.cur_rolls = []
        self.rollcount = 0
        self.rollmax = 15


@bot.gateway.command
def helloworld(resp):
    global scrape_channel, roll_i, bot_num,username
    
    if resp.event.ready_supplemental: #ready_supplemental is sent after ready
        user = bot.gateway.session.user
        username = user['username']
        print("Logged in as {}#{}".format(user['username'], user['discriminator']))
    
    if resp.event.message:
        m = resp.parsed.auto()
        
        roll_channel_id = m['channel_id']
        
        if roll_channel_id == '980201775950868532':
            m = resp.parsed.auto()
            if m['content'] == "$autobet {}".format(bot_num):
                roll_i = roll_instance()
                # bot.reply(m['channel_id'], m['id'], "ðŸ‘»")
                
                # bot.addReaction(m['channel_id'], m['id'], "sad_pirate:980994471544115231")
                sleep(2)
                bot.sendMessage(m['channel_id'],f"$dk")
                sleep(3)
                bot.sendMessage(m['channel_id'],f"$daily")
                sleep(3)
                for i in range(0,15):
                    sleep(1)
                    bot.sendMessage(m['channel_id'],f"$wa")
                
            
            if (len(m['embeds']) > 0) and (m['author']['id'] == "432610292342587392"): #and (messagan == "Mudae"): #make sure this is only from mudae
            #someone was rolled
                e = m['embeds'][0]
                desc = e['description']
                # if not type(an) == discord.embeds._EmptyEmbed:
                if "Harem size:" in desc:
                    if (('author' in e) and ('name' in e['author'])):
                        if e['author']['name'] == username:
                            s = re.search("(?P<word>\*\*\d+\*\*)", desc)
                            if not s is None:
                                kval = int(s.group().strip("**")) #change for wishes and owneds
                                time.sleep(2)
                                if not username == "kjh":
                                    bot.sendMessage(m['channel_id'],f"$givek 978105521754218547 {kval}")
                                    time.sleep(2)
                                    bot.sendMessage(m['channel_id'],f"y")
                else:
                    if (('author' in e) and ('name' in e['author'])):
                        # an = e['author']['name']
                        # if not (("Like Rank" in desc or "Claim Rank" in desc) or ("Custom" in desc) or ("Harem size:" in desc) or ("Kakera" in desc) or ("TOP 1000" in an) or ("kakera" in an) or ("Kakera" in an) or ("harem" in an) or ("disablelist" in an) or ("Total value:" in desc)): #really shit way to make sure it was a roll
                        if "**" in desc:
                            s = re.search("(?P<word>\*\*\d+\*\*)", desc)
                            if not s is None:
                                kval = int(s.group().strip("**")) #change for wishes and owneds
                                kname = e['author']['name']

                                if roll_i is None:
                                    print(f'ignoring {kname} because roll_i is None')
                                else:
                                    roll_i.rollcount+=1
                                    if (len(m['components'])) == 0:
                                        roll_i.cur_rolls.append([m['id'], kval, kname])
                                        print(f"rolled value {kval} in message id {m['id']}")
                                    else:
                                        print(f"rolled value {kval} in message id {m['id']}, ignored because pre-owned or wish")
                                    if roll_i.rollcount == roll_i.rollmax:
                                        highest_val_message = sorted(roll_i.cur_rolls, key=lambda x: -x[1])[0]
                                        print('highest val', highest_val_message[1], 'message id', highest_val_message[0])
                                        roll_i = None
                                        bot.addReaction(m['channel_id'], highest_val_message[0], "sad_pirate:980994471544115231")
                                        time.sleep(2)
                                        bot.sendMessage(m['channel_id'],f"$divorce {highest_val_message[2]}")
                                        time.sleep(2)
                                        bot.sendMessage(m['channel_id'],f"y")
                                        time.sleep(2)
                                        bot.sendMessage(m['channel_id'],f"$givek 978105521754218547 {highest_val_message[1]}")
                                        time.sleep(2)
                                        bot.sendMessage(m['channel_id'],f"y")


bot.gateway.run(auto_reconnect=True)
