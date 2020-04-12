# The terrifying depths of the dungeon... are also
# where heroes are made.
from .Location import Location

class Dungeon(Location):
	def __init__(self, locationId, name, description, locationType, monstersArray, itemsArray):
		super().__init__(locationId, name, description, locationType)
		self.monstersArray = monstersArray
		self.itemsArray = itemsArray
		