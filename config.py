import configparser
# import main
import os.path

config = configparser.ConfigParser()

# Create settings file if not already created

if os.path.exists("./settings.ini") == None:
    print("No settings found")

    # Create settings file
    # config = configparser.ConfigParser()

    # Set default settings
    config.add_section("Settings")
    config.set("Settings", "language", "l_english")
    config.set("Settings", "font_size", "20")

    # Save settings file
    with open(r"settings.ini", 'w') as setting:
        config.write(setting)
        setting.flush()
        setting.close()

    print("Config file 'settings.ini' created")

def change_setting(**setting):

    config.read("settings.ini")

    # Checks for which setting to change then changes it

    if "language" in setting:
        # main.language = setting["language"]
        config["Settings"]["language"]=setting["language"]
        config["Settings"].update()

        with open("settings.ini","w") as file_object:
            config.write(file_object)


    if "font_size" in setting:
        # main.font_size = setting["font_size"]
        config["Settings"]["font_size"]=setting["font_size"]
        config["Settings"].update()

        with open("settings.ini","w") as file_object:
            config.write(file_object)
