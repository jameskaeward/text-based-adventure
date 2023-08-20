################
### GAMEDATA ###
################

locations = {

    "location_Entrance": "NAME_Entrance",
    "location_Main_Hall": "NAME_Main_Hall",
    "location_Shop": "NAME_Equipment_Shop",
    "location_Central": "NAME_Central",
    "location_Tavern": "NAME_Tavern",

    "location_Dungeon": "NAME_Dungeon",

}

town = [

    "location_Entrance", 
    "location_Main_Hall", 
    "location_Shop", 
    "location_Central", 
    "location_Tavern",

]

chest_rarities = {

    "1": "NAME_Wood_Chest",
    "2": "NAME_Stone_Chest",
    "3": "NAME_Gold_Chest",
    "4": "NAME_Diamond_Chest",
    "5": "NAME_Legend_Chest",

}

dungeon = {

    "location_dungeon_room_1": "NAME_dungeon_room_1",   # Dark Cavern
    "location_dungeon_room_2": "NAME_dungeon_room_2",   # Hidden Swamp
    "location_dungeon_room_3": "NAME_dungeon_room_3",   # Flooded Grotto
    "location_dungeon_room_4": "NAME_dungeon_room_4",   # Silent Tomb

}

encounters = {

    # encounter_name    :   [encounter_actions  , attack, hp    , mp    , reward]

    "encounter_chest"   :   [(1,)               , 3     , 5     , 0     , 15    ],
    "encounter_skeleton":   [(1, 2)             , 1     , 4     , 0     , 4     ],
    "encounter_zombie"  :   [(1,)               , 1     , 7     , 0     , 3     ],
    "encounter_ghost"   :   [(1, 2, 3, 4)       , 2     , 3     , 10    , 5     ],
    "encounter_slime"   :   [(1, 2, 3)          , 1     , 2     , 5     , 2     ],
    "encounter_goblin"  :   [(1, 2, 5)          , 1     , 4     , 3     , 8     ],

}

encounter_actions = [

    "encounter_action_null",

    "encounter_action_attack",
    "encounter_action_defend",
    "encounter_action_heal",
    "encounter_action_recharge",
    "encounter_action_run",

]

if __name__ == "__main__":
    print("Run the Main File!")