
import os
import sys

#custom modules
from  application_terminal import terminal
from application_panda3d import Panda3DApplication
from applcation_tkinter import GUIApplication

#Main Function
def main (application_mode):
    
    match application_mode: 
        case "Terminal":
         terminal_instance=terminal()
         

        case "Panda_3D":
         panda3d_instance = Panda3DApplication()
         panda3d_instance.run()
        case "custom tkinter":
            customtkinter_instance= GUIApplication()
        case _:
         "this command us unvailiable"


#function to clear terminal 



#main guard
if __name__=="__main__":
    main("Panda_3D")
