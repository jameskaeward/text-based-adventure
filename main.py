# import time
# import tkinter
from typing import Union, Callable
import customtkinter
import localisation
import config
import configparser
import gameworld as world
import random
import PIL.Image
import os.path

# TODO: Add to settings menu
customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("green")

############################
#### External Functions ####
############################

def read_config():
    config_read = configparser.ConfigParser()
    config_read.read('settings.ini')
    return config_read

if __name__ == "__main__":
    global LANGUAGE
    global FONT_SIZE
    settings = read_config()
    LANGUAGE = str(settings["Settings"]["language"])
    FONT_SIZE = int(settings["Settings"]["font_size"])

def placeholder_function():
    print(loc("TEST_Hello_World"))

def loc(loc_id):
    if LANGUAGE == "l_english":
        text = localisation.l_english.get(loc_id)
    if LANGUAGE == "l_french":
        text = localisation.l_french.get(loc_id)
    
    if text == None:
        text = loc_id

    # text = "MAX IS A NOOB"

    return text

# def random_text(dictonary):
#     random.choice()

def image(image_id):
    image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
    image_location = localisation.images.get(image_id)
    image_location_absolute = os.path.join(image_path, image_location[0])
    image = customtkinter.CTkImage(PIL.Image.open(image_location_absolute), size=(image_location[1], image_location[2]))

    # print(image_path)
    # print(image_location)
    # print(image_location_absolute)
    # print(image)

    return image

# image("IMAGE_Placeholder")

##############
#### Game ####
##############

class Game():
    def __init__(self):
        print(loc("LOG_Game_Start"))

    def start_game(self):

        global PLAYER
        global ENCOUNTER

        if PLAYER is None:
            PLAYER = Player()
            print(loc("LOG_Player_Spawned"))
        else:
            print(loc("LOG_Player_Already_Spawned"))

        if ENCOUNTER is None:
            ENCOUNTER = Encounter()
            print(loc("LOG_Encounter_Spawned"))
        else:
            print(loc("LOG_Encounter_Already_Spawned"))

        # Initalise visual bars
        APP.update_all_bars()

    def locate_player(self):

        if PLAYER is None:
            print(loc("LOG_Player_Not_Found"))
        else:
            return loc(world.locations.get(PLAYER.location))
    
    def move_player(self, location_id):

        if PLAYER is None:
            print(loc("LOG_Player_Not_Found"))
        else:
            PLAYER.move(location_id)

class Player():
    def __init__(self):
        self.alive = True # TODO: Incorporate
        self.hp_max = 10
        self.hp = 10
        self.mp_max = 10
        self.mp = 10
        self.gold = 0
        self.dungeon_count = 0  # NOTE: This is a debug function, TODO: Add to message log
        self.busy = False       # When the player is NOT in combat
        self.in_combat = False  # When the player IS in combat
        # self.tags = [] # TODO: Incorporate all checks into this list
        # self.location = "location_Central"
        self.town_move("location_Central")
    
    # def encounter(self, encounter_type):
    #     self.busy = True
    #     encounter = random.choice(list(world.encounters.keys))

    # Use this to improve readability
    def end_encounter(self):
        self.busy = False
        self.in_combat = False
        APP.update_map()

    # NOTE: This function MUST be called when moving to a location in town
    def town_move(self, location):
        self.location = location
        APP.update_map() # No abusing the map
        print(loc("LOG_Moving_Player"), location)
        self.town_actions(location)

    def town_actions(self, location):

        # Error Check
        if location not in world.town:
            print("ERROR: Player not in town")
            return

        if location == "location_Entrance":
            print("Now in entrance")
            ACTIONBAR.delete_all_options()
            ACTIONBAR.action_config(1, text="ACTION_Enter_Dungeon", command=self.enter_dungeon)

        if location == "location_Main_Hall":
            print("Now in main hall")
            ACTIONBAR.delete_all_options()
            ACTIONBAR.action_config(1, text="ACTION_Wander_Around")

            # TODO: Add secret when a key is found in dungeon

        if location == "location_Shop":
            print("Now in shop")
            ACTIONBAR.delete_all_options()
            ACTIONBAR.action_config(1, text="ACTION_Buy_Item")
            ACTIONBAR.action_config(2, text="ACTION_Sell_Item")
            ACTIONBAR.action_config(3, text="ACTION_Upgrade_Skills")

        if location == "location_Central":
            print("Now in central")
            ACTIONBAR.delete_all_options()
            ACTIONBAR.action_config(1, text="ACTION_View_Achievements")
            ACTIONBAR.action_config(2, text="ACTION_Save_Game")
            ACTIONBAR.action_config(3, text="ACTION_Load_Game")

        if location == "location_Tavern":
            print("Now in tavern")
            ACTIONBAR.delete_all_options()
            ACTIONBAR.action_config(1, text="ACTION_View_Questboard")

    def enter_dungeon(self):
        self.end_encounter()
        self.dungeon_count = 0
        random_room = random.choice(list(world.dungeon.keys()))
        self.location = "location_Dungeon"
        print(loc("LOG_Entering_Dungeon"))
        self.dungeon_move(random_room)
        # print("Entering: ", random_room)

    def exit_dungeon(self):
        self.busy = False
        self.in_combat = False
        print(loc("LOG_Exiting_Dungeon"))
        self.hp = self.hp_max # Could change to recharge at central plaza
        self.mp = self.mp_max # 
        APP.update_all_bars() # Must be called every time a player value changes
        dungeon_exit_message = loc("MESSAGE_Exited_Dungeon").format(self.dungeon_count)
        APP.send_message(dungeon_exit_message) # NOTE: Function MUST be localised
        print("Dungeon Room Count:", self.dungeon_count)
        self.dungeon_count = 0 # NOTE: Probably unecessary but sets to 0 anyway
        self.town_move("location_Entrance")

    def enter_random_dungeon_room(self):
        random_room = random.choice(list(world.dungeon.keys()))
        self.dungeon_move(random_room)
        # print("Entering: ", random_room)

    def dungeon_move(self, room):
        print("Entering: ", room)
        APP.update_map() # No abusing the map
        
        if room not in world.dungeon:
            print("ERROR: Wrong dungeon room")
            return
        
        ACTIONBAR.delete_all_options()

        # Set exit parameters here
        # TODO: Difficulty settings or different dungeons

        # NOTE Make sure to change these values when testing is done
        minimum_dungeon_rooms = 3
        exit_threshold = 5

        # The Exit
        if self.dungeon_count >= minimum_dungeon_rooms: # Must enter a mininum number of rooms before having a chance to exit

            exit_chance = self.dungeon_count*random.random()
            print("Exit chance: ", exit_chance)

            if exit_chance > exit_threshold:
                self.busy = True
                APP.update_map()
                ACTIONBAR.action_config(1, text="ACTION_Exit_Dungeon", command=self.exit_dungeon)
                ACTIONBAR.action_config(2, text="ACTION_Return_Dungeon", command=self.enter_dungeon)
                return # Function stops here to not continue into dungeon

        self.dungeon_count = self.dungeon_count + 1

        ENCOUNTER.spawn_encounter_random()

class Encounter():
    def __init__(self):

        self.active = None
        self.hp = None
        self.hp_max = None
        self.mp = None
        self.mp_max = None
        self.reward = None
        self.attack = None
        self.type = None
        self.available_actions = []

    def spawn_encounter_random(self):
        encounter = random.choice(list(world.encounters.keys()))
        print("Spawning:", encounter)
        self.encounter_setup(encounter)

    def encounter_setup(self, encounter_type):

        # Reset encounter
        self.active = True
        self.available_actions = []

        self.type = encounter_type

        # Retrieve data from gameworld file
        encounter_parameters = list(world.encounters.get(encounter_type))

        # Determines what actions the encounter can take
        available_action_id = list(encounter_parameters[0])
        for x in available_action_id:
            self.available_actions.append(world.encounter_actions[x])

        print(self.available_actions)

        # Refilling encounter bars
        self.hp_max = encounter_parameters[2]
        self.hp = self.hp_max
        print("Encounter HP:", self.hp)
        self.mp_max = encounter_parameters[3]
        self.mp = self.mp_max
        print("Encounter MP:", self.mp)

        # Setting encounter stats
        self.attack = encounter_parameters[1]
        self.reward = encounter_parameters[4]

        # Sets actions in player UI
        self.encounter_type_check(encounter_type)

    def encounter_type_check(self, encounter_type):
        
        match encounter_type:
            case "encounter_chest":
                print("Chest encounter")
                APP.send_message(loc("MESSAGE_Found_Chest")) # NOTE: Function MUST be localised
                PLAYER.end_encounter() # Player can choose to not open chest
                ACTIONBAR.delete_all_options()
                ACTIONBAR.action_config(1, text=loc("ACTION_Open_Chest"), command=self.unlock_chest)

            case "encounter_skeleton":
                print("Skeleton encounter")
                APP.send_message(loc("MESSAGE_Found_Skeleton")) # NOTE: Function MUST be localised
                PLAYER.in_combat = True
                APP.update_map()
                ACTIONBAR.delete_all_options()
                ACTIONBAR.action_config(1, text=loc("ACTION_Fight"), command=self.fight)
                ACTIONBAR.action_config(2, text=loc("ACTION_Retreat"), command=self.retreat)

            case "encounter_zombie":
                print("Zombie encounter")
                APP.send_message(loc("MESSAGE_Found_Zombie")) # NOTE: Function MUST be localised
                PLAYER.in_combat = True
                APP.update_map()
                ACTIONBAR.delete_all_options()
                ACTIONBAR.action_config(1, text=loc("ACTION_Fight"), command=self.fight)
                ACTIONBAR.action_config(2, text=loc("ACTION_Retreat"), command=self.retreat)

            case "encounter_ghost":
                print("Ghost encounter")
                APP.send_message(loc("MESSAGE_Found_Ghost")) # NOTE: Function MUST be localised
                PLAYER.in_combat = True
                APP.update_map()
                ACTIONBAR.delete_all_options()
                ACTIONBAR.action_config(1, text=loc("ACTION_Fight"), command=self.fight)
                ACTIONBAR.action_config(2, text=loc("ACTION_Retreat"), command=self.retreat)

            case "encounter_slime":
                print("Slime encounter")
                APP.send_message(loc("MESSAGE_Found_Slime")) # NOTE: Function MUST be localised
                PLAYER.in_combat = True
                APP.update_map()
                ACTIONBAR.delete_all_options()
                ACTIONBAR.action_config(1, text=loc("ACTION_Fight"), command=self.fight)
                ACTIONBAR.action_config(2, text=loc("ACTION_Retreat"), command=self.retreat)

            case "encounter_goblin":
                print("Goblin encounter")
                APP.send_message(loc("MESSAGE_Found_Goblin")) # NOTE: Function MUST be localised
                PLAYER.in_combat = True
                APP.update_map()
                ACTIONBAR.delete_all_options()
                ACTIONBAR.action_config(1, text=loc("ACTION_Fight"), command=self.fight)
                ACTIONBAR.action_config(2, text=loc("ACTION_Retreat"), command=self.retreat)

    # TODO: Unsucessful Retreat
    def retreat(self):
        ACTIONBAR.disable_all_options()
        PLAYER.end_encounter()

    def fight(self):
        # ACTIONBAR.delete_all_options()
        placeholder_function()

    # TODO: Mimic chest
    def unlock_chest(self):

        # Randomise chest rarity
        chest_rarity = random.randint(1, 5)
        # randomiser = 1.0 - ( 0.5 - random.random ) * 0.5
        self.reward = int(self.reward * chest_rarity)
        print("Chest worth:", self.reward)

        # Sends message in the game
        opening_message = loc("MESSAGE_Opened_Chest")
        chest_type = loc(world.chest_rarities[str(chest_rarity)])
        sent_message = opening_message.format(chest_type, self.reward)
        APP.send_message(sent_message) # NOTE: Function MUST be localised

        self.encounter_defeat()

    # Deinitialise the encounter
    def encounter_defeat(self):
        ACTIONBAR.disable_all_options()
        
        PLAYER.gold = PLAYER.gold + self.reward
        print(f"Encounter defeated for {self.reward} gold, new balance is {PLAYER.gold}")

        APP.update_all_bars()

        self.active = False


###############
##### GUI #####
###############

## Pop-Up Interfaces

class Map(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        
        self.resizable(width=False, height=False)
        self.title(loc("NAME_Map"))
        self.geometry("700x300")
        self.rowconfigure((1, 2, 3, 4, 5, 6), weight=1)
        self.columnconfigure((1, 2, 3, 4, 5), weight=1)
        self.draw_map()

    # Renders the map, separate function to allow updating the map
    def draw_map(self):

        # Removes old map elements
        for item in self.winfo_children():
            item.destroy()

        # Player should not see this, checks if player is present
        if PLAYER is None: 
            label = customtkinter.CTkLabel(self, text=loc("NAME_Map"), font=FONT_BOLD)
            label.grid(column=1, columnspan=5, padx=20, pady=20)
            
            warning = customtkinter.CTkLabel(self, text=loc("DESC_No_Player_Found"), font=FONT_DEFAULT)
            warning.grid(row=1, rowspan=4, column=1, columnspan=5, padx=20, pady=20)

            # print("Player doesn't exist!")
            return
        
        # Player must finish interactions before moving to another location
        if PLAYER.busy is True or PLAYER.in_combat is True:
            label = customtkinter.CTkLabel(self, text=loc("NAME_Map"), font=FONT_BOLD)
            label.grid(column=1, columnspan=5, padx=20, pady=20)

            if PLAYER.in_combat is True:
                warning = customtkinter.CTkLabel(self, text=loc("DESC_Finish_Interaction_Combat"), font=FONT_DEFAULT)
                warning.grid(row=1, rowspan=4, column=1, columnspan=5, padx=20, pady=20)
            else:
                warning = customtkinter.CTkLabel(self, text=loc("DESC_Finish_Interaction"), font=FONT_DEFAULT)
                warning.grid(row=1, rowspan=4, column=1, columnspan=5, padx=20, pady=20)

            # print("Player is busy!")
            return

        # Town Map
        if PLAYER.location in world.town:

            # print("Player is in town")

            player_location = loc("DESC_Current_Location") + APP.game.locate_player()

            label = customtkinter.CTkLabel(self, text=player_location, font=FONT_BOLD)
            label.grid(column=1, columnspan=5, padx=20, pady=20)

            navbutton1 = customtkinter.CTkButton(self, text=loc("NAME_Entrance"), command=lambda: self.map_move("location_Entrance", in_dungeon=False))
            navbutton1.grid(row=6, column=3, padx=10, pady=10, sticky="NESW")

            navbutton2 = customtkinter.CTkButton(self, text=loc("NAME_Main_Hall"), command=lambda: self.map_move("location_Main_Hall", in_dungeon=False))
            navbutton2.grid(row=2, column=3, padx=10, pady=10, sticky="NESW")

            navbutton3 = customtkinter.CTkButton(self, text=loc("NAME_Tavern"), command=lambda: self.map_move("location_Tavern", in_dungeon=False))
            navbutton3.grid(row=4, column=1, padx=10, pady=10, sticky="NESW")

            navbutton4 = customtkinter.CTkButton(self, text=loc("NAME_Equipment_Shop"), command=lambda: self.map_move("location_Shop", in_dungeon=False))
            navbutton4.grid(row=4, column=5, padx=10, pady=10, sticky="NESW")

            navbutton5 = customtkinter.CTkButton(self, text=loc("NAME_Central"), command=lambda: self.map_move("location_Central", in_dungeon=False))
            navbutton5.grid(row=4, column=3, padx=10, pady=10, sticky="NESW")

        # Dungeon Map
        else:

            # print("Player in dungeon")

            player_location = loc("DESC_Current_Location") + APP.game.locate_player()

            label = customtkinter.CTkLabel(self, text=player_location, font=FONT_BOLD)
            label.grid(column=1, columnspan=5, padx=20, pady=20)

            dungeon_destinations = list(world.dungeon.keys())

            destination_1 = random.choice(dungeon_destinations)
            destination_1_name = world.dungeon[destination_1]
            dungeon_destinations.remove(destination_1) # This removes duplicates, just make sure there at least two dungeon rooms otherwise it will throw an error

            destination_2 = random.choice(dungeon_destinations)
            destination_2_name = world.dungeon[destination_2]

            navbutton1 = customtkinter.CTkButton(self, text=loc(destination_1_name), command=lambda: self.map_move(destination_1, in_dungeon=True))
            navbutton1.grid(row=2, column=2, padx=10, pady=10, sticky="NESW")

            navbutton2 = customtkinter.CTkButton(self, text=loc(destination_2_name), command=lambda: self.map_move(destination_2, in_dungeon=True))
            navbutton2.grid(row=2, column=4, padx=10, pady=10, sticky="NESW")

    def map_move(self, new_location, in_dungeon):
        if in_dungeon is False:
            PLAYER.town_move(new_location)
            move = True
        if in_dungeon is True:
            PLAYER.dungeon_move(new_location)
            move = True

        if move is not True:
            print("ERROR: map_move called incorrecty")

class Settings(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        
        self.resizable(width=False, height=False)
        self.title(loc("NAME_Settings"))
        self.geometry("400x400")

        # This doesn't use the localisation function as it breaks the combobox
        languages = list(localisation.l_index.keys())

        font_sizes = ["15", "20", "25", "30"]
        
        self.label = customtkinter.CTkLabel(self, text = loc("NAME_Settings"), font=FONT_BOLD)
        self.label.pack(pady=10)

        self.language_select_label = customtkinter.CTkLabel(self, text = loc("NAME_Languages"), font=FONT_DEFAULT)
        self.language_select_label.pack(pady=10)
        self.language_select = customtkinter.CTkOptionMenu(self, values = languages, command = self.change_language)
        self.language_select.set(localisation.l_index_reverse.get(LANGUAGE))
        self.language_select.pack(pady=10)

        self.font_select_label = customtkinter.CTkLabel(self, text = loc("NAME_Font_Size"), font=FONT_DEFAULT)
        self.font_select_label.pack(pady=10)
        self.font_select = customtkinter.CTkOptionMenu(self, values = font_sizes, command = self.change_font_size)
        self.font_select.set(FONT_SIZE)
        self.font_select.pack(pady=10)

        self.restart = None
        
    def change_language(self, new_language):
        language_id = localisation.l_index.get(new_language)
        config.change_setting(language=language_id)
        self.setting_changed()

    def change_font_size(self, new_font_size):
        config.change_setting(font_size=new_font_size)
        self.setting_changed()

    # Prompts player to restart to apply settings
    def setting_changed(self):
        if self.restart == None:
            self.restart = customtkinter.CTkLabel(self, text=loc("DESC_Apply_To_Restart"))
            self.restart.pack(pady=10)

#################
## Main Frames ##
#################

class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        self.resizable(width=False, height=False)

        # Setting font here as it gives an error when set outside

        global FONT_DEFAULT
        global FONT_BOLD

        FONT_DEFAULT = customtkinter.CTkFont(size=FONT_SIZE, weight="normal")
        FONT_BOLD = customtkinter.CTkFont(size=round(FONT_SIZE*1.3), weight="bold")

        global PLAYER
        global ENCOUNTER

        PLAYER = None
        ENCOUNTER = None

        self.game = Game()

        self.geometry("1000x500")
        self.title(loc("NAME_Text_Based_Adventure"))

        # self.grid_columnconfigure(1, weight=1)
        # self.grid_rowconfigure(0, weight=1)

        self.start_frame = BaseFrame(self)
        self.start_frame.starting_frame(self)
        self.start_frame.pack(expand=True)
        self.main_frame = BaseFrame(self)
        self.main_frame.main_frame()

        global ACTIONBAR

        ACTIONBAR = ActionBar(self.main_frame)
        ACTIONBAR.grid(row=1, column=1, sticky="NESW")

        self.mainwindow = MainWindow(self.main_frame)
        self.mainwindow.grid(row=0, column=1, sticky="NESW")

        self.sidebar = SideBar(self.main_frame, self)
        self.sidebar.grid(row=0, rowspan=2, column=0, padx=10)

        self.map = None
        self.settings = None

    def open_map(self):
        if self.map is None or not self.map.winfo_exists():
            self.map = Map(self)  # Create window if its None or destroyed
        else:
            self.map.focus()  # if window exists focus it

    # NOTE: MUST be called after movement
    def update_map(self):
        if self.map is None or not self.map.winfo_exists():
            # print("No map to destroy")
            pass
        else:
            self.map.draw_map()

    def open_settings(self):
        if self.settings is None or not self.settings.winfo_exists():
            self.settings = Settings(self)  # Create window if its None or destroyed
        else:
            self.settings.focus()  # if window exists focus it

    def start_game(self):
        self.start_frame.pack_forget()
        self.main_frame.pack(expand=True, fill="both")
        self.game.start_game()

    def update_all_bars(self):
        self.mainwindow.update_bar("health_bar")
        self.mainwindow.update_bar("mana_bar")
        self.mainwindow.update_bar("gold_bar")

    def send_message(self, message):
        self.mainwindow.add_message(message)

class BaseFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
    
    def starting_frame(self, master):

        self.title = customtkinter.CTkLabel(self, text=loc("NAME_Text_Based_Adventure"), font=FONT_BOLD)
        self.title.pack(expand=True, pady=10)
        self.button = customtkinter.CTkButton(self, text=loc("ACTION_Start_Game"), font=FONT_BOLD, command=master.start_game)
        self.button.pack(pady=10)


    def main_frame(self):

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    # TODO: Add make the sidebar a method
    # def side_bar(self):

    #     self.grid_rowconfigure((1, 2, 3, 4), weight=0)
    #     self.grid_rowconfigure(5, weight=10)

    #     self.label = customtkinter.CTkLabel(self, width=10, text=loc("NAME_Menu"), font=FONT_BOLD)
    #     self.label.grid(row=0, column=0, padx=10, sticky="N")

    #     self.open_settings = customtkinter.CTkButton(master=self, width=10, text=loc("DESC_Open_Settings"), command=APP.open_settings)
    #     self.open_settings.grid(row=1, column=0, pady=10)
    #     self.open_map = customtkinter.CTkButton(master=self, width=10, text=loc("DESC_Open_Map"), command=APP.open_map)
    #     self.open_map.grid(row=2, column=0, pady=10)

class SideBar(customtkinter.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")

        self.grid_rowconfigure((1, 2, 3, 4), weight=0)
        self.grid_rowconfigure(5, weight=10)

        self.label = customtkinter.CTkLabel(self, width=10, text=loc("NAME_Menu"), font=FONT_BOLD)
        self.label.grid(row=0, column=0, padx=10, sticky="N")

        self.open_settings = customtkinter.CTkButton(master=self, width=10, text=loc("DESC_Open_Settings"), command=app.open_settings)
        self.open_settings.grid(row=1, column=0, pady=10)
        self.open_map = customtkinter.CTkButton(master=self, width=10, text=loc("DESC_Open_Map"), command=app.open_map)
        self.open_map.grid(row=2, column=0, pady=10)
        # self.test_game = customtkinter.CTkButton(master=self, width=10, text=loc("DESC_Test_Game"), command=app.game.start_game)
        # self.test_game.grid(row=3, column=0, pady=10)

class MainWindow(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(4, weight=1)
        
        self.label = customtkinter.CTkLabel(self, width=10, text=loc("NAME_Main_Window"), font=FONT_BOLD)
        self.label.grid(row=0, column=1)

        self.health_bar_label = customtkinter.CTkLabel(self, width=10, text=loc("NAME_Health"), font=FONT_DEFAULT)
        self.health_bar_label.grid(row=1, column=0, padx=10, pady=2)
        self.health_bar = customtkinter.CTkProgressBar(master=self)
        self.health_bar.grid(row=1, column=1, sticky="W", padx=10, pady=2)

        self.mana_bar_label = customtkinter.CTkLabel(self, width=10, text=loc("NAME_Mana"), font=FONT_DEFAULT)
        self.mana_bar_label.grid(row=2, column=0, padx=10, pady=2)
        self.mana_bar = customtkinter.CTkProgressBar(master=self)
        self.mana_bar.grid(row=2, column=1, sticky="W", padx=10, pady=2)

        self.gold_bar = customtkinter.CTkLabel(self, width=10, text=loc("PLAECHOLDER"), font=FONT_DEFAULT)
        self.gold_bar.grid(row=3, column=0, columnspan=2, sticky="W", padx=10, pady=2)

        # NOTE: Textbox must use .insert method to add text
        self.messages = customtkinter.CTkTextbox(self, state="disabled", height=100)
        self.messages.grid(row=5, column=0, columnspan=2, sticky="EW", padx=10, pady=10)

    def update_bar(self, bar):
        match bar:
            case "health_bar":
                health_level = PLAYER.hp / PLAYER.hp_max
                self.health_bar.set(health_level)

            case "mana_bar":
                mana_level = PLAYER.mp / PLAYER.mp_max
                self.mana_bar.set(mana_level)

            case "gold_bar":
                gold = PLAYER.gold
                gold_level = loc("NAME_Gold") + " : " + str(gold)
                self.gold_bar.configure(text=str(gold_level))

    # TODO: Delete old text with a setting for how many lines
    def add_message(self, message):
        message_newline = message + "\n"
        self.messages.configure(state="normal")
        self.messages.insert(0.0, message_newline)
        self.messages.configure(state="disabled")

class ActionBar(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.grid_columnconfigure(1, weight=1)

        self.title = customtkinter.CTkLabel(self, width=10, text=loc("NAME_Action_Bar"), font=FONT_BOLD)
        self.title.grid(row=0, column=1, padx=10, pady=10, sticky="NSEW")
        self.options = customtkinter.CTkFrame(master=self, fg_color="transparent")
        self.options.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky="W")

        # Options Pre-Initialise

        self.total_options = range(1, 6)

        for x in self.total_options:
            locals()[f"option_{x}"] = customtkinter.CTkFrame(master=self.options, fg_color="transparent")
            locals()[f"option_{x}"].button = customtkinter.CTkButton(master=locals()[f"option_{x}"], width=10)
            locals()[f"option_{x}"].label = customtkinter.CTkLabel(master=locals()[f"option_{x}"], width=10)

        # option_1 = customtkinter.CTkFrame(master=self.options, fg_color="transparent")
        # option_1.button = customtkinter.CTkButton(master=option_1, width=10)
        # option_1.label = customtkinter.CTkLabel(master=option_1, width=10)

        # option_2 = customtkinter.CTkFrame(master=self.options, fg_color="transparent")
        # option_2.button = customtkinter.CTkButton(master=option_2, width=10)
        # option_2.label = customtkinter.CTkLabel(master=option_2, width=10)

        # option_3 = customtkinter.CTkFrame(master=self.options, fg_color="transparent")
        # option_3.button = customtkinter.CTkButton(master=option_3, width=10)
        # option_3.label = customtkinter.CTkLabel(master=option_3, width=10)

        # option_4 = customtkinter.CTkFrame(master=self.options, fg_color="transparent")
        # option_4.button = customtkinter.CTkButton(master=option_4, width=10)
        # option_4.label = customtkinter.CTkLabel(master=option_4, width=10)

        self.local_variables = locals()
        # print(self.local_variables)

        # TODO: Make sure to set .grid later 

    # Configures initialised buttons
    # TODO: Use dictionary arguments **parameters
    # def action_config(self, button_row, input_text, function):
    #    update_button = self.local_variables[f"option_{button_row}"]    # TODO Replace update_button with locals(self)[format(f"option_{button}")] as Python variables are stupid
    #    update_button.configure(text=input_text, command=function)      # format() is not needed: format(f"option_{button_row}")
    #    update_button.grid(row=button_row)
    #    locals(self)[f"option_{button_row}"] = update_button # TODO Refer to previous TODO
    #    update_button.grid_forget()

    def action_config(self,
                      button_row,
                      text: str = "DESC_Placeholder_Button_Text",
                    #   label_text: str = "DESC_Placeholder_Label_Text",
                      command: Union[Callable[[], None], None] = lambda: placeholder_function()):
        
        # Old Code
        # if "text" in parameters: #TODO Change to button reference
        #    self.local_variables[f"option_{button_row}"].configure(text=parameters["text"])
        # if "command" in parameters:
        #    self.local_variables[f"option_{button_row}"].configure(command=lambda: parameters["command"])


        self.local_variables[f"option_{button_row}"].button.configure(text=f"{button_row}. "+loc(text), command=command, state="normal")
        self.local_variables[f"option_{button_row}"].button.grid(row=0, column=0, padx=10)
        # self.local_variables[f"option_{button_row}"].label.configure(text=loc(label_text))
        # self.local_variables[f"option_{button_row}"].label.grid(row=0, column=1, padx=10)

        self.local_variables[f"option_{button_row}"].grid(row=button_row, pady=10, sticky="EW")

    def delete_all_options(self):
        for x in self.total_options:
            self.delete_option(x)

    def delete_option(self, button_row):
        # print("Disabling option: ", button_row)
        self.local_variables[f"option_{button_row}"].grid_forget()

    def disable_all_options(self):
        for x in self.total_options:
            self.disable_option(x)

    def disable_option(self, button_row):
        # print("Disabling option: ", button_row)
        self.local_variables[f"option_{button_row}"].button.configure(state="disabled")

    # # Old Code for dynamic number of options #
    #
    # def dialogue_option(self, input_text, function, nrow):
    #
    #    rows = customtkinter.CTkFrame(master=self.options, fg_color="transparent")
    #    #rows = tkinter.Frame(master=self.options)
    #    rows.grid(row=nrow, column=0, pady=10, sticky="EW")
    #
    #    options = customtkinter.CTkButton(master=rows, width=10, text=input_text, command=function)
    #    options.grid(row=nrow, column=0, padx=10)
    #    label = customtkinter.CTkLabel(master=rows, width=10, text=input_text)
    #    label.grid(row=nrow, column=1, padx=10)
    #
    # Example of getting dynamic buttons
    # def get(self):
    #    checked_checkboxes = []
    #    for checkbox in self.checkboxes:
    #        if checkbox.get() == 1:
    #            checked_checkboxes.append(checkbox.cget("text"))
    #    return checked_checkboxes
    #
    # def reset_dialogue(self):
    #
    #    for rows in self.options:
    #        #rows.destroy()
    #        rows.grid.forget()


# class ActionBarOptions(customtkinter.CTkFrame):
#    def __init__(self, master):
#        super().__init__(master)
#        options = 0
#
#    def dialogue_option(self, input_text):
#        self.label = customtkinter.CTkLabel(self, width=10, text=input_text, font=customtkinter.CTkFont(size=20, weight="normal"))
#        self.label.grid(row=options, column=0, padx=10, pady=10, sticky="NSEW")
#
#        options = options + 1
#
# Use the get() method instead of having dynamic object names



# test = ActionBarOptions.dialogue_option(ACTIONBAR.options, "Hello World")
# print("Hello World")

# https://felipetesc.github.io/CtkDocs/#/multiple_frames
# https://pythonguides.com/convert-python-file-to-exe-using-pyinstaller/

## This runs the application ##
if __name__ == "__main__":
    global APP
    APP = App()
    APP.mainloop()