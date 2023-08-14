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
    global _language
    global _font_size
    global _settings
    _settings = read_config()
    _language = str(_settings["Settings"]["language"])
    _font_size = int(_settings["Settings"]["font_size"])

def placeholder_function():
    print(loc("TEST_Hello_World"))

def loc(loc_id):
    if _language == "l_english":
        text = localisation.l_english.get(loc_id)
    if _language == "l_french":
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

        self.player = None

    def start_game(self):

        if self.player is None:
            self.player = Player()
            print(loc("LOG_Player_Spawned"))
        else:
            print(loc("LOG_Player_Already_Spawned"))

    def locate_player(self):

        if self.player is None:
            print(loc("LOG_Player_Not_Found"))
        else:
            return loc(world.locations.get(self.player.location))
    
    def move_player(self, location_id):

        if self.player is None:
            print(loc("LOG_Player_Not_Found"))
        else:
            self.player.move(location_id)

class Player():
    def __init__(self):
        self.state = True # Alive
        self.hp_max = 10
        self.hp = 10
        self.mp_max = 10
        self.mp = 10
        self.gold = 0
        self.dungeon_count = 0
        self.busy = False # NOTE: For use with the map so player cannot run away
        self.in_combat = False
        # self.tags = [] # TODO: Incorporate all checks into this list
        # self.location = "location_Central"
        self.town_move("location_Central")
    
    def encounter(self, encounter_type):
        self.busy = True
        encounter = random.choice(list(world.encounters.keys))

    # NOTE: This function MUST be called when moving to a location in town
    def town_move(self, location):
        app.close_map() # No abusing the map
        print(loc("LOG_Moving_Player"), location)
        self.location = location
        self.town_actions(location)

    def town_actions(self, location):

        # Error Check
        if location not in world.town:
            print("ERROR: Player not in town")
            return

        if location == "location_Entrance":
            print("Now in entrance")
            app.actionbar.disable_all_options()
            app.actionbar.action_config(1, text="ACTION_Enter_Dungeon", command=self.enter_dungeon)

        if location == "location_Main_Hall":
            print("Now in main hall")
            app.actionbar.disable_all_options()
            app.actionbar.action_config(1, text="ACTION_Wander_Around")

            # TODO: Add secret when a key is found in dungeon

        if location == "location_Shop":
            print("Now in shop")
            app.actionbar.disable_all_options()
            app.actionbar.action_config(1, text="ACTION_Buy_Item")
            app.actionbar.action_config(2, text="ACTION_Sell_Item")
            app.actionbar.action_config(3, text="ACTION_Upgrade_Skills")

        if location == "location_Central":
            print("Now in central")
            app.actionbar.disable_all_options()
            app.actionbar.action_config(1, text="ACTION_View_Achievements")
            app.actionbar.action_config(2, text="ACTION_Save_Game")
            app.actionbar.action_config(3, text="ACTION_Load_Game")

        if location == "location_Tavern":
            print("Now in tavern")
            app.actionbar.disable_all_options()
            app.actionbar.action_config(1, text="ACTION_View_Questboard")

    def enter_dungeon(self):
        app.close_map() # No abusing the map
        self.busy = False
        self.in_combat = False
        print(loc("LOG_Entering_Dungeon"))
        self.location = "location_Dungeon"
        self.dungeon_count = 0
        random_room = random.choice(world.dungeon)
        self.dungeon_move(random_room)
        print("Entering: ", random_room)

    def exit_dungeon(self):
        app.close_map() # No abusing the map
        self.busy = False
        self.in_combat = False
        print(loc("LOG_Exiting_Dungeon"))
        self.hp = self.hp_max # Could change to recharge at central plaza
        self.mp = self.mp_max # 
        print("Dungeon Room Count: ", self.dungeon_count)
        self.dungeon_count = 0 # NOTE: Probably unecessary but sets to 0 anyway
        self.town_move("location_Entrance")

    def dungeon_move(self, room):
        app.close_map() # No abusing the map
        
        if room not in world.dungeon:
            print("ERROR: Wrong dungeon room")
            return
        
        app.actionbar.disable_all_options()

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
                app.actionbar.action_config(1, text="ACTION_Exit_Dungeon", command=self.exit_dungeon)
                app.actionbar.action_config(2, text="ACTION_Return_Dungeon", command=self.enter_dungeon)
                return # Function stops here to not continue into dungeon

        self.dungeon_count = self.dungeon_count + 1

        # The Dungeon
        if room == "location_dungeon_room_1":
            self.busy = True
            app.actionbar.action_config(1, text="ACTION_1")

        if room == "location_dungeon_room_2":
            self.busy = True
            app.actionbar.action_config(1, text="ACTION_2")
        
        if room == "location_dungeon_room_3":
            self.busy = True
            app.actionbar.action_config(1, text="ACTION_3")

        if room == "location_dungeon_room_4":
            self.busy = True
            app.actionbar.action_config(1, text="ACTION_4")

class Encounter():
    def __init__(self, encounter_type):
        
        encounter_parameters = list(world.encounters.get(encounter_type))

        self.hp = encounter_parameters[2]


###############
##### GUI #####
###############

## Pop-Up Interfaces

class Map(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        
        self.title(loc("NAME_Map"))
        self.geometry("700x300")
        self.rowconfigure((1, 2, 3, 4, 5, 6), weight=1)
        self.columnconfigure((1, 2, 3, 4, 5), weight=1)

        ## Navigation Buttons

        # Player should not see this, checks if player is present
        if app.game.player is None: 
            self.label = customtkinter.CTkLabel(self, text=loc("NAME_Map"), font=_font_bold)
            self.label.grid(column=1, columnspan=5, padx=20, pady=20)
            
            self.warning = customtkinter.CTkLabel(self, text=loc("DESC_No_Player_Found"), font=_font_default)
            self.warning.grid(row=1, rowspan=4, column=1, columnspan=5, padx=20, pady=20)

            # print("Player doesn't exist!")
            return
        
        # Player must finish interactions before moving to another location
        if app.game.player.busy is True or app.game.player.in_combat is True:
            self.label = customtkinter.CTkLabel(self, text=loc("NAME_Map"), font=_font_bold)
            self.label.grid(column=1, columnspan=5, padx=20, pady=20)

            if app.game.player.in_combat is True:
                self.warning = customtkinter.CTkLabel(self, text=loc("DESC_Finish_Interaction_Combat"), font=_font_default)
                self.warning.grid(row=1, rowspan=4, column=1, columnspan=5, padx=20, pady=20)
            else:
                self.warning = customtkinter.CTkLabel(self, text=loc("DESC_Finish_Interaction"), font=_font_default)
                self.warning.grid(row=1, rowspan=4, column=1, columnspan=5, padx=20, pady=20)

            # print("Player is busy!")
            return

        if app.game.player.location in world.town: # If player is in town

            # print("Player is in town")

            player_location = loc("DESC_Current_Location") + app.game.locate_player()

            self.label = customtkinter.CTkLabel(self, text=player_location, font=_font_bold)
            self.label.grid(column=1, columnspan=5, padx=20, pady=20)

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

        else: # If player is in the dungeon

            # print("Player in dungeon")

            player_location = loc("DESC_Current_Location") + app.game.locate_player()

            self.label = customtkinter.CTkLabel(self, text=player_location, font=_font_bold)
            self.label.grid(column=1, columnspan=5, padx=20, pady=20)

            # TODO: Random buttons with random commands

            # Template Dungeon Button
            templatebutton = customtkinter.CTkButton(self, text=loc("NAME_Entrance"), command=lambda: self.map_move("location_Entrance", in_dungeon=True))

            # navbutton1 = customtkinter.CTkButton(self, text=loc("NAME_Entrance"), command=lambda: self.map_move("location_Entrance"))
            # navbutton1.grid(row=6, column=3, padx=10, pady=10, sticky="NESW")

            # navbutton2 = customtkinter.CTkButton(self, text=loc("NAME_Main_Hall"), command=lambda: self.map_move("location_Main_Hall"))
            # navbutton2.grid(row=2, column=3, padx=10, pady=10, sticky="NESW")

            # navbutton3 = customtkinter.CTkButton(self, text=loc("NAME_Tavern"), command=lambda: self.map_move("location_Tavern"))
            # navbutton3.grid(row=4, column=1, padx=10, pady=10, sticky="NESW")

            # navbutton4 = customtkinter.CTkButton(self, text=loc("NAME_Equipment_Shop"), command=lambda: self.map_move("location_Shop"))
            # navbutton4.grid(row=4, column=5, padx=10, pady=10, sticky="NESW")

            # navbutton5 = customtkinter.CTkButton(self, text=loc("NAME_Central"), command=lambda: self.map_move("location_Central"))
            # navbutton5.grid(row=4, column=3, padx=10, pady=10, sticky="NESW")

    def map_move(self, new_location, in_dungeon):
        if in_dungeon == False:
            app.game.player.town_move(new_location)
            move = True
        if in_dungeon == True:
            app.game.player.dungeon_move(new_location)
            move = True

        if move is not True:
            print("ERROR: map_move called incorrecty")
            return
        
        # self.destroy()

class Settings(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        
        self.title(loc("NAME_Settings"))
        self.geometry("400x300")

        # language_id = customtkinter.StringVar()
        # No need: Use .configure() to change text

        languages = list(localisation.l_index.keys())

        font_sizes = ["15", "20", "25", "30"]
        
        self.label = customtkinter.CTkLabel(self, text = loc("NAME_Settings"), font=_font_bold)
        self.label.pack(pady=10)

        self.language_select_label = customtkinter.CTkLabel(self, text = loc("NAME_Languages"), font=_font_default)
        self.language_select_label.pack(pady=10)
        self.language_select = customtkinter.CTkOptionMenu(self, values = languages, command = self.change_language)
        self.language_select.set(localisation.l_index_reverse.get(_language))
        self.language_select.pack(pady=10)

        self.font_select_label = customtkinter.CTkLabel(self, text = loc("NAME_Font_Size"), font=_font_default)
        self.font_select_label.pack(pady=10)
        self.font_select = customtkinter.CTkOptionMenu(self, values = font_sizes, command = self.change_font_size)
        self.font_select.set(_font_size)
        self.font_select.pack(pady=10)

        self.restart = None
        
    def change_language(self, new_language):
        language_id = localisation.l_index.get(new_language)
        config.change_setting(language=language_id)
        self.setting_changed()

    def change_font_size(self, new_font_size):
        config.change_setting(font_size=new_font_size)
        self.setting_changed()

    def setting_changed(self):
        if self.restart == None:
            self.restart = customtkinter.CTkLabel(self, text=loc("DESC_Apply_To_Restart"))
            self.restart.pack(pady=10)

#################
## Main Frames ##
#################

class App(customtkinter.CTk):

    # frames = {}
    # current = None
    # bg = ""

    def __init__(self):
        super().__init__()

        # Setting font here as it gives an error when set outside

        global _font_default
        global _font_bold

        _font_default = customtkinter.CTkFont(size=_font_size, weight="normal")
        _font_bold = customtkinter.CTkFont(size=round(_font_size*1.3), weight="bold")

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

        self.actionbar = ActionBar(self.main_frame)
        self.actionbar.grid(row=1, column=1, sticky="NESW")

        self.mainwindow = MainWindow(self.main_frame)
        self.mainwindow.grid(row=0, column=1, sticky="NESW")

        self.sidebar = SideBar(self.main_frame, self)
        self.sidebar.grid(row=0, rowspan=2, column=0, padx=10)

        self.map = None
        self.settings = None

        # Initial Button Configuration
        # TODO: Move check for location, then change

        # self.actionbar.action_config(1)
        # self.actionbar.action_config(2)
        # self.actionbar.action_config(3)
        # self.actionbar.action_config(4)

    def open_map(self):
        if self.map is None or not self.map.winfo_exists():
            self.map = Map(self)  # Create window if its None or destroyed
        else:
            self.map.focus()  # if window exists focus it

    def close_map(self):
        if self.map is None or not self.map.winfo_exists():
            # print("No map to destroy")
            pass
        else:
            self.map.destroy()

    def open_settings(self):
        if self.settings is None or not self.settings.winfo_exists():
            self.settings = Settings(self)  # Create window if its None or destroyed
        else:
            self.settings.focus()  # if window exists focus it

    def start_game(self):
        self.start_frame.pack_forget()
        self.main_frame.pack(expand=True, fill="both")
        self.game.start_game()

class BaseFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
    
    def starting_frame(self, master):

        self.title = customtkinter.CTkLabel(self, text=loc("NAME_Text_Based_Adventure"), font=_font_bold)
        self.title.pack(expand=True, pady=10)
        self.button = customtkinter.CTkButton(self, text=loc("ACTION_Start_Game"), font=_font_bold, command=master.start_game)
        self.button.pack(pady=10)

    def main_frame(self):

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

class SideBar(customtkinter.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")

        self.grid_rowconfigure((1, 2, 3, 4), weight=0)
        self.grid_rowconfigure(5, weight=10)

        self.label = customtkinter.CTkLabel(self, width=10, text=loc("NAME_Menu"), font=_font_bold)
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
        
        self.label = customtkinter.CTkLabel(self, width=10, text=loc("NAME_Main_Window"), font=_font_bold)
        self.label.grid(row=0, column=1)

class ActionBar(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.grid_columnconfigure(1, weight=1)

        self.title = customtkinter.CTkLabel(self, width=10, text=loc("NAME_Action_Bar"), font=_font_bold)
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


        self.local_variables[f"option_{button_row}"].button.configure(text=f"{button_row}. "+loc(text), command=command)
        self.local_variables[f"option_{button_row}"].button.grid(row=0, column=0, padx=10)
        # self.local_variables[f"option_{button_row}"].label.configure(text=loc(label_text))
        # self.local_variables[f"option_{button_row}"].label.grid(row=0, column=1, padx=10)

        self.local_variables[f"option_{button_row}"].grid(row=button_row, pady=10, sticky="EW")

    def disable_all_options(self):
        for x in self.total_options:
            self.disable_option(x)

    def disable_option(self, button_row):
        # print("Disabling option: ", button_row)
        self.local_variables[f"option_{button_row}"].grid_forget()

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



# test = ActionBarOptions.dialogue_option(app.actionbar.options, "Hello World")
# print("Hello World")

# https://felipetesc.github.io/CtkDocs/#/multiple_frames
# https://pythonguides.com/convert-python-file-to-exe-using-pyinstaller/

## This runs the application ##
if __name__ == "__main__":
    global app
    app = App()
    app.mainloop()