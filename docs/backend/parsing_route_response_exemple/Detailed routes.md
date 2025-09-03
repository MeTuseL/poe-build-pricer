### /decoder
General skeleton of the response (thing may defer case by case) :
````json
{
      "class": "", # The class of the character
      "ascendClass": "", # The ascendancy class of the character
      "items": [
        {
          "name": "", # Item name
          "itemBase": "", # Type of base
          "rarity": "UNIQUE | RARE | MAGIC | NORMAL", # Rarity of the item
          "properties": [ # There is a lot of different properties, this is just an example of the most common
            {
              "name": "Unique ID",
              "values": "" # hash_or_id_string unique to each item
            },
            {
              "name": "Item Level",
              "values": "" # Level of the item
            },
            {
              "name": "LevelReq",
              "values": "" # Level requirement of the item
            },
            {
              "name": "Implicits",
              "values": "" # Number of implicits modifiers
            },
            {
              "name": "Corrupted",
              "values": "True | False" # Corrupted or not
            }
          ],
          "implicitMods": [
            "" # List of implicit modifiers
          ],
          "explicitMods": [
            "" # Liste of explicit modifiers
          ],
          "type": "Weapon | Armor | Jewelry | Jewel | Flask", # Type of the item
          "subType": "" # Subtype depending on type (e.g. Bow, Ring, Cluster Jewel)
          "5/6Link" # Check if item is five or six linked
        }
      ],
      "skills": [
        {
          "slot": "Body Armour | Gloves | Helmet | Weapon 1 | Weapon 2 | Jewelry | Jewel | Flask", # Slot where the gem is located
          "gems": [
            {
              "count": "", # Number of gems in the slot (always 1 in this version)
              "level": integer, # Level of the gem
              "enabled": true, # Activated of not (mostly irrelevant)
              "quality": integer, # Quality of the gem
              "qualityId": "Default | Alternate", # Qualtity of the gem (not used as of modern PoE)
              "skillId": "InternalGemID", # Internal ID of the gem
              "variantId": "VariantName", # Variant of the gem
              "enableGlobal1": true | false, # ? variable
              "enableGlobal2": true | false, # ? variable, false for item only skills
              "nameSpec": "Display Name of the Gem", # Display name of the gem
              "gemId": "FullMetadataPath", # Full metadata path of the gem
              "Corrupted": true | false # Infered data on, if  the gem is corrupted or not
            }
          ]
        }
      ],
      "linksBySlot": {
        "Slot" : "", # Links of a PoB slot on the form "O-O-O-O O-O" = 6 sockets, 1 groupe of 4 linked and 1 group of 2 linked
      }
    }
````
### /pricer
General skeleton of the response added to the skeleton of the /decoder route (thing may defer case by case)
`````json
{
      "items": [
        {
          "priceChaos": float, # Price of the item in chaos
          "priceDivine": float, # Price of the item in divine
        }
      ],
      "skills": [
        {
          "gems": [
            {
              "priceChaos": float, # Price of the gem in chaos
              "priceDivine": float, # Price of the gem in divine
              "matchedLevel": integer, # Level of gem if there a fallback
              "matchedQuality": integer, # Quality of gem if there a fallback
              "fallbackUsed": true | false # True if a fallback was used in case of original item not found
            }
          ]
        }
      ],
    }
`````