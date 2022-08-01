tier_toggle = {"bronze":True,
              "silver":False,
              "gold":True,
              "sapphire":True,
              "ruby":True,
              "emerald":True}

gold_keep_toggle = True

tier_costs = {"bronze":10_000,
              "silver":20_000,
              "gold":30_000,
              "sapphire":30_000,
              "ruby":30_000,
              "emerald":30_000}

gold_to_return = sum([tcv for tcn,tcv in tier_costs.items() if tier_toggle[tcn]]) - (tier_costs['gold'] if gold_keep_toggle else 0)

roll_num = (4 if tier_toggle['sapphire'] else 0) + (2 if tier_toggle['ruby'] else 0)