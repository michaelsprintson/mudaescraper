
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
ROLL_NUM = 21
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
self_id = None
claim_or_not = 1

def say_y_response(cid, thing):
    bot.sendMessage(cid,thing)
    time.sleep(2)
    bot.sendMessage(cid,"y")
    time.sleep(2)

def say_confirm_response(cid, thing):
    bot.sendMessage(cid,thing)
    time.sleep(2)
    bot.sendMessage(cid,"confirm")
    time.sleep(2)

class roll_instance():
    def __init__(self):
        self.cur_rolls = []
        self.rollcount = 0
        self.rollmax = ROLL_NUM


@bot.gateway.command
def helloworld(resp):
    global scrape_channel, roll_i, bot_num,username, claim_or_not, self_id
    
    if resp.event.ready_supplemental: #ready_supplemental is sent after ready
        user = bot.gateway.session.user
        self_id = user['id']
        username = user['username']
        print("Logged in as {}#{}".format(user['username'], user['discriminator']))
        # say_confirm_response("980201775950868532",f"$kakerareset {self_id}")
        # if username != "kjh":
        #     say_y_response("980201775950868532",f"$givek 978105521754218547 120000")
        # m = bot.getMessage("980201775950868532", "983439739002695750")    
        # print(m.json()[0])
        # buttoner = Buttoner(m.json()[0]["components"])
        # buts = [j for i in [buttoner.findButton(label=None, customID=None, row=None, column=None, emojiName=f"kakera{l}", emojiID=None, findFirst=True) for l in ["","L","P","G","O", "T", ]] for j in i]
        # print(buts)
    
    if resp.event.message:
        m = resp.parsed.auto()

        # print(m['author']['id'])
        if (m['content'][:14] == f"$specbotecho {bot_num}") and m['author']['id'] == "138336085703917568":
            sleep(2)
            if int(bot_num) == 7:
                bot.sendMessage("970798258869911562",m['content'][15:])
            else:
                bot.sendMessage(m['channel_id'],m['content'][15:])
        
        roll_channel_id = m['channel_id']
        
        if roll_channel_id == '980201775950868532':
            # print('made to roll channe')
            m = resp.parsed.auto()

            if m['content'][:11] == "$allbotecho":
                sleep(int(bot_num) * 2)
                bot.sendMessage(m['channel_id'],m['content'][12:])

            

            if m['content'][:10] == "$autobet {}".format(bot_num):
                roll_i = roll_instance()
                claim_or_not = int(m['content'][11:])
                # bot.reply(m['channel_id'], m['id'], "ðŸ‘»")
                
                # bot.addReaction(m['channel_id'], m['id'], "sad_pirate:980994471544115231")
                sleep(4)
                say_y_response(m['channel_id'],f"$bronze 4")
                say_y_response(m['channel_id'],f"$gold 4")
                say_y_response(m['channel_id'],f"$ruby 4")
                say_y_response(m['channel_id'],f"$sapphire 4")
                say_y_response(m['channel_id'],f"$emerald 4")

                sleep(2)
                bot.sendMessage(m['channel_id'],f"$dk")
                sleep(3)
                bot.sendMessage(m['channel_id'],f"$daily")
                sleep(3)

                for i in range(0,ROLL_NUM):
                    sleep(1)
                    bot.sendMessage(m['channel_id'],f"$wa")
                sleep(30)
                say_confirm_response(m['channel_id'],f"$kakerareset {self_id}")
                if username != "kjh":
                    say_y_response(m['channel_id'],f"$givek 978105521754218547 130000")
                
            
            if (len(m['embeds']) > 0) and (m['author']['id'] == "432610292342587392"): #and (messagan == "Mudae"): #make sure this is only from mudae
            #someone was rolled
                e = m['embeds'][0]
                desc = e['description']
                # if not type(an) == discord.embeds._EmptyEmbed:
                if "Harem size:" in desc:
                    if (('author' in e) and ('name' in e['author'])):
                        if e['author']['name'] == username:
                            s = re.findall("(?P<word>\*\*\d+\*\*)", desc)
                            if not len(s) == 0:
                                kval = int(s[-1].strip("**")) #change for wishes and owneds
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
                                    # print(f'ignoring {kname} because roll_i is None')
                                    pass
                                else:
                                    roll_i.rollcount+=1
                                    if (len(m['components'])) == 0:
                                        roll_i.cur_rolls.append([m['id'], kval, kname])
                                        print(f"rolled value {kval} in message id {m['id']}")
                                    else:
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
                                                sleep(2)
                                        print(f"rolled value {kval} in message id {m['id']}, ignored because pre-owned or wish")
                                    if roll_i.rollcount == roll_i.rollmax:
                                        highest_val_message = sorted(roll_i.cur_rolls, key=lambda x: -x[1])[0]
                                        print('highest val', highest_val_message[1], 'message id', highest_val_message[0])
                                        roll_i = None
                                        if claim_or_not == 1:
                                            bot.addReaction(m['channel_id'], highest_val_message[0], "sad_pirate:980994471544115231")
                                            time.sleep(2)
                                            say_y_response(m['channel_id'],f"$divorce {highest_val_message[2]}")
                                            # say_y_response(m['channel_id'],f"$givek 978105521754218547 {highest_val_message[1] * 2}")


bot.gateway.run(auto_reconnect=True)
