import configparser
#import main
import os.path

# Create settings file if not already created

if os.path.exists("./settings.ini") == None:
    print("No settings found")
    # CREATE OBJECT
    settings_file = configparser.ConfigParser()

    # ADD SECTION
    settings_file.add_section("Settings")
    # ADD SETTINGS TO SECTION
    settings_file.set("Settings", "language", "l_english")
    settings_file.set("Settings", "font_size", "20")

    # SAVE SETTINGS FILE
    with open(r"settings.ini", 'w') as setting:
        settings_file.write(setting)
        setting.flush()
        setting.close()

    print("Config file 'settings.ini' created")

def change_setting(*var1, **var2):

    # CREATE OBJECT
    settings_file = configparser.ConfigParser()

    # ADD SECTION
    settings_file.add_section("Settings")
    # ADD SETTINGS TO SECTION
    settings_file.set("Settings", "language", "l_english")
    settings_file.set("Settings", "font_size", "20")

    # SAVE CONFIG FILE
    with open(r"settings.ini", 'w') as setting:
        settings_file.write(setting)
        setting.flush()
        setting.close()
    
    read_settings = open("settings.ini", "r")
    content = read_settings.read()
    print("Content of the config file are:\n")
    print(content)
    read_settings.flush()
    read_settings.close()

#if "pady" in scaled_kwargs:
#if isinstance(scaled_kwargs["pady"], (int, float)):
#    scaled_kwargs["pady"] = self._apply_widget_scaling(scaled_kwargs["pady"])
#elif isinstance(scaled_kwargs["pady"], tuple):
#    scaled_kwargs["pady"] = tuple([self._apply_widget_scaling(v) for v in scaled_kwargs["pady"]])

#def test(*args, **kwargs):
#    print('arguments are:')
#    for i in args:
#        print(i)
#
#    print('\nkeywords are:')
#    for j in kwargs:
#        print(j)

#if __name__ == "__main__":
#    change_setting()
#
#    # PRINT FILE CONTENT
#
#    read_settings = open("settings.ini", "r")
#    content = read_settings.read()
#    print("Content of the config file are:\n")
#    print(content)
#    read_settings.flush()
#    read_settings.close()