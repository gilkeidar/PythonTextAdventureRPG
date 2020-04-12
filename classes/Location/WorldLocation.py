# Pretty much everywhere when the player
# goes exploring.
from .Location import Location

class WorldLocation(Location):
	def __init__(self, locationId, name, description, locationType, monstersArray, itemsArray):
		super().__init__(locationId, name, description, locationType)
		self.monstersArray = monstersArray
		self.itemsArray = itemsArray