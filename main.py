#import time
#import tkinter
from typing import Union, Callable
import customtkinter
import localisation
import config
import configparser
import gameworld

# TODO: Add to settings menu
customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("green")

def read_config():
    config_read = configparser.ConfigParser()
    config_read.read('settings.ini')
    return config_read

if __name__ == "__main__":
    global language
    global font_size
    global settings
    settings = read_config()
    language = str(settings["Settings"]["language"])
    font_size = int(settings["Settings"]["font_size"])

def placeholder_function():
    print(loc("TEST_Hello_World"))

######################
#### Localisation ####
######################

def loc(loc_id):
    if language == "l_english":
        text = localisation.l_english.get(loc_id)
    if language == "l_french":
        text = localisation.l_french.get(loc_id)
    
    if text == None:
        text = loc_id

    #text = "Max is a Noob"

    return text

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
            return loc(gameworld.locations.get(self.player.location))
    
    def move_player(self, location_id):

        if self.player is None:
            print(loc("LOG_Player_Not_Found"))
        else:
            self.player.move(location_id)

class Player():
    def __init__(self):
        self.state = True # Alive
        self.hp = 10
        self.mp = 10
        self.location = "location_Central"
    
    def town_move(self, location):
        print(loc("LOG_Moving_Player"), location)
        self.location = location

    def enter_dungeon(self):
        print(loc("LOG_Entering_Dungeon"))
        self.location = "location_Dungeon"

###############
##### GUI #####
###############

## Pop-Up Interfaces

class Map(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        
        self.title(loc("NAME_Map"))
        self.geometry("400x300")
        self.rowconfigure((1, 2, 3, 4, 5, 6), weight=1)
        self.columnconfigure((1, 2, 3, 4, 5), weight=1)

        # Navigation Buttons
        if app.game.player is None:
            self.label = customtkinter.CTkLabel(self, text=loc("NAME_Map"), font=font_bold)
            self.label.grid(column=1, columnspan=5, padx=20, pady=20)
            
            self.warning = customtkinter.CTkLabel(self, text=loc("DESC_No_Player_Found"), font=font_default)
            self.warning.grid(row=1, rowspan=4, column=1, columnspan=5, padx=20, pady=20)

            #print("Player doesn't exist!")

        else:

            player_location = loc("DESC_Current_Location") + app.game.locate_player()

            self.label = customtkinter.CTkLabel(self, text=player_location, font=font_bold)
            self.label.grid(column=1, columnspan=5, padx=20, pady=20)

            self.navbutton1 = customtkinter.CTkButton(self, text=loc("NAME_Entrance"), command=lambda: self.map_move("location_Entrance"))
            self.navbutton1.grid(row=6, column=3, padx=10, pady=10, sticky="NESW")

            self.navbutton2 = customtkinter.CTkButton(self, text=loc("NAME_Main_Hall"), command=lambda: self.map_move("location_Main_Hall"))
            self.navbutton2.grid(row=2, column=3, padx=10, pady=10, sticky="NESW")

            self.navbutton3 = customtkinter.CTkButton(self, text=loc("NAME_Tavern"), command=lambda: self.map_move("location_Tavern"))
            self.navbutton3.grid(row=4, column=1, padx=10, pady=10, sticky="NESW")

            self.navbutton4 = customtkinter.CTkButton(self, text=loc("NAME_Equipment_Shop"), command=lambda: self.map_move("location_Shop"))
            self.navbutton4.grid(row=4, column=5, padx=10, pady=10, sticky="NESW")

            self.navbutton5 = customtkinter.CTkButton(self, text=loc("NAME_Central"), command=lambda: self.map_move("location_Central"))
            self.navbutton5.grid(row=4, column=3, padx=10, pady=10, sticky="NESW")

    def map_move(self, new_location):
        app.game.player.town_move(new_location)
        self.destroy()

class Settings(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        
        self.title(loc("NAME_Settings"))
        self.geometry("400x300")

        #language_id = customtkinter.StringVar()

        languages = list(localisation.l_index.keys())
        
        self.label = customtkinter.CTkLabel(self, text = loc("NAME_Settings"), font=font_bold)
        self.label.pack(pady=10)
        self.language_select = customtkinter.CTkOptionMenu(self, values = languages, command = self.change_language, state="r")
        self.language_select.set(localisation.l_index_reverse.get(language))
        self.language_select.pack(pady=10)

        self.restart = None
        
    def change_language(self, new_language):
        language_id = localisation.l_index.get(new_language)
        config.change_setting(language=language_id)
        self.setting_changed()

    def setting_changed(self):
        if self.restart == None:
            self.restart = customtkinter.CTkLabel(self, text=loc("DESC_Apply_To_Restart"))
            self.restart.pack(pady=10)

## Main Frames

class App(customtkinter.CTk):

    #frames = {}
    #current = None
    #bg = ""

    def __init__(self):
        super().__init__()

        # Setting font here as it gives an error when set outside

        global font_default
        global font_bold

        font_default = customtkinter.CTkFont(size=font_size, weight="normal")
        font_bold = customtkinter.CTkFont(size=font_size, weight="bold")

        self.game = Game()

        self.geometry("1000x500")
        self.title(loc("NAME_Text_Based_Adventure"))

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.actionbar = ActionBar(self)
        self.actionbar.grid(row=1, column=1, sticky="NESW")

        self.mainwindow = MainWindow(self)
        self.mainwindow.grid(row=0, column=1, sticky="NESW")

        self.sidebar = SideBar(self)
        self.sidebar.grid(row=0, rowspan=2, column=0, padx=10)

        self.map = None
        self.settings = None

        # Initial Button Configuration
        # TODO: Move check for location, then change

        self.actionbar.action_config(1)
        self.actionbar.action_config(2)
        self.actionbar.action_config(3)
        self.actionbar.action_config(4)

    def open_map(self):
        if self.map is None or not self.map.winfo_exists():
            self.map = Map(self)  # Create window if its None or destroyed
        else:
            self.map.focus()  # if window exists focus it

    def open_settings(self):
        if self.settings is None or not self.settings.winfo_exists():
            self.settings = Settings(self)  # Create window if its None or destroyed
        else:
            self.settings.focus()  # if window exists focus it


class SideBar(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.grid_rowconfigure((1, 2, 3, 4), weight=0)
        self.grid_rowconfigure(5, weight=10)

        self.label = customtkinter.CTkLabel(self, width=10, text=loc("NAME_Menu"), font=font_bold)
        self.label.grid(row=0, column=0, padx=10, sticky="N")

        self.open_settings = customtkinter.CTkButton(master=self, width=10, text=loc("DESC_Open_Settings"), command=master.open_settings)
        self.open_settings.grid(row=1, column=0, pady=10)
        self.open_map = customtkinter.CTkButton(master=self, width=10, text=loc("DESC_Open_Map"), command=master.open_map)
        self.open_map.grid(row=2, column=0, pady=10)
        self.test_game = customtkinter.CTkButton(master=self, width=10, text=loc("DESC_Test_Game"), command=master.game.start_game)
        self.test_game.grid(row=3, column=0, pady=10)


class MainWindow(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.grid_columnconfigure(1, weight=1)
        
        self.label = customtkinter.CTkLabel(self, width=10, text=loc("NAME_Main_Window"), font=font_bold)
        self.label.grid(row=0, column=1)


class ActionBar(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.grid_columnconfigure(1, weight=1)

        self.title = customtkinter.CTkLabel(self, width=10, text=loc("NAME_Action_Bar"), font=font_bold)
        self.title.grid(row=0, column=1, padx=10, pady=10, sticky="NSEW")
        self.options = customtkinter.CTkFrame(master=self, fg_color="transparent")
        self.options.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky="W")

        # Options Pre-Initialise

        for x in range(1, 4):
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
        #print(self.local_variables)

        # TODO: Make sure to set .grid later 

    # Configures initialised buttons
    # TODO: Use dictionary arguments **parameters
    #def action_config(self, button_row, input_text, function):
    #    update_button = self.local_variables[f"option_{button_row}"]    # TODO Replace update_button with locals(self)[format(f"option_{button}")] as Python variables are stupid
    #    update_button.configure(text=input_text, command=function)      # format() is not needed: format(f"option_{button_row}")
    #    update_button.grid(row=button_row)
    #    locals(self)[f"option_{button_row}"] = update_button # TODO Refer to previous TODO
    #    update_button.grid_forget()

    def action_config(self,
                      button_row,
                      button_text: str = "DESC_Placeholder_Button_Text",
                      label_text: str = "DESC_Placeholder_Label_Text",
                      command: Union[Callable[[], None], None] = lambda: placeholder_function()):
        
        # Old Code
        #if "text" in parameters: #TODO Change to button reference
        #    self.local_variables[f"option_{button_row}"].configure(text=parameters["text"])
        #if "command" in parameters:
        #    self.local_variables[f"option_{button_row}"].configure(command=lambda: parameters["command"])


        self.local_variables[f"option_{button_row}"].button.configure(text=loc(button_text), command=command)
        self.local_variables[f"option_{button_row}"].button.grid(row=0, column=0, padx=10)
        self.local_variables[f"option_{button_row}"].label.configure(text=loc(label_text))
        self.local_variables[f"option_{button_row}"].label.grid(row=0, column=1, padx=10)

        self.local_variables[f"option_{button_row}"].grid(row=button_row, pady=10, sticky="EW")

    def disable_option(self, button_row):
        self.local_variables[f"option_{button_row}"].grid_forget()

    ## Old Code for dynamic number of options ##

    #def dialogue_option(self, input_text, function, nrow):
    #
    #    rows = customtkinter.CTkFrame(master=self.options, fg_color="transparent")
    #    #rows = tkinter.Frame(master=self.options)
    #    rows.grid(row=nrow, column=0, pady=10, sticky="EW")
    #
    #    options = customtkinter.CTkButton(master=rows, width=10, text=input_text, command=function)
    #    options.grid(row=nrow, column=0, padx=10)
    #    label = customtkinter.CTkLabel(master=rows, width=10, text=input_text)
    #    label.grid(row=nrow, column=1, padx=10)

    # Example of getting dynamic buttons
    #def get(self):
    #    checked_checkboxes = []
    #    for checkbox in self.checkboxes:
    #        if checkbox.get() == 1:
    #            checked_checkboxes.append(checkbox.cget("text"))
    #    return checked_checkboxes
    #
    #def reset_dialogue(self):
    #  
    #    for rows in self.options:
    #        #rows.destroy()
    #        rows.grid.forget()


#class ActionBarOptions(customtkinter.CTkFrame):
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



#test = ActionBarOptions.dialogue_option(app.actionbar.options, "Hello World")
#print("Hello World")

#https://felipetesc.github.io/CtkDocs/#/multiple_frames

## This runs the application ##
if __name__ == "__main__":
    app = App()
    app.mainloop()