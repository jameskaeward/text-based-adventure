l_index = {

    "English": 'l_english',
    "Français": 'l_french',

}

l_index_reverse = {

    'l_english': "English",
    "l_french": 'Français',

}

images = {

    # "TAG": ["File Location", Image Width, Image Height]

    "IMAGE_Placeholder": ["placeholder.png", 1000, 1000],

}

l_english = {

    # Title

    "NAME_Text_Based_Adventure": "Graphics Based Adventure",
    "ACTION_Start_Game": "Start Game",

    "NAME_Action_Bar": "Actions",

    # Menus

    "NAME_Map": "Map",
    "DESC_Open_Map": "Open Map",

    "DESC_Open_Settings": "Open Settings",
    "NAME_Settings": "Settings",

    "DESC_No_Player_Found": "Player doesn't exist!",
    "NAME_Menu": "Menu",
    "NAME_Main_Window": "Main Window",

    "NAME_Health": "Health",
    "NAME_Mana": "Mana",
    "NAME_Gold": "Gold",

    # Map Locations

    "DESC_Current_Location": "Current Location: ",
    
    "DESC_Finish_Interaction": "The map cannot be used right now",
    "DESC_Finish_Interaction_Combat": "The map cannot be used in combat!",

    "NAME_Entrance": "Entrance",
    "NAME_Main_Hall": "Town Hall",
    "NAME_Equipment_Shop": "Augury and Alchemy",
    "NAME_Central": "Plaza",
    "NAME_Tavern": "The Hypnotic Meerkat",

    "NAME_Dungeon": "The Dungeon",

    "NAME_dungeon_room_1": "Dark Cavern",
    "NAME_dungeon_room_2": "Hidden Swamp",
    "NAME_dungeon_room_3": "Flooded Grotto",
    "NAME_dungeon_room_4": "Silent Tomb",

    # Chest Rarities

    "NAME_Wood_Chest": "Castaway's Chest",
    "NAME_Stone_Chest": "Seafarer's Chest",
    "NAME_Gold_Chest": "Marauders Chest",
    "NAME_Diamond_Chest": "Captain's Chest",
    "NAME_Legend_Chest": "Chest of Legends",

    # Game Messages

    "MESSAGE_Found_Chest": "You spot a sparkling chest in the distance!",
    "MESSAGE_Found_Skeleton": "A skeleton's arrow surprises you!",
    "MESSAGE_Found_Zombie": "A zombie walks out of the corner!",
    "MESSAGE_Found_Ghost": "A feel a cold shiver as a ghost approaches!",
    "MESSAGE_Found_Slime": "You find a ball, which turns out to be a slime!",
    "MESSAGE_Found_Goblin": "You hear metal clinking, it was a goblin!",

    "MESSAGE_Opened_Chest": "You opened the {} chest for {} gold!",
    "MESSAGE_Exited_Dungeon": "You manage to escape the dungeon with your life, traversing a total of {} rooms inside.",

    # Settings

    "NAME_English": "English",
    "NAME_French": "French",

    "NAME_Languages": "Language",
    "NAME_Font_Size": "Font Size",

    "DESC_Apply_To_Restart": "Restart application to apply settings.",

    # Gameplay

    "ACTION_Wander_Around": "Look around",

    "ACTION_Upgrade_Skills": "Upgrade skills",
    "ACTION_Buy_Item": "Buy item",
    "ACTION_Sell_Item": "Sell item",

    "ACTION_View_Achievements": "View accomplishments",
    "ACTION_Save_Game": "Save game",
    "ACTION_Load_Game": "Load game",

    "ACTION_View_Questboard": "View questboard",

    "ACTION_Enter_Dungeon": "Enter the dungeon",
    "ACTION_Exit_Dungeon": "Exit the dungeon",
    "ACTION_Return_Dungeon": "Return to the dungeon",

    # Dungeon

    "ACTION_Open_Chest": "Open Chest",
    "ACTION_Fight": "Fight",
    "ACTION_Retreat": "Retreat",

    # Testing Localisation

    "TEST_Hello_World": "Feature not yet implemented",
    "NAME_Test": "Test",

    "LOG_Game_Start": "Game Start",
    "LOG_Player_Spawned": "Player Spawned",
    "LOG_Player_Already_Spawned": "Player Already Spawned",

    "LOG_Entering_Dungeon": "Entering Dungeon",
    "LOG_Exiting_Dungeon": "Exiting Dungeon",
    "LOG_Moving_Player": "Moving player to",

    "PLACEHOLDER": "Placeholder Text",

}

l_french = {

    # Titles

    "NAME_Text_Based_Adventure": "Aventure textuelle",
    "NAME_Action_Bar": "Barre d'action",

    # Menu
    "NAME_Map": "Carte",
    "DESC_Open_Map": "Ouvrir la carte",

    "DESC_Open_Settings": "Ouvrir les paramètres",
    "NAME_Settings": "Paramètres",

    "DESC_No_Player_Found": "Le joueur n'existe pas",
    "NAME_Menu": "Menu",
    "NAME_Main_Window": "Fenêtre Principale",

    # Map Locations
    "DESC_Current_Location": "Localisation actuelle: ",
    "NAME_Entrance": "L'entrée",

    # Settings

    "NAME_English": "Anglais",
    "NAME_French": "Français",

    "DESC_Apply_To_Restart": "Redémarrez l'application pour appliquer les paramètres.",

    # Testing Localisation

    "TEST_Hello_World": "Bonjour le monde!",
    "NAME_Test": "Test",

    "LOG_Game_Start": "Jeu commencé",
    "LOG_Player_Spawned": "Joueur engendré",
    "LOG_Player_Already_Spawned": "Joueur déjà apparu",
}

if __name__ == "__main__":
    print("Run the Main File!")
    # print(l_english)
    # print(l_french)
    # print(l_index.values())
    # print(l_index.keys())