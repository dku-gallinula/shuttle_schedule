##############################
#  Version 0.9               #
#  Only DKU <-> TA Provided  #
##############################

from datetime import datetime
import json
import sys

f = open("shuttle_schedule.json")
schedule = json.load(f)
now = datetime.now()
weekday_define = schedule['weekday_define']
weekend_define = schedule['weekend_define']

if len(sys.argv) > 1:
    if sys.argv[1].lower() in ["dku", "d"]:
        location = "DKU"
    elif sys.argv[1].lower() in ["ta", "t"]:
        location = "TA"
    else:
        location = "DKU"
else:
    location = "DKU"

# location = "DKU"
# now = datetime(2021, 12, 21, 20, 30, 00)

# Weekday Schedule
if now.weekday()+1 in weekday_define:
# if test_var in weekday_define:
    if location == "TA":
        plan = "weekday_A"
    elif location == "DKU":
        plan = "weekday_B"
    else:
        pass

# Weekend Schedule
elif now.weekday()+1 in weekend_define:
    if location == "TA":
        plan = "weekend_A"
    elif location == "DKU":
        plan = "weekend_B"
    else:
        pass
else:
    pass

future_shuttles = [i[0] for i in schedule[plan] if datetime.strptime(i[0], "%H:%M").time() > now.time()]
future_shuttles_2 = future_shuttles[:5]
if len(future_shuttles_2) > 1:
    result = location + ";" + ";".join(future_shuttles_2)
    # result = location + ";" + future_shuttles_2[0] + ";" + future_shuttles_2[1]
elif len(future_shuttles_2) > 0:
    result = location + ";" + future_shuttles_2[0]
else:
    result = "None"
print(result)