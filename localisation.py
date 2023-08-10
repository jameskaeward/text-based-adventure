l_index = {

    "English": 'l_english',
    "Français": 'l_french',

}

l_index_reverse = {

    'l_english': "English",
    "l_french": 'Français',

}

l_english = {

    # Title

    "NAME_Text_Based_Adventure": "Text Based Adventure",
    "NAME_Action_Bar": "Action Bar",

    # Menus

    "NAME_Map": "Map",
    "DESC_Open_Map": "Open Map",

    "DESC_Open_Settings": "Open Settings",
    "NAME_Settings": "Settings",

    "DESC_No_Player_Found": "Player doesn't exist!",
    "NAME_Menu": "Menu",
    "NAME_Main_Window": "Main Window",

    # Map Locations

    "DESC_Current_Location": "Current Location: ",
    "NAME_Entrance": "Entrance",

    # Settings

    "NAME_English": "English",
    "NAME_French": "French",

    "DESC_Apply_To_Restart": "Restart application to apply settings.",

    # Testing Localisation

    "TEST_Hello_World": "Hello World!",
    "NAME_Test": "Test",

    "LOG_Game_Start": "Game Start",
    "LOG_Player_Spawned": "Player Spawned",
    "LOG_Player_Already_Spawned": "Player Already Spawned",
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
    #print(l_english)
    #print(l_french)
    #print(l_index.values())
    print(l_index.keys())