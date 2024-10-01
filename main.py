from main_api import TornAPI
from sections import Sections

api = TornAPI()
sections = Sections(api)

# Get user's ammo
user_ammo = sections.user.ammo()

for ammo in user_ammo:
    print(f"Ammo: {ammo['type']} (ID: {ammo['ammo_id']})")
    print(f"  Quantity: {ammo['quantity']}")
    print(f"  Equipped: {'Yes' if ammo['equipped'] else 'No'}")
    print("---")

api.close()