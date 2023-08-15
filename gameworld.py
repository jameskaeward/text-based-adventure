# NOTE Location IDs are in word form
# Example ID: NAME_Entrance
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

dungeon = [
                                # TODO: Add comments here for room description
    "location_dungeon_room_1",  # 
    "location_dungeon_room_2",  # 
    "location_dungeon_room_3",  # 
    "location_dungeon_room_4",  # 

]

encounters = {

    # encounter_name: [encounter_actions, attack, hp, mp, reward]

    "encounter_chest": [(0), 0, 10, 0, 20],
    "encounter_skeleton": [(1, 2), 0, 10, 0, 20],
    "encounter_zombie": [(1), 0, 10, 0, 20],
    "encounter_ghost": [(1, 2, 3, 4), 0, 10, 10, 20],
    "encounter_slime": [(1, 2, 3), 0, 10, 5, 20],
    "encounter_goblin": [(1, 2, 5), 0, 10, 3, 20],

}

# TODO: Append and test to encounter instance
# For x in encounters
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