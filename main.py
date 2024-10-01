from main_api import TornAPI
from sections import Sections, User

api = TornAPI()
sections = Sections(api)
api_user = User(api,'')
api_user_ammo = User.Ammo(api,"")


print(f"equpped_ammo: {api_user_ammo.ammo_data[0].equipped} Qty:{api_user_ammo.ammo_data[0].quantity}")

for ammo in User.Ammo(api,"").ammo_data:
    print(f"ammo size: {ammo.size}, qty:{ammo.quantity}")