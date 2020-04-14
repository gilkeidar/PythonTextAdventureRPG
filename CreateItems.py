from classes.Item.Armor import Armor
from classes.Item.Consumable import Consumable
from classes.Item.Potion import Potion
from classes.Item.Weapon import Weapon

# All Items:
# itemId, name, description, itemType
# Armor:
# stats, equipmentLocation, level, armorType
# Consumable:
# use, statEffect
# Weapon:
# stats, equipmentLocation, level, weaponType
def createItems():
	items = []
	# items.append(Weapon(0, "The Varen Sword", "A sword forged from a branch of The Varen Tree. Though it can lay waste to many terrifying foes, its real power doesn't rely on its blade...", "Weapon", [], "Hand", 50, "1H"))
	items.append(Weapon(0, "The Varen Sword", "A sword forged from a branch of The Varen Tree. Though it can lay waste to many terrifying foes, its real power doesn't rely on its blade...", 100));
	items.append(Potion(1, "Healing Potion", "A bottle which contains a potion that, when drank, heals the user.", "Healing", 10))
	# items.append(Armor(2, "Silver-White Light Armor", "A fine set of armor worn long ago and crafted, some say, by the hammer of Welf Crozzo.", "Armor", [], "Body", 50, "Light Armor"))
	items.append(Armor(2, "Silver-White Light Armor", "A fine set of armor worn long ago an crafted, some say, by the hammer of Welf Crozzo.", 30))

	items.append(Potion(3, "Pure Healing Potion", "A bottle that contains a purified healing potion, making it more potent.", "Healing", 20))

	items.append(Weapon(4, "Short Sword", "A short sword.", 10))

	return items