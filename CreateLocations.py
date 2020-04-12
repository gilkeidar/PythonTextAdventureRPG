from classes.Location.WorldLocation import WorldLocation
from classes.Location.Path import Path


def createLocations(itemArray):
	locations = []
	locations.append(WorldLocation(0, "Evelore Woods", "You are in a forest path; the forest path that beckons beginnings.", "World", [], []))
	locations.append(WorldLocation(1, "The Varen Tree", "The Tree of Life, or so they say. A giant tree rises from the ground, a warm brown trunk with infinite branches and green leaves that shine golden in the sun.", "World", [], [itemArray[0], itemArray[1], itemArray[2], itemArray[3], itemArray[4]]))
	locations.append(WorldLocation(2, "Green Field", "A green field, under a cool blue sky; where a hero starts their journey.", "World", [], [itemArray[1]]))

	# locations = [EveloreWoods, TheVarenTree, GreenField]
	return locations

def getNeighbors(locationId, pathArray):
	locations = []
	for path in pathArray:
		if(path.source == locationId):
			locations.append([path.target, path.directionST])
		elif(path.target == locationId):
			locations.append([path.source, path.directionTS])
	return locations

def createPaths():
	paths = []
	paths.append(Path(0, 1, "Walking", "north", "south"))
	paths.append(Path(0, 2, "Walking", "east", "west"))
	paths.append(Path(1, 2, "Walking", "southeast", "northwest"))
	
	# paths = [EWtoVT, EWtoGF]
	return paths
