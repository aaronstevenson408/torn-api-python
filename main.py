from main_api import TornAPI
from sections import Sections, User

api = TornAPI()
sections = Sections(api)
api_user = User(api,'')
api_user_ammo = User.Ammo(api,"")
user = sections.user('')
# public_user= sections.user('123456')
# print(f"equpped_ammo: {api_user_ammo.ammo_data[0].size} Qty:{api_user_ammo.ammo_data[0].quantity}")
# print(f"equpped_ammo: {sections_user.ammo.ammo_data[0].size} Qty:{sections_user.ammo.ammo_data[0].quantity}")

# for ammo in User.Ammo(api,"").ammo_data:
#     print(f"ammo size: {ammo.size}, qty:{ammo.quantity}")
    
# print(sections_user.basic.basic_data.status)

# Fetch user's full attacks with optional query parameters
# user = sections.user()  # Replace with the actual user ID or None
# print(user.basic.basic_data)
# attacksfull = user.attacksfull.fetch_attacksfull(limit=50) #only works with user 
# print(attacksfull)

# # Fetch user's bars
# user = sections.user()  # Replace with the actual user ID or None
# bars = user.bars.fetch_bars()
# print(bars.energy.current)

# # Fetch user's battle stats
# user = sections.user()  # Replace with the actual user ID or None
# battle_stats = user.battlestats.fetch_battle_stats()
# print(battle_stats)

# bazaar_items = user.bazaar.fetch_bazaar()
# print(bazaar_items)

# cooldowns = user.cooldowns.cooldowns_data
# print(cooldowns)

# #this is implementations for 2 different criminal record selections , one through crim
# criminal_record = user.crimes.criminal_record # this has a minimal access level
# print(criminal_record)
# user2 = sections.user(123456)
# criminal_record2 = user2.criminal_record.record_data #this is public
# print(criminal_record2)

# discord_info = user.discord.fetch_discord()
# print(discord_info)

# display_items = user.display_items.fetch_display()
# print(display_items)

# education_info = user.education.fetch_education()
# print(f"current education : {education_info.education_current} Time left:{education_info.education_timeleft}")

# equipped_items = user.equipment.fetch_equipment()
# print(equipped_items)

# events_list = user.events.fetch_events(limit=25)  # Adjust limit as needed
# print(events_list)

# active_gym = user.gym.fetch_active_gym()
# print(f"Active Gym ID: {active_gym}")

# hof_rankings = user.hof.fetch_rankings()
# print("Hall of Fame Rankings:")
# for category, ranking in hof_rankings.items():
#     print(f"{category}: {ranking}")


# honors_info = public_user.honors.fetch_honors()
# print("Honors Awarded:", honors_info.get("awarded", []))
# print("Honors Time:", honors_info.get("times", []))

# icons_info = user.icons.fetch_icons()
# print("Currently Shown Icons:", icons_info)

# jobpoints_info = user.jobpoints.fetch_jobpoints()
# print("Currently Owned Job Points:", jobpoints_info)

logs_info = user.log.fetch_logs()  # Example timestamps
print("Activity Logs:", logs_info)








api.close()