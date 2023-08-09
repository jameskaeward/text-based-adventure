import configparser
import main
import os.path

config_setting = configparser.ConfigParser()

# Create settings file if not already created

if os.path.exists("./settings.ini") == None:
    print("No settings found")

    # Create settings file
    #config_setting = configparser.ConfigParser()

    # Set default settings
    config_setting.add_section("Settings")
    config_setting.set("Settings", "language", "l_english")
    config_setting.set("Settings", "font_size", "20")

    # Save settings file
    with open(r"settings.ini", 'w') as setting:
        config_setting.write(setting)
        setting.flush()
        setting.close()

    print("Config file 'settings.ini' created")

def change_setting(**setting):

    #read_settings = open("settings.ini", "r")
    #content = read_settings.read()
    #print("Content of the config file are:\n")
    #print(content)
    #read_settings.flush()
    #read_settings.close()

    config_setting.read("settings.ini")

    #settings = open("settings.ini", "w")

    if "language" in setting:
        #print(setting["language"])
        main.language = setting["language"]
        #print(main.language)
        #config_setting.set("Settings", "language", setting["language"])
        config_setting["Settings"]["language"]=setting["language"]
        config_setting["Settings"].update()

        with open("configurations.ini","w") as file_object:
            config_setting.write(file_object)
    
    # TODO This function overwrite old settings

    #config_setting.write(settings)
    #settings.flush()
    #settings.close()

#import configparser
#
# CREATE OBJECT
#config_file = configparser.ConfigParser()
#
# READ CONFIG FILE
#config_file.read("configurations.ini")
# 
# UPDATE A FIELD VALUE
#config_file["Logger"]["LogLevel"]="Debug"
# 
# ADD A NEW FIELD UNDER A SECTION
#config_file["Logger"].update({"Format":"(message)"})
# 
# SAVE THE SETTINGS TO THE FILE
#with open("configurations.ini","w") as file_object:
#    config_file.write(file_object)
# 
# DISPLAY UPDATED SAVED SETTINGS
#print("Config file 'configurations.ini' is updated")
#print("Updated file settings are:\n")
#file=open("configurations.ini","r")
#settings=file.read()
#print(settings)

new_language = "l_english"
change_setting(language = new_language)

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