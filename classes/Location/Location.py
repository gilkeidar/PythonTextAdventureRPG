# e.g. a node
class Location:
	def __init__(self, locationId, name, description, locationType):
		self.locationId = locationId
		self.name = name
		self.description = description
		self.locationType = locationType
		self.surroundingLocations = []
		self.explored = False
