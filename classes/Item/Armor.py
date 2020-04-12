from .Item import Item

class Armor(Item):
	def __init__(self, itemId, name, description, defense):
		super().__init__(itemId, name, description);
		self.defense = defense;

# class Armor(Item):
# 	def __init__(self, itemId, name, description, itemType, stats, equipmentLocation, level, armorType):
# 		super().__init__(itemId, name, description, itemType)
# 		self.stats = stats
# 		self.equipmentLocation = equipmentLocation
# 		self.level = level
# 		self.armorType = armorType