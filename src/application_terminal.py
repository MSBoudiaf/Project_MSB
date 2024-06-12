import sys
import os
from application import Application

class terminal (Application):
    project_name="Python Terminal"
    Project_version=""
    def __init__(self):
        #instance attribute
        self.terminal_state = "LOADING"
        self.app_launch()
        

    def app_launch(self):
        self.clear_terminal()
        print(f"Welcome to the {terminal.project_name}")
    
    def app_main_menu(self):
        print("Main Menu \n 1) Start the game \n 2) Options \n 3) Quit Game")
    
    def app_quit(self):
        exit()

    def clear_terminal(slef):

        if (sys.platform == "win32"):
            os.system('cls')

        elif (sys.platform == "darwin"):
            os.system('cls')
        else:
            os.system('cls')
    