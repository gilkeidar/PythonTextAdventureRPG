from .Item import Item

class Weapon(Item):
	def __init__(self, itemId, name, description, attack):
		super().__init__(itemId, name, description)
		self.attack = attack;

# class Weapon(Item):
# 	def __init__(self, itemId, name, description, itemType, stats, equipmentLocation, level, weaponType):
# 		super().__init__(itemId, name, description, itemType)
# 		self.stats = stats # stats array
# 		self.equipmentLocation = equipmentLocation
# 		self.level = level
# 		self.weaponType = weaponType
