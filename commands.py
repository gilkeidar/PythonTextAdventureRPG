# from main import updateCurrentLocation

# # Movement function - for when the player moves!
# def movement(direction, directions, currentLocation, oldLocation, locationArray):
# 	# global directions
# 	# global currentLocation
# 	# global oldLocation
	
# 	shortcutDirections = ["n", "s", "e", "w", "nw", "ne", "sw", "se"]
# 	 # parse directions if not in the same form as in neighborLocation array
# 	if (direction in shortcutDirections):
# 	    direction = directions[shortcutDirections.index(direction)]

# 	for neighborLocation in currentLocation.surroundingLocations:
# 		if (neighborLocation[1] == direction):
# 			locationId = neighborLocation[0]
# 			location = locationArray[locationId]
# 			print("You make your way " + direction + " to " + location.name + "...")
# 			updateCurrentLocation(location)
#     # if didn't change rooms (user tried to go in a way they can't)
# 	if (currentLocation == oldLocation):
# 		print("You cannot go that way.")

# # Print the player's inventory and stats
# def printInventory(player):
# 	# global player

# 	print(player.name + " | Level: " + str(player.level))
# 	print("ATK: " + str(player.attack) + " | DEF: " + str(player.defense))
# 	print()

# 	if len(player.inventory) > 0:
# 		print("You unsling your bag to find the following:");
# 		for item in player.inventory:
# 			print(item.name)
# 	else:
# 		print("You're not carrying anything.")

# # Player picks up an item
# def take(itemName, currentLocation, player):
# 	# global currentLocation
# 	# global player
# 	# Find item in currentLocation.itemsArray
# 	takenItem = None

# 	if len(currentLocation.itemsArray) > 0: # If there are items
# 		for item in currentLocation.itemsArray:
# 			if(itemName == item.name.lower()):
# 				takenItem = item
# 				break
# 		if takenItem is not None: # If item exists
# 			print("You pick up " + takenItem.name)
# 			# Remove item from current location
# 			currentLocation.itemsArray.remove(takenItem)
# 			# Place item in player's inventory
# 			player.inventory.append(takenItem)

# 		else:
# 			print("There is no such item here.")


# 	else:
# 		print("There are no items here.")

