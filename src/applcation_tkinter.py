
from application import Application

import customtkinter

class GUIApplication (Application, customtkinter.CTk):
    

    def __init__(self):
        

        self.app_launch()
    
    

    def app_launch (self):
        super().__init__()
        self.geometry("1000x800")
        self.title ("python Application")

        self.option_window=None
        
        self.button_options = customtkinter.CTkButton(self, text="Options", command=self.button_app_options)
        self.button_options.grid(row=0, column=0, padx=10, pady=15)


        self.button_quit = customtkinter.CTkButton(self,text="Quit Application", command=self.button_app_quit)
        self.button_quit.grid(row=0, column=1, padx=15, pady=15)

        self.combobox_charachter=customtkinter.CTkComboBox(self, values=["haven", "Jonesy","peely"], command=self.button_select_character)
        self.combobox_charachter.grid (row=0, column=2)
        
    
    def app_main_menu (self):...

    
    def app_quit (self):
        exit()
    
    def button_app_quit(self):
        self.app_quit()

    def button_app_options(self):
        if self.option_window is None or not self.option_window.winfo_exists():
            self.option_window =GUIOptionWindows()
            self.option_window.focus()
        else:
            self.option_windows.focus()

    def button_select_character(self):
        pass

    


class GUIOptionWindows(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry("400x400")
        self.title("Python App - Options")

        self.label=customtkinter.CTkLabel(self, text="top level Window")
        self.label.grid(row=0,column=1)




if __name__=="__main__":
    guiapp_test_instance=GUIApplication()
    guiapp_test_instance.mainloop()
