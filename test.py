# Testing code here

option_1 = 100
option_2 = 50

def dialogue_option(button):
    #self.button.grid(row=nrow, column=0, pady=10, sticky="EW")
    #self.button.configure(text=input_text, command=function)
    #update_button = eval(f"option_{button}")
    update_button = globals()[format(f"option_{button}")]
    print(update_button)
    #update_button = self.option_1
    print("Referring to button", update_button)
    update_button = 20
    print("Value is now", update_button)
    globals()[format(f"option_{button}")] = update_button

dialogue_option(2)

print("Value should be", option_2)

# IT WORKS