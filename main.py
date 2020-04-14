### Adventure Game of Ultimate Power
###
### Because honestly, I've waited too long to work
### on it.
###
### As with the previous one:
###Credit to Aidan Mott's Adventure Game, as since I'm a beginner
###I used some of the starting idea as inspiration (i.e. using colored text :P)

### Since Locations are connected to one another
### by paths, if you go in a for loop and change
### each path's source and target ids,
### you can mess up the map completely.
### This can be a really cool game mechanic e.g. "The Evil Wizard cast his spell, 'Rearrangum' (or something), and the whole world fell to disarray. Places that used to be next to each other suddenly were miles apart. Now, the player has to explore what is essentially an entire new map! Cool, eh?

import random
# import time
# from termcolor import colored
# from colored import fg, bg, attr

from classes.Character.Character import Character
from classes.Character.Player import Player
from CreateLocations import createLocations, createPaths, getNeighbors
from CreateItems import createItems
from CreateMonsters import createMonsters
from utility import textRoomFormatter, unrecognizedCommand, traversalText

# print(colored("Test!", "yellow", attrs = ["bold"]))

# First things first...
#
# Classes:
# Character -> Player, Non-Player (non-lethal), Monster
# Item -> Weapon, Armor, Consumable
# Location -> World, (everywhere that isnt the following:)
#			  Town, Dungeon, Boss Room



#### Variables of Ultimate Power! ####

# item array
itemArray = []

# monster array
monsterArray = []

# arrays of locations and paths (last since they include items & characters)
locationArray = []
pathArray = []

# Current Location
currentLocation = None
oldLocation = []
player = None

# Directions Array
directions = [
    "north", "south", "east", "west", "northwest", "northeast", "southwest",
    "southeast", "n", "s", "e", "w", "nw", "ne", "sw", "se"
]

# Booleans
printLocationDetails = False  # Used for "look" command to show location info even if currentLocation isn't new

# Current game state
states = ["Travel", "Combat"]
state = states[0] # Starts with Travel as the main state

# Combat turn (only relevant in combat)
currentTurn = 0
whoseTurn = None # Player or monster

#### Variables of Ultimate Power! ####



#### Methods of Ultimate Power!   ####

# Initialize game variables
def initializeGame():
	global itemArray
	global monsterArray
	global locationArray
	global pathArray
	global currentLocation
	global player

	# instantiating items
	itemArray = createItems()

	# instantiating monsters
	monsterArray = createMonsters()

	# instantiating locations and paths
	locationArray = createLocations(itemArray, monsterArray)
	pathArray = createPaths()

	# Initialize all locations' surroundingLocations arrays
	for location in locationArray:
		location.surroundingLocations = getNeighbors(location.locationId, pathArray)
	
	currentLocation = locationArray[0]
	player = Player("Player", 250, 1)

# Update player
def updatePlayer():
    global player

    # Update player's attack
    if player.equipment["weapon"] is not None:
        player.attack = player.equipment["weapon"].attack
    else:
        player.attack = 1

    # Update player's defense
    if player.equipment["armor"] is not None:
        player.defense = player.equipment["armor"].defense
    else:
        player.defense = 1

# To be used if the command functions were in a separate file to update the 
# global variables here
def updateCurrentLocation(newLocation):
    global currentLocation

    currentLocation = newLocation


# Get name of item in input:
def getItemName(inputArray, startingIndex):
	# Get name of item in input
	itemString = inputArray[startingIndex]
	for i in range(startingIndex + 1, len(inputArray)):
		itemString += " " + inputArray[i]
	
	return itemString

# Get item by its name
def getItem(itemName, searchLocation = True, searchInventory = True, searchEquipment = True):

	global currentLocation
	global player

	# If a searched item's name contains the itemName parameter, add it as a possible match
	matchingItems = []
	exactItem = None
	foundExactItemCounter = 0
	source = ""
	# If matchingItems length is 1, then there's only one item (just return first index)
	# Otherwise, ask the player which item they meant

	if searchLocation:
		for item in currentLocation.itemsArray:
			if itemName == item.name.lower():
				exactItem = item
				foundExactItemCounter += 1
				# return exactItem
				source = "location"
			elif itemName in item.name.lower():
				matchingItems.append(item)
				source = "location"
			
	if searchInventory and exactItem is None:
		for item in player.inventory:
			if itemName == item.name.lower():
				exactItem = item
				foundExactItemCounter += 1
				# return exactItem
				source = "inventory"
			if itemName in item.name.lower():
				matchingItems.append(item)
				source = "inventory"
	if searchEquipment:
		if player.equipment["armor"] is not None and itemName in player.equipment["armor"].name.lower():
			if itemName == player.equipment["armor"].name.lower():
				exactItem = player.equipment["armor"]
				foundExactItemCounter += 1
				# return exactItem
				source = "armor"
			else:
				matchingItems.append(player.equipment["armor"])
				source = "weapon"
		if player.equipment["weapon"] is not None and itemName in player.equipment["weapon"].name.lower():
			if itemName == player.equipment["weapon"].name.lower():
				exactItem = player.equipment["weapon"]
				foundExactItemCounter += 1
				# return exactItem
				source = "weapon"
			else:
				matchingItems.append(player.equipment["weapon"])
				source = "weapon"
	
	# print("DEBUG foundExactItemCounter:" + str(foundExactItemCounter))
	# print("DEBUG Matching Items length:" + str(len(matchingItems)))	


	if exactItem is not None and foundExactItemCounter == 1:
		return {"item": exactItem, "source": source}
	elif exactItem is None:
		if len(matchingItems) == 1:
			return {"item": matchingItems[0], "source": source}
		elif len(matchingItems) == 0:
			return {"item": None, "source": None}
		else:
			print("I'm not sure which item you meant.")
			# Returns "printed" to avoid printing other dialogue in other functions
			return {"item" : "printed", "source": None}
	elif exactItem is not None and foundExactItemCounter > 1:
		print("I'm not sure which item you meant.")
		# Returns "printed" to avoid printing other dialogue in other functions
		return {"item": "printed", "source": None}


def getItem2(itemName, searchLocation = True, searchInventory = True, searchEquipment = True, arrayImportance = True):
	global currentLocation
	global player

	# For each item, store dictionary {"item": item, "source": source}
	matchingItems = []
	exactItem = [] 

	# Search each location, and prioritize exact matches over partial matches
	if searchLocation:
		for item in currentLocation.itemsArray:
			if itemName == item.name.lower():
				# Found an exact match
				exactItem.append({"item" : item, "source" : "location"})
			elif itemName in item.name.lower():
				# Found a partial match
				matchingItems.append({"item": item, "source": "location"})
	if searchInventory:
		for item in player.inventory:
			if itemName == item.name.lower():
				# Found an exact match
				exactItem.append({"item" : item, "source" : "inventory"})
			elif itemName in item.name.lower():
				# Found a partial match
				matchingItems.append({"item": item, "source": "inventory"})
	if searchEquipment:
		if player.equipment["armor"] is not None:
			if itemName == player.equipment["armor"].name.lower():
				# Found an exact match
				exactItem.append({"item": player.equipment["armor"], "source" : "armor"})
			elif itemName in player.equipment["armor"].name.lower():
				# Found a partial match
				matchingItems.append({"item": player.equipment["armor"], "source": "armor"})
		if player.equipment["weapon"] is not None:
			if itemName == player.equipment["weapon"].name.lower():
				# Found an exact match
				exactItem.append({"item": player.equipment["weapon"], "source" : "weapon"})
			elif itemName in player.equipment["weapon"].name.lower():
				# Found a partial match
				matchingItems.append({"item": player.equipment["weapon"], "source": "weapon"})
	
	# Review results:
	# Possibilities:
	# 0 in E and 0 in M -> Item not found
	# 1 in E and 0 in M -> Found one exact match, return it
	# 0 in E and 1 in M -> found one partial match, return it
	# 1 in E and 1 in M -> found one in both, prioritize exact, return exact match
	# 0 in E and 2 in M -> found 2 in matching, unknown which is which --> if in different arrays, ask player which object he/she meant
	# 2 in E and 0 in M -> found 2 in exact, unknown which is which --> if in different arrays, ask player which object he/she meant



	print("matchingItems Length: " + str(len(matchingItems)))
	print("exactItem Length: " + str(len(exactItem)))

	if len(matchingItems) == 0 and len(exactItem) == 0:
		# No item found; return None
		return {"item": None, "source": None}
	if len(exactItem) >= 1: # Prioritize exact match over not exact matches
		if len(exactItem) == 1:
			# Only one match, return this one
			return exactItem[0]
		else:
			# Multiple matches, compare to see if they're in different arrays
			# If they're in the same array, just return one of them
			uniqueItemsAndLocations = []
			for itemDictionary in exactItem:
				if not (itemDictionary in uniqueItemsAndLocations):
					uniqueItemsAndLocations.append(itemDictionary)
			
			# Now uniqueItemsAndLocations should have only unique items that are unique in both item and source values
			# (each has a different source value)
			if len(uniqueItemsAndLocations) == 1 or arrayImportance == False:
				return uniqueItemsAndLocations[0]
			else:
				# Ask player which item he meant
				askString = "Which item did you mean, "
				for itemDictionary in uniqueItemsAndLocations:
					if itemDictionary == uniqueItemsAndLocations[-1]:
						askString += "or "
					if itemDictionary["item"].name.lower().split(" ")[0] == "the":
						askString += itemDictionary["item"].name
					else:
						askString += "the " + itemDictionary["item"].name
					if itemDictionary["source"] == "location":
						askString += " on the ground"
					elif itemDictionary["source"] == "inventory":
						askString += " in your inventory"
					elif itemDictionary["source"] == "armor":
						askString += " that you're wearing"
					elif itemDictionary["source"] == "weapon":
						askString += " that you're wielding"
					if itemDictionary == uniqueItemsAndLocations[-1]:
						askString += "?"
					else:
						askString += ", "

				# Get user input
				while True:
					print(askString)
					userInput = input("> ")
					formattedInput = userInput.lower()

					if "inventory" in formattedInput:
						# Return exact item whose source is from inventory
						for itemDictionary in uniqueItemsAndLocations:
							if itemDictionary["source"] == "inventory":
								return itemDictionary
					elif "ground" in formattedInput:
						# Return exact item whose source is from inventory
						for itemDictionary in uniqueItemsAndLocations:
							if itemDictionary["source"] == "location":
								return itemDictionary
					elif "armor" in formattedInput or "wearing" in formattedInput:
						# Return exact item whose source is from inventory
						for itemDictionary in uniqueItemsAndLocations:
							if itemDictionary["source"] == "armor":
								return itemDictionary
					elif "weapon" in formattedInput or "wielding" in formattedInput:
						# Return exact item whose source is from inventory
						for itemDictionary in uniqueItemsAndLocations:
							if itemDictionary["source"] == "weapon":
								return itemDictionary
				
				return {"item": "printed", "source": None}
				# Needs a new command with the form {the} [item name] in {source}
				# Maybe flip a global boolean switch so that the command works? (Can't use this command all
				# the time, only when prompted)
	
	if len(matchingItems) >= 1:
		if len(matchingItems) == 1:
			return matchingItems[0]
		else:
			# Unknown item
			print("I'm not sure which item you meant.")
			return {"item" : "printed", "source": None}
			# uniqueItemsAndLocations = [matchingItems[0]] # add first entry, doesn't need to be checked
			# for itemDictionary in matchingItems:
			# 	# Check if the source array of the item dictionary isn't in uniqueItemsAndLocations
			# 	for element in uniqueItemsAndLocations:
			# 		if element["source"] != itemDictionary["source"]:
			# 			uniqueItemsAndLocations.append(itemDictionary)
			# 			break
			
			# # Now that uniqueItemsAndLocations is filled, check i


		
		



def getCharacter(characterName):
	global currentLocation

	matchingCharacters = []
	exactCharacter = []

	# Will NPCs also be in the monsters array? Maybe change it so
	# It's a characters array instead
	for character in currentLocation.monstersArray:
		if characterName == character.name.lower():
			# Exact match
			exactCharacter.append(character)
			# print("Found an exact match!")
		elif characterName in character.name.lower():
			# Matching Character
			matchingCharacters.append(character)
	
	# Prioritize exact matches over non-exact matches
	if len(exactCharacter) >= 1:
		if len(exactCharacter) == 1:
			return {"character": exactCharacter[0]}
		else:
			# If there are more than one exact characters (shouldn't happen?)
			print("I'm not sure to which character you're referring.")
			return {"character": "printed"}
	elif len(matchingCharacters) >= 1:
		if len(matchingCharacters) == 1:
			return {"character" : matchingCharacters[0]}
		else:
			print("I'm not sure to which character you're referring.")
			return {"character": "printed"}
	else: # Character not found
		return {"character": None}


# Movement function - for when the player moves!
def movement(direction):
	global directions
	global currentLocation
	global oldLocation

	shortcutDirections = ["n", "s", "e", "w", "nw", "ne", "sw", "se"]
	# parse directions if not in the same form as in neighborLocation array
	if (direction in shortcutDirections):
		direction = directions[shortcutDirections.index(direction)]

	for neighborLocation in currentLocation.surroundingLocations:
		if (neighborLocation[1] == direction):
			locationId = neighborLocation[0]
			location = locationArray[locationId]
			# Print traversal text based on the path type
			pathType = neighborLocation[2]
			# print("path type: " + pathType)

			# print("You make your way " + direction + " to " + location.name +
			# 		"...")
			print(traversalText(pathType, direction, location.name))
			currentLocation = location
	# if didn't change rooms (user tried to go in a way they can't)
	if (currentLocation == oldLocation):
		print("You cannot go that way.")


# Print the player's inventory and stats
def printInventory():
    global player

    # Print player's stats
    print(player.name + " | HP: " + str(player.hp) + "/" + str(player.fullHP) +
          " | Level: " + str(player.level))
    print("ATK: " + str(player.attack) + " | DEF: " + str(player.defense))
    print()

    # Print player's equipment
    if (player.equipment["armor"] is not None):
        print("You are wearing " + player.equipment["armor"].name + ".")
    else:
        print("You are wearing plain clothes.")
    if player.equipment["weapon"] is not None:
        if player.equipment["weapon"].name.lower().split(" ")[0] == "the":
            print("You are wielding " + player.equipment["weapon"].name + ".")
        else:
            print("You are wielding a " + player.equipment["weapon"].name + ".")
    else:
        print("You wield only your undisciplined fists.")

    print()

    # Print player's items
    if len(player.inventory) > 0:
        print("You unsling your bag to find the following:")
        for item in player.inventory:
            print(item.name)
    else:
        print("You're not carrying anything.")


# Player picks up an item
def take(itemName):
	global currentLocation
	global player
	# Find item in currentLocation.itemsArray
	takenItem = None
	if len(currentLocation.itemsArray) > 0:  # If there are items
		
		# for item in currentLocation.itemsArray:
		#     if (itemName == item.name.lower()):
		#         takenItem = item
		#         break
		takenItemDictionary = getItem2(itemName, True, False, False)
		takenItem = takenItemDictionary["item"]
		
		if takenItem is not None and takenItem != "printed":  # If item exists
			if (takenItem.name.lower().split(" ")[0] == "the"):
				print("You pick up " + takenItem.name + ".")
			else:
				print("You pick up a " + takenItem.name + ".")
			# Remove item from current location
			currentLocation.itemsArray.remove(takenItem)
			# Place item in player's inventory
			player.inventory.append(takenItem)
		
		elif takenItem != "printed":
			print("There is no such item here.")

	else:
		print("There are no items here.")


# Player drops an item
def drop(itemName):
	global currentLocation
	global player

	# Get item to drop:
	droppedItemDictionary = getItem2(itemName, False, True, True)
	droppedItem = droppedItemDictionary["item"]
	source = droppedItemDictionary["source"]

	if droppedItem is not None and droppedItem != "printed": # If item exists
		# Drop item

		if droppedItem.name.lower().split(" ")[0] == "the":
			print("You drop " + droppedItem.name + ".")
		else:
			print("You drop a " + droppedItem.name + ".")
		currentLocation.itemsArray.append(droppedItem)

		# Remove item from its original location
		if source == "inventory":
			player.inventory.remove(droppedItem)
		elif source == "armor":
			player.equipment["armor"] = None
			updatePlayer()
		elif source == "weapon":
			player.weapon = None
			updatePlayer()
	elif droppedItem is None:
		print("You have no such item.")
		

	# # Find item in player's inventory or equipment
	# matchingItems = []
	# droppedItem = None
	# sourceArray = None
	# foundExactItemCounter = 0

	# for item in player.inventory:
	# 	if item.name.lower() == itemName:
	# 		droppedItem = item
	# 		foundExactItemCounter += 1
	# 	elif itemName in item.name.lower():
	# 		# droppedItem = item
	# 		matchingItems.append(item)
	# 		sourceArray = "inventory"
			
	# # If item wasn't found in player's inventory, search player's equipment
	# if droppedItem is None:
	# 	if player.armor is not None:
	# 		if player.armor.name.lower() == itemName:
	# 			droppedItem = player.armor
	# 			foundExactItemCounter += 1
	# 		elif itemName in player.armor.name.lower():
	# 			# droppedItem = player.armor
	# 			matchingItems.append(player.armor)
	# 			sourceArray = "armor"
	# 			# Remove player's armor
	# 			# player.armor = None

	# 			# Update player
	# 			# updatePlayer()
	# 	if player.weapon is not None:
	# 		if player.weapon.name.lower() == itemName:
	# 			droppedItem = player.weapon
	# 			foundExactItemCounter += 1
	# 		elif itemName in player.weapon.name.lower():
	# 			# droppedItem = player.weapon
	# 			matchingItems.append(player.weapon)

	# 			sourceArray = "weapon"
	# 			# Remove player's weapon
	# 			# player.weapon = None

	# 			# Update player
	# 			# updatePlayer()

	# # print("DEBUG foundExactItemCounter: " + str(foundExactItemCounter))
	# # print("DEBUG Matching Items length: " + str(len(matchingItems)))

	# if droppedItem is None:
	# 	if len(matchingItems) == 0:
	# 		print("You have no such item.")
	# 	elif len(matchingItems) == 1:
	# 		droppedItem = matchingItems[0]
	# 	elif len(matchingItems) > 1:
	# 		print("I'm not sure what item you meant.")

	# if droppedItem is not None and foundExactItemCounter <= 1:
	# 	# Remove item from either inventory or equipment
	# 	if sourceArray == "inventory":
	# 		player.inventory.remove(droppedItem)
	# 	elif sourceArray == "armor":
	# 		player.armor = None
	# 	elif sourceArray == "weapon":
	# 		player.weapon = None

	# 	updatePlayer()
		

	# 	# Place item in current location
	# 	currentLocation.itemsArray.append(droppedItem)
	# 	if droppedItem.name.lower().split(' ')[0] == "the":
	# 		print("You drop " + droppedItem.name + ".")
	# 	else:
	# 		print("You drop a " + droppedItem.name + ".")
	# elif foundExactItemCounter > 1:
	# 	print("I'm not sure what item you meant to drop.")



# Player equips an item
def equip(itemName):
	global currentLocation
	global player

	equippedItemDictionary = getItem2(itemName, True, True, False)
	equippedItem = equippedItemDictionary["item"]
	source = equippedItemDictionary["source"]

	if equippedItem is not None and equippedItem != "printed": # Item exists
		# Equip item
		itemType = equippedItem.__class__.__name__
		# print("Item Type: " + itemType)
		if itemType in ["Armor", "Weapon"]:
			if itemType == "Armor":
				# If player is already wearing an armor, then put the current armor in the player's inventory
				if player.equipment["armor"] is not None:
					player.inventory.append(player.equipment["armor"])
				player.equipment["armor"] = equippedItem
			elif itemType == "Weapon":
				if player.equipment["weapon"] is not None:
					player.inventory.append(player.equipment["weapon"])
				player.equipment["weapon"] = equippedItem
			
			print("You equip " + equippedItem.name + ".")
			# Update player
			updatePlayer()

			# Remove item from original array
			if source == "location":
				currentLocation.itemsArray.remove(equippedItem)
			elif source == "inventory":
				player.inventory.remove(equippedItem)

		else:
			print(equippedItem.name + " is not equippable.")


	elif equippedItem is None:
		print("You see no such item.")

	# # Find item in either player's inventory or current location
	# equippedItem = None
	# sourceArray = None
	# matchingItems = []
	# foundExactItemCounter = 0

	# for item in player.inventory:
	# 	if item.name.lower() == itemName:
	# 		equippedItem = item
	# 		sourceArray = "inventory"
	# 		# break
	# 		foundExactItemCounter += 1
	# 	elif itemName in item.name.lower():
	# 		matchingItems.append(item)
	# 		sourceArray = "inventory"

	# if equippedItem is None:  # If item wasn't found in player's inventory
	# 	for item in currentLocation.itemsArray:
	# 		if item.name.lower() == itemName:
	# 			equippedItem = item
	# 			sourceArray = "location"
	# 			# break
	# 			foundExactItemCounter += 1
	# 		elif itemName in item.name.lower():
	# 			matchingItems.append(item)
	# 			sourceArray = "location"
	# if len(matchingItems) > 1 or foundExactItemCounter > 1:
	# 	print("I'm not sure which item you meant to equip.")
	# 	return
	# elif len(matchingItems) == 1 and equippedItem is None:
	# 	equippedItem = matchingItems[0]
		
	# if equippedItem is not None and foundExactItemCounter <= 1:  # If item exists
	# 	# Check that item is a weapon or armor
	# 	# print("Item is a: " + equippedItem.__class__.__name__);
	# 	itemType = equippedItem.__class__.__name__

	# 	if itemType in ["Armor", "Weapon"]:
	# 		if itemType == "Armor":
	# 			if player.armor is not None:  # If armor slot is filled
	# 				# Put currently equipped armor in inventory
	# 				player.inventory.append(player.armor)

	# 			# Replace armor with new armor
	# 			player.armor = equippedItem
	# 		elif itemType == "Weapon":
	# 			if player.weapon is not None:  # If weapon slot is filled
	# 				# Put currently equipped weapon in inventory
	# 				player.inventory.append(player.weapon)

	# 			# Replace weapon with new weapon
	# 			player.weapon = equippedItem

	# 		# Remove item from source array
	# 		if sourceArray == "inventory":
	# 			player.inventory.remove(equippedItem)
	# 		elif sourceArray == "location":
	# 			currentLocation.itemsArray.remove(equippedItem)

	# 		print("You equip " + equippedItem.name + ".")

	# 		# Update player:
	# 		updatePlayer()

	# 	else:  # Item isn't armor or weapon; cannot be equippedItem
	# 		print(equippedItem.name + " is not equippable.")
	# else:  # If item wasn't found
	# 	print("You have no such item.")


# Player unequips an item
def unequip(itemName):
	global player

	unequippedItemDictionary = getItem2(itemName, False, False, True)
	unequippedItem = unequippedItemDictionary["item"]
	source = unequippedItemDictionary["source"]

	if unequippedItem is not None and unequippedItem != "printed":
		# Unequip item
		if source == "armor":
			player.inventory.append(player.equipment["armor"])
			player.equipment["armor"] = None
		elif source == "weapon":
			player.inventory.append(player.equipment["weapon"])
			player.equipment["weapon"] = None

		# Update player
		updatePlayer()
		print("You unequip " + unequippedItem.name + ".")
	elif unequippedItem is None:
		print("You have no such item equipped.")

	# # Check if item is currently equipped
	# if player.armor is not None:
	# 	if itemName in player.armor.name.lower():
	# 		unequippedItem = player.armor

	# 		# Remove player's armor
	# 		player.armor = None
	# if player.weapon is not None:
	# 	if itemName in player.weapon.name.lower():
	# 		unequippedItem = player.weapon

	# 		# Remove player's weapon
	# 		player.weapon = None

	# if unequippedItem is not None:
	# 	# Place item in player's inventory
	# 	player.inventory.append(unequippedItem)

	# 	print("You unequip " + unequippedItem.name + ".")

	# 	# Update player
	# 	updatePlayer()
	# else:
	# 	print("You have no such item equipped.")


# Player examines an item
def examine(itemName):
	global player
	global currentLocation

	# Find item in either current location, player's inventory, or player's equipment
	examinedItem = None

	# # Try to find item in current location:
	# for item in currentLocation.itemsArray:
	# 	if item.name.lower() == itemName:
	# 		examinedItem = item
	# 		break
	
	# # If item still wasn't found, try to search for it in the player's inventory
	# if examinedItem is None:
	# 	for item in player.inventory:
	# 		if item.name.lower() == itemName:
	# 			examinedItem = item
	# 			break

	# # If item still wasn't found, try to search for it in the player's equipment
	# if examinedItem is None:
	# 	if player.armor is not None and player.armor.name.lower() == itemName:
	# 		examinedItem = player.armor
	# 	elif player.weapon is not None and player.weapon.name.lower() == itemName:
	# 		examinedItem = player.weapon

	examinedItemDictionary = getItem2(itemName, True, True, True, False)
	examinedItem = examinedItemDictionary["item"]

	# If item was found, print its information
	if examinedItem is not None and examinedItem != "printed":

		itemType = examinedItem.__class__.__name__

		# print("class:" + examinedItem.__bases__)

		if itemType in ["Potion"]: # classes that inherit from consumable should be displayed the same way
			itemType = "Consumable"

		if examinedItem.name.lower().split(" ")[0] == "the":
			print("You examine " + examinedItem.name + ":")
		else:
			print("You examine the " + examinedItem.name + ":")
		
		print()

		print(examinedItem.description)

		print()
		
		if itemType == "Armor":
			print ("Type: Armor | DEF: " + str(examinedItem.defense))
		elif itemType == "Weapon":
			print("Type: Weapon | ATK: " + str(examinedItem.attack))
		elif itemType == "Consumable":
			consumableString = ""
			consumableString = "Type: Consumable | Use: " + examinedItem.use + " | Effect: "
			if examinedItem.statEffect > 0:
				consumableString += "+ "
			elif examinedItem.statEffect < 0:
				consumableString += "- "
			consumableString += str(examinedItem.statEffect)
			print(consumableString)
		else:
			print("Type: " + itemType)
		
	elif examinedItem != "printed": # If item still wasn't found, player doesn't have the item
		# Check whether it's a character
		characterDictionary = getCharacter(itemName)
		examinedCharacter = characterDictionary["character"]

		if examinedCharacter is not None and examinedCharacter != "printed":
			# Print character info
			characterType = examinedCharacter.__class__.__name__

			if examinedCharacter.name.lower().split(" ")[0] == "the":
				print("You examine " + examinedCharacter.name + ":")
			else:
				print("You examine the " + examinedCharacter.name + ":")
			
			print()
			print(examinedCharacter.description)
			print()

			if characterType == "Monster":
				print("Type: Monster | Attack: " + str(examinedCharacter.attack) + " | Defense: " + str(examinedCharacter.defense))
			elif characterType == "NPC":
				print("Type: Person | Role: " + examinedCharacter.role)
			else:
				print("Type: " + characterType)
			
		elif examinedCharacter != "printed":
			print("You see no such thing.")
	



# Lists all commands
def helpFunction():
	print("Here is a list of commands I understand:")
	print()
	commands = { 
		"look": "Describes the surrounding environment.",
		"inventory" : "Shows your inventory, equipment, and stats.",
		"help" : "Displays this list of commands.",
		"go [direction]" : "Lets you travel in a particular direction. The 'go' is optional.",
		"get/take/pick up [item]" : "Takes an item from the surroundings and places it in your inventory.",
		"drop [item]" : "Drops an item from your inventory or equipment and places it in the surroundings.",
		"equip [item]" : "Takes an equippable item from the surroundings or your inventory and places it in the relevant equipment slot.",
		"unequip [item]" : "Unequips an item from one of your equipment slots and places it in your inventory.",
		"examine/inspect/appraise [item]" : "Displays information about the examined item."
		}
	for command in commands:
		print(command + " - " + commands[command])


# Use [item] command
def use(itemName):
	global player
	global currentLocation
	# Get item, can be in any of the arrays
	usedItemDictionary = getItem2(itemName)
	usedItem = usedItemDictionary["item"]
	source = usedItemDictionary["source"]

	if usedItem is not None and usedItem != "printed": # Item exists
		try:
			useInstructions = usedItem.useMethod()
			print("You use the " + usedItem.name + ".")

			# Use the "useInstructions" object to determine how the object is used:

			# If it is a healing item:
			if useInstructions["type"] == "Healing":
				if player.fullHP - player.hp <= useInstructions["effect"]:
					player.hp = player.fullHP
					print("The " + usedItem.name + " heals you to full health!")
				else:
					player.hp += useInstructions["effect"]
					print("The " + usedItem.name + " heals you by " + str(useInstructions["effect"]) + " HP.")
			
			# If item should be destroyed upon use
			if useInstructions["destroyed"] == True:
				# Destroy item (remove it from its array)
				print("The " + usedItem.name + " is consumed by its use.")
				if source == "location":
					currentLocation.itemsArray.remove(usedItem)
				elif source == "inventory":
					player.inventory.remove(usedItem)
				elif source == "armor":
					player.equipment["armor"] = None
					updatePlayer()
				elif source == "weapon":
					player.equipment["weapon"] = None
					updatePlayer()

		except:
			print(usedItem.name + " is not usable.")
	elif usedItem is None:
		print("You see no such item.");


# User attacks a monster, gaining the first turn in combat
def attack(monsterName):
	global currentLocation
	global player
	global state
	global states
	global currentTurn
	global whoseTurn

	monsterDictionary = getCharacter(monsterName)
	monster = monsterDictionary["character"]

	if monster is not None and monster != "printed":
		# Monster exists

		# If player starts combat:
		if state == states[0]: # If current state is peaceful
			# Turn state into combat
			state = states[1]
			whoseTurn = player
			currentTurn = 0
		
		
	else:
		print("There is no such entity in sight.")


#### Methods of Ultimate Power!   ####

def inputCommands(userInput):
	global currentLocation
	global directions
	global printLocationDetails

	formattedInput = userInput.lower().split(' ')
	# 1 word commands
	if (len(formattedInput) == 1):
		# 1 word commands
		# print("1 word command!")
		if (formattedInput[0] in directions):
			direction = formattedInput[0]
			movement(direction)
		elif (formattedInput[0] in ["look", "l"]):  # Look command
			printLocationDetails = True
		elif (formattedInput[0] in ["inventory", "i"]):  # Inventory command
			printInventory()
		elif formattedInput[0] == "help": # Help command
			helpFunction()

		# if player typed a non-recognized command or string
		else:
			# Thanks for the solution, Jean Francois Fabre! (Stack Overflow)
			if (formattedInput[0].isupper() or formattedInput[0].islower()):
				# Show responses to unintelligble text
				print(unrecognizedCommand())
			else:
				# Show responses to NO text
				print(unrecognizedCommand(False))

	# multi-word commands
	elif (len(formattedInput) > 1):
		if (formattedInput[0] == "go"):  #1st word in command
			if (formattedInput[1] in directions):  #2nd word in command
				direction = formattedInput[1]
				movement(direction)
		elif (formattedInput[0] in ["get", "take"]):  # Take command
			# Get name of item
			# itemString = formattedInput[1]
			# for i in range(2, len(formattedInput)):
			# 	itemString += " " + formattedInput[i]
			
			take(getItemName(formattedInput, 1))

		elif (formattedInput[0] == "pick"
				and formattedInput[1] == "up"):  # Take command
			if len(formattedInput) > 2:
				# Get name of item
				# itemString = formattedInput[2]
				# for i in range(3, len(formattedInput)):
				# 	itemString += " " + formattedInput[i]
				take(getItemName(formattedInput, 2))
			else:
				print("What item do you want to pick up?")

		elif (formattedInput[0] == "drop"):  # Drop command
			# Get name of item
			# itemString = formattedInput[1]
			# for i in range(2, len(formattedInput)):
			# 	itemString += " " + formattedInput[i]
			drop(getItemName(formattedInput, 1))
		elif formattedInput[0] == "equip":  # Equip command
			# Get name of item
			# itemString = formattedInput[1]
			# for i in range(2, len(formattedInput)):
			# 	itemString += " " + formattedInput[i]
			equip(getItemName(formattedInput, 1))
		elif formattedInput[0] == "unequip":  #Unequip command
			# Get name of item
			# itemString = formattedInput[1]
			# for i in range(2, len(formattedInput)):
			# 	itemString += " " + formattedInput[i]
			unequip(getItemName(formattedInput, 1))
		elif formattedInput[0] in ["examine", "inspect", "appraise"]: # Examine item commmand
			# Get name of item
			# itemString = formattedInput[1]
			# for i in range(2, len(formattedInput)):
			# 	itemString += " " + formattedInput[i]
			examine(getItemName(formattedInput, 1))
		elif formattedInput[0] in ["use"]: # Use item command
			use(getItemName(formattedInput,1))
		elif formattedInput[0] in ["attack", "fight"]:
			attack(getItemName(formattedInput, 1))
		# if player typed a non-recognized command or string
		else:
			print(unrecognizedCommand())



def gameLoop():
	global oldLocation
	global currentLocation
	global player
	global printLocationDetails
	global state

	while (player.hp > 0):  #change to while (player.hp > 0)
		if (currentLocation != oldLocation or printLocationDetails):

			oldLocation = currentLocation
			print(currentLocation.name)
			# Only print description if printLocationDetails is true or if currentLocation.explored is false
			if printLocationDetails == True or currentLocation.explored == False:
				print(currentLocation.description)
			print()
			# If this ran because of a look command, reset the printLocationDetails global boolean
			if (printLocationDetails):
				printLocationDetails = False
			# If this room wasn't already explored, set its explored attribute to True
			if currentLocation.explored == False:
				currentLocation.explored = True

			if (len(currentLocation.monstersArray) > 0):
				# print("There be monsters.")
				monsterString = textRoomFormatter("There ", "monsters", currentLocation)
				
				print(monsterString)
			if (len(currentLocation.itemsArray) > 0):
				# print("There be items.")
				itemsString = textRoomFormatter("You see ", "items",
												currentLocation)
				print(itemsString)

			directionsString = textRoomFormatter("You can go ", "directions",
													currentLocation)
			print(directionsString)
		userInput = input("> ")
		inputCommands(userInput)


# start the game!
initializeGame()
gameLoop()
