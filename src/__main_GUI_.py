import tkinter as tk
from tkinter import messagebox
from GUI_app import BankApp_GUI
import customtkinter as ctk
from Terminal_app import BankApp

# Global Variables
python_app_instance = None

# Main Function
def main():
    # Create the main window
    GUI_instance = tk.Tk()
    GUI_instance.title("Application Mode Selection")
    GUI_instance.geometry("300x150")

    # Define callback functions
    def run_terminal_mode():
        GUI_instance.destroy()
        app = BankApp()
        app.run()

    def run_gui_mode():
        GUI_instance.destroy()
        Bank_instance = ctk.CTk()
        app = BankApp_GUI(Bank_instance)
        Bank_instance.mainloop()

    # Add widgets
    label = tk.Label(GUI_instance, text="Please select your application mode:")
    label.pack(pady=10)

    button_terminal = tk.Button(GUI_instance, text="Terminal", command=run_terminal_mode)
    button_terminal.pack(pady=5)

    button_gui = tk.Button(GUI_instance, text="GUI", command=run_gui_mode)
    button_gui.pack(pady=5)

    # Run the Tkinter event loop
    GUI_instance.mainloop()

# main guard
if __name__ == "__main__":
    main()
