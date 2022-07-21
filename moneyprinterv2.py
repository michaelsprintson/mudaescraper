
# Import the os module.
from time import sleep
import re
import json
from tracemalloc import start
from typing import final
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
ROLL_NUM = 21
MUDAE_ID = "432610292342587392"
# demon's sword master of excalibur school.

srape_location = "big_scrape.json"
scrape_channel = None

from collections import defaultdict
import discum     
bot = discum.Client(token=DISCORD_TOKEN, log=False)

import asyncio
import time
from threading import Event, Lock
from discum.utils.slash import SlashCommander

roll_i = None
username = None
self_id = None
claim_or_not = 1

start_impulse = Event()

badge_confirm = Event()
badge_impulse = Event()
badge_skip = Event()

dk_impulse = Event()
daily_impulse = Event()
roll_response = Event()
married_impulse = Event()
divorce_confirm = Event()
divorce_impulse = Event()
reset_confirm = Event()
done_impulse = Event()
give_confirm = Event()
give_impulse = Event()

final_impulse = Event()

mudae_message_text_values_mapping = {"are now married!": married_impulse,
                                     "Do you confirm the divorce?": divorce_confirm,
                                     "are now divorced.": divorce_impulse,
                                     "kakera invested will be refunded.": reset_confirm,
                                     "Done.": done_impulse,
                                     "do you really want to give": give_confirm,
                                     "just gifted": give_impulse,
                                     "melt those kakera into a power badge?": badge_confirm,
                                     "You just reached": badge_impulse,
                                     "You already reached": badge_impulse, #TODO: FIX
                                     "Next $dk reset in": dk_impulse,
                                     "added to your kakera collection!": dk_impulse,
                                     "Next $daily reset in": daily_impulse,
}

def say_message(cid, thing, t = 2):
    time.sleep(t)
    bot.sendMessage(cid,thing)


class roll_instance():
    def __init__(self):
        self.cur_rolls = []
        self.rollcount = 0
        self.rollmax = ROLL_NUM
        self.married = False
    def marry(self, kname):
        self.married = True
        self.mname = kname


def give_money(desc,m):
    global username
    s = re.findall("(?P<word>\*\*\d+\*\*)", desc)
    if not len(s) == 0:
        kval = int(s[-1].strip("**")) #change for wishes and owneds
        time.sleep(2)
        if not username == "kjh":
            say_message(m['channel_id'], f"$givek 978105521754218547 {kval}")
            give_confirm.wait(timeout = 10) 
            say_message(m['channel_id'], "y")
            give_impulse.wait(timeout = 10)
            say_message(m['channel_id'], f"prfinished")
            start_impulse.clear()

def found_roll(e,m,s):
    global roll_i, claim_or_not, self_id
    kval = int(s.group().strip("**")) #change for wishes and owneds
    kname = e['author']['name']

    if roll_i is None:
        # print(f'ignoring {kname} because roll_i is None')
        pass
    else:
        roll_i.rollcount+=1
        if (len(m['components'])) == 0:
            print(f"rolled value {kval} in message id {m['id']}")
            roll_i.cur_rolls.append([m['id'], kval, kname])
        else:
            print(f"rolled value {kval} in message id {m['id']}, ignored because pre-owned or wish")
            if not ("Wished by" in m['content']):
                message = bot.getMessage(m['channel_id'], m['id'])
                data = message.json()[0]
                
                buttoner = Buttoner(m["components"])
                buts = [j['emoji']['name'] for i in [buttoner.findButton(label=None, customID=None, row=None, column=None, emojiName=f"kakera{l}", emojiID=None, findFirst=True) for l in ["","Y","L","G","O","R","W", "P"]] for j in i]
                
                
                if len(buts) > 0:
                    print(f"attempting to click on {buts[0]}")
                    bot.click(
                        data["author"]["id"],
                        channelID=data["channel_id"],
                        guildID=m['guild_id'],
                        messageID=data["id"],
                        messageFlags=data["flags"],
                        data=buttoner.getButton(emojiName=buts[0]),
                    )
    
        if roll_i.rollcount == roll_i.rollmax:
            print("ending rolls")
            highest_val_message = sorted(roll_i.cur_rolls, key=lambda x: -x[1])[0]
            print('highest val', highest_val_message[1], 'message id', highest_val_message[0])
            roll_i = None
            if claim_or_not == 1:
                bot.addReaction(m['channel_id'], highest_val_message[0], "sad_pirate:980994471544115231")
                print("waiting for marry")
                if married_impulse.wait(timeout = 10):
                    say_message(m['channel_id'], f"$divorce {highest_val_message[2]}")
                    if divorce_confirm.wait(timeout = 10):
                        say_message(m['channel_id'], "y")
                        divorce_impulse.wait(timeout = 10)
            
            reset_and_give(m)
            
            final_impulse.set()
            final_impulse.clear()

        else:
            print("need more rolls")
            roll_response.set()
            roll_response.clear()

def reset_and_give(m, give = True):
    global self_id
    say_message(m['channel_id'], f"$kakerareset {self_id}")
    reset_confirm.wait(timeout = 10)
    say_message(m['channel_id'], "confirm")
    done_impulse.wait(timeout = 10)

    if give:
        say_message(m['channel_id'],f"$givek 978105521754218547 85000")
        give_confirm.wait(timeout = 10)
        say_message(m['channel_id'], "y")
        give_impulse.wait(timeout = 10)

    say_message(m['channel_id'], "$gold 4")
    badge_confirm.wait(timeout = 10)
    say_message(m['channel_id'], "y")
    badge_impulse.wait(timeout = 10)

@bot.gateway.command
def helloworld(resp):
    global scrape_channel, roll_i, bot_num,username, claim_or_not, self_id
    
    if resp.event.ready_supplemental: #ready_supplemental is sent after ready
        user = bot.gateway.session.user
        self_id = user['id']
        username = user['username']
        print("Logged in as {}#{}".format(user['username'], user['discriminator']))

        # say_message("980201775950868532", f"$kakerareset {self_id}")
        # if reset_confirm.wait(timeout=10):
        #     say_message("980201775950868532", "confirm")
        #     done_impulse.wait()
        # else:
        #     print("timed out, continuting...")
    
    if resp.event.message:
        m = resp.parsed.auto()

        if m['channel_id'] == '997367196093272074':
            # print('made to roll channe')
            m = resp.parsed.auto()

            if m['content'][:10] == "$givemoney":
                if username == "kjh":
                    kname = m['content'].split(" ")[1]
                    kval = m['content'].split(" ")[2]
                    say_message(m['channel_id'], f"$givek {kname} {kval}")
                    give_confirm.wait(timeout = 3) 
                    say_message(m['channel_id'], "y")
                    give_impulse.wait(timeout = 3)
        
        if m['channel_id'] == '980201775950868532':
            # print('made to roll channe')
            m = resp.parsed.auto()

            if m['content'][:10] == "$givemoney":
                if username == "kjh":
                    kname = m['content'].split(" ")[1]
                    kval = m['content'].split(" ")[2]
                    say_message(m['channel_id'], f"$givek {kname} {kval}")
                    give_confirm.wait(timeout = 3) 
                    say_message(m['channel_id'], "y")
                    give_impulse.wait(timeout = 3)

            if m['content'][:11] == "$allbotecho":
                sleep(int(bot_num) * 2)
                bot.sendMessage(m['channel_id'],m['content'][12:])
            
            if (m['content'][:14] == f"$specbotecho {bot_num}") and m['author']['id'] == "138336085703917568":
                sleep(2)
                bot.sendMessage(m['channel_id'],m['content'][15:])
            
            if (m['content'][:15] == f"$specbotreset {bot_num}"):
                sleep(2)

                start_impulse.set()
                reset_and_give(m, give = False)
                start_impulse.clear()
                bot.sendMessage(m['channel_id'],"resetfinished")
            
            if m['content'][:10] == "$autobet {}".format(bot_num):
                start_impulse.set()
                roll_i = roll_instance()
                claim_or_not = int(m['content'][11:])

                for badge_name in ["$bronze 4","$gold 4","$ruby 4","$sapphire 4","$emerald 4"]:
                    say_message(m['channel_id'], badge_name)
                    print('getting')
                    badge_confirm.wait(timeout=10)
                    say_message(m['channel_id'], "y")
                    print("confirming")
                    # if not enough kakera, request more -- if already had, 
                    badge_impulse.wait(timeout=10)
                    print("got")
                
                say_message(m['channel_id'], "$dk")
                print("waiting on dk impulse")
                dk_impulse.wait(timeout = 10)
                say_message(m['channel_id'], "$daily")
                daily_impulse.wait(timeout = 10)

                for i in range(0, ROLL_NUM):
                    say_message(m['channel_id'], "$wa", t = 1)
                    roll_response.wait(timeout = 10)
                
                final_impulse.wait()
                say_message(m['channel_id'], f"finished")
                print("main thread done")
                start_impulse.clear()


            if (m['author']['id'] == MUDAE_ID):
                # now we know it will be a mudae message
                if (len(m['embeds']) > 0):
                    #pr
                    #roll

                    e = m['embeds'][0]
                    desc = e['description']
                    # if not type(an) == discord.embeds._EmptyEmbed:
                    if "Harem size:" in desc:
                        if (('author' in e) and ('name' in e['author'])):
                            if e['author']['name'] == username:
                                start_impulse.set()
                                give_money(desc, m)
                    else:
                        if (('author' in e) and ('name' in e['author'])):
                            # an = e['author']['name']
                            # if not (("Like Rank" in desc or "Claim Rank" in desc) or ("Custom" in desc) or ("Harem size:" in desc) or ("Kakera" in desc) or ("TOP 1000" in an) or ("kakera" in an) or ("Kakera" in an) or ("harem" in an) or ("disablelist" in an) or ("Total value:" in desc)): #really shit way to make sure it was a roll
                            if "**" in desc:
                                s = re.search("(?P<word>\*\*\d+\*\*)", desc)
                                if not s is None:
                                    found_roll(e,m,s)
                                    
                else:
                    if start_impulse.is_set():
                        for mud_key, imp_key in mudae_message_text_values_mapping.items():
                            if mud_key in m['content']:
                                # print(mud_key)
                                imp_key.set()
                                imp_key.clear()
                                    


bot.gateway.run(auto_reconnect=True)
