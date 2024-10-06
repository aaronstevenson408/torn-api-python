from tornApi import TornAPI
from sections import Sections
from typing import Dict, Any, Optional
from tornApi import TornAPI
from env_loader import load_environment_variables
from logger import setup_logger, close_logger

env = load_environment_variables()
if env is None:
    raise ValueError("Failed to load environment variables.")
logger, file_handler = setup_logger('Example', env['DEBUG_LEVEL'])
logger.info("env loaded : %s", env)
api = TornAPI(access_level='full')
sections = Sections(api)
user = sections.user('')
# user_properties_id = user.properties.fetch_data().properties[0].id
market = sections.market(item_id=1)  # or just sections.market() if no item_id is needed
torn = sections.torn(id="")
user_properties = user.properties.fetch_data()
# print(user_properties.properties[0].property_data)
property = sections.property(user_properties.properties[0].id)
public_user= sections.user('123456')
### User Section ###
# [print(ammo) for ammo in user.ammo.fetch_data()] 
# print(user.basic.fetch_data())
# print(user.attacks.fetch_data())
# print(user.attacks_full.fetch_data())
# print(user.bars.fetch_data())
# print(user.battle_stats.fetch_data())
# print(user.bazaar.fetch_data())
# print(user.cooldowns.fetch_data())
# print(user.crimes.fetch_data())
# print(user.criminal_record.fetch_data())
# print(user.discord.fetch_data())
# print(user.display_items.fetch_data())
# print(user.education.fetch_data())
# print(user.equipment.fetch_data()[0].uid)
# print(user.events.fetch_data())
# print(user.gym.fetch_data())
# print(user.hof.fetch_data())
# print(user.honors.fetch_data())
# print(user.icons.fetch_data())
# print(user.jobpoints.fetch_data())
# print(user.log.fetch_data())
# print(user.lookup.fetch_data())
# print(user.medals.fetch_data())
# print(user.merits.fetch_data())
# print(user.messages.fetch_data())
# print(user.missions.fetch_data())
# print(user.money.fetch_data())
# print(user.networth.fetch_data())
# print(user.newevents.fetch_data())
# print(user.newmessages.fetch_data())
# print(user.notifications.fetch_data())
# print(user.perks.fetch_data())
# print(user.personalstats.fetch_data())
# print(user.profile.fetch_data())
# print(user.properties.fetch_data())
# print(user.public_status.fetch_data())
# print(user.refills.fetch_data())
# print(user.reports.fetch_data())
# print(user.reports.fetch_data())
# print(user.revives.fetch_data())
# print(user.revives_full.fetch_data())
# print(user.skills.fetch_data())
# print(user.stocks.fetch_data())
# print(user.timestamp.fetch_data())
# print(user.travel.fetch_data())
# print(user.weapon_exp.fetch_data())
# print(user.work_stats.fetch_data())

# #### Property Section ###
# print(sections.property(user_properties.properties[0].id).timestamp.fetch_data().timestamp)
# print(sections.property(user_properties.properties[0].id).lookup.fetch_data())
# print(sections.property(user_properties.properties[0].id).property.fetch_data())

# #### Market Section ###
# print("Bazaar Data:", market.bazaar.fetch_data())
# print("Item Market Data:", market.itemmarket.fetch_data())
# print("Lookup Data:", market.lookup.fetch_data())
# print("Points Market Data:", market.pointsmarket.fetch_data())
# print("Timestamp:", market.timestamp.fetch_data())

# #### Torn Section ###
# print(torn.bank.fetch_data())
# print(torn.cards.fetch_data())
# print(torn.chainreport.fetch_data())
# print(torn.cityshops.fetch_data())
# print(torn.companies.fetch_data())
# print(torn.competition.fetch_data())
# print(torn.education.fetch_data())
# print(torn.factiontree.fetch_data())
# print(torn.gyms.fetch_data())
# print(torn.honors.fetch_data())
# print(torn.itemdetails.fetch_data(user.equipment.fetch_data()[0].uid))
print(torn.items.fetch_data())
print(torn.itemstats.fetch_data(user.equipment.fetch_data()[0].uid))


api.close() 