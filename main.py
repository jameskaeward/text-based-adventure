#import time
import tkinter
#from typing import Optional, Tuple, Union
import customtkinter
import localisation
import config
import configparser

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("green")

def read_config():
    config_read = configparser.ConfigParser()
    config_read.read('settings.ini')
    return config_read

settings = read_config()

language = str(settings["Settings"]["language"])
font_size = int(settings["Settings"]["font_size"])

def test_function():
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
            return self.player.location
    
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
        self.location = loc("NAME_Entrance")
    
    def move(self):
        print(loc("LOG_Moving_Player"))


###############
##### GUI #####
###############

## Pop-Up Interfaces

class Map(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        
        self.title(loc("NAME_Map"))
        self.geometry("400x300")
        self.rowconfigure((1, 2, 3, 4, 5), weight=1)
        self.columnconfigure((1, 2, 3, 4, 5), weight=1)

        # Navigation Buttons
        if master.game.player is None:
            self.label = customtkinter.CTkLabel(self, text=loc("NAME_Map"), font=font_bold)
            self.label.grid(column=1, columnspan=5, padx=20, pady=20)
            
            self.warning = customtkinter.CTkLabel(self, text=loc("DESC_No_Player_Found"), font=font_default)
            self.warning.grid(row=1, rowspan=4, column=1, columnspan=5, padx=20, pady=20)

            #print("Player doesn't exist!")

        else:

            player_location = loc("DESC_Current_Location") + master.game.locate_player()

            self.label = customtkinter.CTkLabel(self, text=player_location, font=font_bold)
            self.label.grid(column=1, columnspan=5, padx=20, pady=20)

            #self.navbutton1 = customtkinter.CTkButton(self, text="1", command=master.game.player.move)

class Settings(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        
        self.title(loc("NAME_Settings"))
        self.geometry("400x300")

        #language_id = customtkinter.StringVar()

        languages = list(localisation.l_index.keys())
        #print(languages)
        #self.language_select = customtkinter.CTkOptionMenu(self, values = [loc("NAME_English"), loc("NAME_French")], command = self.change_language, state="r")
        self.label = customtkinter.CTkLabel(self, text = "NAME_Settings")
        self.label.pack(pady=10)
        self.language_select = customtkinter.CTkOptionMenu(self, values = languages, command = self.change_language, state="r")
        self.language_select.pack(pady=10)
        
    def change_language(self, new_language):
        language_id = localisation.l_index.get(new_language)
        config.change_setting(language=language_id)
        
#def combobox_callback(choice):
#    print("combobox dropdown clicked:", choice)
#
#combobox_var = customtkinter.StringVar(value="option 2")
#combobox = customtkinter.CTkComboBox(app, values=["option 1", "option 2"],
#                                     command=combobox_callback, variable=combobox_var)
#combobox_var.set("option 2")
#
#
#def combobox_callback(choice):
#    print("combobox dropdown clicked:", choice)
#
#combobox = customtkinter.CTkComboBox(app, values=["option 1", "option 2"],
#                                     command=combobox_callback)
#combobox.set("option 2")

## Main Frames

class App(customtkinter.CTk):

    #frames = {}
    #current = None
    #bg = ""

    def __init__(self):
        super().__init__()

        #self.font_default = customtkinter.CTkFont(size=font_size+20, weight="normal")
        #self.font_bold = customtkinter.CTkFont(size=font_size+20, weight="bold")

        # Setting font here as it gives an error when set outside

        global font_default
        global font_bold

        font_default = customtkinter.CTkFont(size=font_size, weight="normal")
        font_bold = customtkinter.CTkFont(size=font_size, weight="bold")

        self.game = Game()

        self.geometry("1000x500")
        self.title(loc("NAME_Text_Based_Adventure"))

        #self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.actionbar = ActionBar(self)
        self.actionbar.grid(row=1, column=1, sticky="NESW")

        self.mainwindow = MainWindow(self)
        self.mainwindow.grid(row=0, column=1, sticky="NESW")

        self.sidebar = SideBar(self)
        self.sidebar.grid(row=0, column=0, padx=10)

        self.map = None
        self.settings = None

        #self.test_button = customtkinter.CTkButton(master=self, width=10, text= "Test", command=self.actionbar.dialogue_option("Test", test_function))
        #self.test_button.grid(row=0, column=0)

        self.actionbar.dialogue_option(loc("NAME_Test"), test_function, 0)
        self.actionbar.dialogue_option(loc("NAME_Test"), test_function, 1)
        self.actionbar.dialogue_option(loc("NAME_Test"), test_function, 2)
        self.actionbar.dialogue_option(loc("NAME_Test"), test_function, 3)

        #self.open_map = customtkinter.CTkButton(master=self, width=10, text="Test Map", command=self.open_map)
        #self.open_map.grid(row=0, column=0)
        #self.test_game = customtkinter.CTkButton(master=self, width=10, text="Test Game", command=self.game.start_game)
        #self.test_game.grid(row=1, column=0)

    def open_map(self):
        if self.map is None or not self.map.winfo_exists():
            self.map = Map(self)  # create window if its None or destroyed
        else:
            self.map.focus()  # if window exists focus it

    def open_settings(self):
        if self.settings is None or not self.settings.winfo_exists():
            self.settings = Settings(self)  # create window if its None or destroyed
        else:
            self.settings.focus()  # if window exists focus it


class SideBar(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.grid_rowconfigure(3, weight=1)

        self.label = customtkinter.CTkLabel(self, width=10, text=loc("NAME_Menu"), font=font_bold)
        self.label.grid(row=0, column=0, padx=20)

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
        self.options = customtkinter.CTkFrame(master=self)
        self.options.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky="W")

        #num_dialogue_options = 0

    def dialogue_option(self, input_text, function, nrow):

        rows = customtkinter.CTkFrame(master=self.options, fg_color="transparent")
        #rows = tkinter.Frame(master=self.options)
        rows.grid(row=nrow, column=0, pady=10, sticky="EW")

        options = customtkinter.CTkButton(master=rows, width=10, text=input_text, command=function)
        options.grid(row=nrow, column=0, padx=10)
        label = customtkinter.CTkLabel(master=rows, width=10, text=input_text)
        label.grid(row=nrow, column=1, padx=10)

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

# Running Code

if __name__ == "__main__":
    app = App()
    app.mainloop()