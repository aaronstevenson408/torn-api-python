from main_api import TornAPI
from sections import Sections, User

api = TornAPI()
sections = Sections(api)
api_user = User(api,'')
api_user_ammo = User.Ammo(api,"")
sections_user = sections.user('')

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

# Fetch user's bars
user = sections.user()  # Replace with the actual user ID or None



bars = user.bars.fetch_bars()
print(bars.energy.current)

api.close()