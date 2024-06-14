
import os
import sys

# custom modules
from GUI_app import BankApp_GUI
import customtkinter as ctk
from Terminal_app import BankApp


# Global Variables
python_app_instance = None


# Main Function
def main():

    print(f"Application Mode Selection Screen: \n 1-Terminal \n 2-GUI ")

    application_mode = int(input("please select your application mode : "))
    print(application_mode)

    match application_mode:
        case 1:
            app = BankApp()
            app.run()

        case 2:

            Bank_instance = ctk.CTk()
            app = BankApp_GUI(Bank_instance)
            Bank_instance.mainloop()
        case _:
            "this command is unvailiable"


# function to clear terminal


# main guard
if __name__ == "__main__":
    main()
    # main()
