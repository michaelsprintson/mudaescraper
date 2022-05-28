
# Import the os module.
from time import sleep
import re
import json
from discum.utils.button import Buttoner
from functools import reduce
import pickle
from dotenv import load_dotenv
import os
load_dotenv()
# Grab the API token from the .env file.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
# demon's sword master of excalibur school.

# bi = pickle.load(open("data/bundle_info.p", 'rb'))
# scrapelist = bi[list(bi.keys())[0]]['series'][322:]
wa = pickle.load(open("data/wa_series_info.p", 'rb'))
scrapelist = list(wa.keys())
# scrapelist = list(json.load(open("failed.json",'r')))
# scrapelist = ['Free!', 'Sweet Punishment', 'Hiveswap Friendsim', 'NBA', ]

srape_location = "big_scrape.json"

from collections import defaultdict
import discum     
bot = discum.Client(token=DISCORD_TOKEN, log=False)

def get_chars(charlist):
    chars_in_ser = defaultdict(lambda: {})
    for li in charlist.split("\n"):
        splitstring = "· *"
        char_name = li.split(splitstring)[0]
        if "," in li.split(splitstring)[1]:
            count = li.split(splitstring)[1].count(",")
            terms = [f"(?P<term{i}>\$[w|m|h][a|x|g]), " for i in range(0, count)]
            intert = reduce(lambda a,b: a+b, terms)
            ss = f"\({intert}(?P<term{count}>\$[w|m|h][a|x|g])\)\* \*\*(?P<val>\d+)\*\*"
            test = re.search(ss, li.split(splitstring)[1])
            chars_in_ser[char_name]['term'] = [test.group(f"term{i}").strip("$") for i in range(0,count+1)]
        else:
            test = re.search("\((?P<term>\$[w|m|h][a|x|g])\)\* \*\*(?P<val>\d+)\*\*", li.split(splitstring)[1])
            chars_in_ser[char_name]['term'] = test.group("term").strip("$")
        chars_in_ser[char_name]['val'] = int(test.group("val"))
        
    return chars_in_ser    

@bot.gateway.command
def helloworld(resp):
    if resp.event.ready_supplemental: #ready_supplemental is sent after ready
        user = bot.gateway.session.user
        print("Logged in as {}#{}".format(user['username'], user['discriminator']))
    
    if resp.event.message:
        m = resp.parsed.auto()
        if (m['author']['id'] == "432610292342587392") and (len(m['embeds'])>0):
            seriesinfo = defaultdict(lambda: {})
            desc = m['embeds'][0]['description']
            is_there_a_title_in_desc = not "$wa" in desc.split("\n\n")[0]
            # ser_name = desc.split("\n\n")[0].strip(" ").strip("*")
            ser_name = m['embeds'][0]['author']['name'].split("  ")[0]
            print(ser_name)
            title_offset = 1 if is_there_a_title_in_desc else 0
            list_imak = desc.split("\n\n")[title_offset:]
            list_char_sels = re.findall("(\d+ \$[w|h|m][a|x|g])+", list_imak[0])
            dict_char_sels = {(j:=i.split(" "))[1].strip("$"):int(j[0]) for i in list_char_sels}
            seriesinfo[ser_name]['rolls'] = dict_char_sels
            seriesinfo[ser_name]['total_val'] = int(re.search("(?P<word>\*\*\d+\*\*)", list_imak[1]).group().strip("**"))

            if 'footer' in m['embeds'][0]:
                lod = [get_chars(list_imak[2])]
                for i in range(0, int(m['embeds'][0]['footer']['text'].split("/")[1])-1):
                    message = bot.getMessage(m['channel_id'], m['id'])
                    data = message.json()[0]
                    buts = Buttoner(data["components"])
                    # sleep(1)
                    bot.click(
                        data["author"]["id"],
                        channelID=data["channel_id"],
                        guildID=m['guild_id'],
                        messageID=data["id"],
                        messageFlags=data["flags"],
                        data=buts.getButton(emojiName='wright'),
                    )
                    sleep(2)
                    message = bot.getMessage(m['channel_id'], m['id'])
                    desc = message.json()[0]['embeds'][0]['description']
                    lod.append(get_chars(desc))
                seriesinfo[ser_name]['chars'] = reduce(lambda a,b: {**a, **b}, lod)
            else:
                # print("get chars called here on ", list_imak[2])
                seriesinfo[ser_name]['chars'] = get_chars(list_imak[2])
            # print(chars_in_ser)
            json.dump(seriesinfo, open(srape_location, 'a'))
        # 
        if m['content'] == "$startscrape":
            for ser in scrapelist:
                sleep(3)
                bot.sendMessage(m['channel_id'],f"$imakt {ser}")

            

bot.gateway.run(auto_reconnect=True)
