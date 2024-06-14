import customtkinter as ctk
from tkinter import messagebox
import sqlite3

class BankAccount_GUI:
    def __init__(self, account_number, account_holder, pin, balance=0):
        if not isinstance(account_holder, str) or not account_holder.isalpha():
            raise ValueError("Le titulaire du compte doit être un nom valide (sans chiffres).")
        if not isinstance(pin, int):
            raise ValueError("Le PIN doit être un entier.")
        self.account_number = account_number
        self.account_holder = account_holder
        self.pin = pin
        self.balance = balance

    def check_pin(self, pin):
        return self.pin == pin
    #fonction dépot
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.update_balance_in_db()
            return f"Déposé {amount}. Nouveau solde est {self.balance}."
        else:
            return "Le montant du dépôt doit être positif."
    #fonction retrait
    def withdraw(self, amount):
        if amount > 0:
            if self.balance >= amount:
                self.balance -= amount
                self.update_balance_in_db()
                return f"Retiré {amount}. Nouveau solde est {self.balance}."
            else:
                return "Solde insuffisant."
        else:
            return "Le montant du retrait doit être positif."
    #Fonction Tranférer (Virement)
    def transfer(self, target_account, amount):
        if amount > 0:
            if self.balance >= amount:
                self.balance -= amount
                target_account.balance += amount
                self.update_balance_in_db()
                target_account.update_balance_in_db()
                return f"Transféré {amount} au compte {target_account.account_number}. Nouveau solde est {self.balance}."
            else:
                return "Solde insuffisant."
        else:
            return "Le montant du transfert doit être positif."

    def get_balance(self):
        return self.balance
    #affichage du détails des comptes
    def display_account_details(self):
        return f"Numéro de compte : {self.account_number}\nTitulaire du compte : {self.account_holder}\nSolde : {self.balance}"

    def update_balance_in_db(self):
        with sqlite3.connect('bank.db') as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE accounts SET balance = ? WHERE account_number = ?", (self.balance, self.account_number))
            conn.commit()
    # l'implemtation grafique de l'application
class BankApp_GUI:
    def __init__(self, GUI_instance):
        self.GUI_instance = GUI_instance
        self.GUI_instance.title("Application Bancaire")
        self.accounts = {}

        self.init_db()
        self.load_accounts()

        self.main_frame = ctk.CTkFrame(self.GUI_instance)
        self.main_frame.pack(pady=20)

        self.title_label = ctk.CTkLabel(self.main_frame, text="Application Bancaire", font=('Arial', 16))
        self.title_label.grid(row=0, column=0, columnspan=10)

        self.create_widgets()

    def init_db(self):
        with sqlite3.connect('bank.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
                                account_number TEXT PRIMARY KEY,
                                account_holder TEXT,
                                pin INTEGER,
                                balance REAL)''')
            conn.commit()

    def load_accounts(self):
        with sqlite3.connect('bank.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM accounts")
            rows = cursor.fetchall()
            for row in rows:
                account_number, account_holder, pin, balance = row
                pin = int(pin)  # Assurez-vous que le pin est un entier
                
                # Vérifiez que account_holder est une chaîne sans chiffres
                if isinstance(account_holder, str) and account_holder.isalpha():
                    self.accounts[account_number] = BankAccount_GUI(account_number, account_holder, pin, balance)
                else:
                    messagebox.showerror("Erreur de chargement", f"Le titulaire du compte pour le numéro de compte {account_number} n'est pas valide. Le compte ne sera pas chargé.")

    def create_widgets(self):
        # Creation des comptes
        self.account_number_label = ctk.CTkLabel(self.main_frame, text="Numéro de compte :")
        self.account_number_label.grid(row=1, column=0, pady=5)
        self.account_number_entry = ctk.CTkEntry(self.main_frame)
        self.account_number_entry.grid(row=1, column=1, pady=5)

        self.account_holder_label = ctk.CTkLabel(self.main_frame, text="Titulaire du compte :")
        self.account_holder_label.grid(row=2, column=0, pady=5)
        self.account_holder_entry = ctk.CTkEntry(self.main_frame)
        self.account_holder_entry.grid(row=2, column=1, pady=5)

        self.pin_label = ctk.CTkLabel(self.main_frame, text="PIN :")
        self.pin_label.grid(row=3, column=0, pady=5)
        self.pin_entry = ctk.CTkEntry(self.main_frame, show="*")
        self.pin_entry.grid(row=3, column=1, pady=5)

        self.create_account_button = ctk.CTkButton(self.main_frame, text="Créer un compte", command=self.create_account)
        self.create_account_button.grid(row=4, column=0, columnspan=2, pady=5)

        # Dépot
        self.deposit_label = ctk.CTkLabel(self.main_frame, text="Montant du dépôt :")
        self.deposit_label.grid(row=5, column=0, pady=5)
        self.deposit_entry = ctk.CTkEntry(self.main_frame)
        self.deposit_entry.grid(row=5, column=1, pady=5)

        self.deposit_pin_label = ctk.CTkLabel(self.main_frame, text="PIN :")
        self.deposit_pin_label.grid(row=6, column=0, pady=5)
        self.deposit_pin_entry = ctk.CTkEntry(self.main_frame, show="*")
        self.deposit_pin_entry.grid(row=6, column=1, pady=5)

        self.deposit_button = ctk.CTkButton(self.main_frame, text="Déposer", command=self.deposit)
        self.deposit_button.grid(row=7, column=0, columnspan=2, pady=5)

        # retrait
        self.withdraw_label = ctk.CTkLabel(self.main_frame, text="Montant du retrait :")
        self.withdraw_label.grid(row=8, column=0, pady=5)
        self.withdraw_entry = ctk.CTkEntry(self.main_frame)
        self.withdraw_entry.grid(row=8, column=1, pady=5)

        self.withdraw_pin_label = ctk.CTkLabel(self.main_frame, text="PIN :")
        self.withdraw_pin_label.grid(row=9, column=0, pady=5)
        self.withdraw_pin_entry = ctk.CTkEntry(self.main_frame, show="*")
        self.withdraw_pin_entry.grid(row=9, column=1, pady=5)

        self.withdraw_button = ctk.CTkButton(self.main_frame, text="Retirer", command=self.withdraw)
        self.withdraw_button.grid(row=10, column=0, columnspan=2, pady=5)

        # transfert
        self.transfer_to_label = ctk.CTkLabel(self.main_frame, text="Transférer vers le compte :")
        self.transfer_to_label.grid(row=11, column=0, pady=5)
        self.transfer_to_entry = ctk.CTkEntry(self.main_frame)
        self.transfer_to_entry.grid(row=11, column=1, pady=5)

        self.transfer_amount_label = ctk.CTkLabel(self.main_frame, text="Montant du transfert :")
        self.transfer_amount_label.grid(row=12, column=0, pady=5)
        self.transfer_amount_entry = ctk.CTkEntry(self.main_frame)
        self.transfer_amount_entry.grid(row=12, column=1, pady=5)

        self.transfer_pin_label = ctk.CTkLabel(self.main_frame, text="PIN :")
        self.transfer_pin_label.grid(row=13, column=0, pady=5)
        self.transfer_pin_entry = ctk.CTkEntry(self.main_frame, show="*")
        self.transfer_pin_entry.grid(row=13, column=1, pady=5)

        self.transfer_button = ctk.CTkButton(self.main_frame, text="Transférer", command=self.transfer)
        self.transfer_button.grid(row=14, column=0, columnspan=2, pady=5)

        # vérification du montant restant
        self.balance_pin_label = ctk.CTkLabel(self.main_frame, text="PIN :")
        self.balance_pin_label.grid(row=15, column=0, pady=5)
        self.balance_pin_entry = ctk.CTkEntry(self.main_frame, show="*")
        self.balance_pin_entry.grid(row=15, column=1, pady=5)

        self.balance_button = ctk.CTkButton(self.main_frame, text="Vérifier le solde", command=self.check_balance)
        self.balance_button.grid(row=16, column=0, columnspan=2, pady=5)

        # affichage des détails des comptes
        self.display_pin_label = ctk.CTkLabel(self.main_frame, text="PIN :")
        self.display_pin_label.grid(row=17, column=0, pady=5)
        self.display_pin_entry = ctk.CTkEntry(self.main_frame, show="*")
        self.display_pin_entry.grid(row=17, column=1, pady=5)

        self.display_button = ctk.CTkButton(self.main_frame, text="Afficher les détails du compte", command=self.display_account_details)
        self.display_button.grid(row=18, column=0, columnspan=2, pady=5)

    def create_account(self):
        account_number = self.account_number_entry.get()
        account_holder = self.account_holder_entry.get()
        try:
            pin = int(self.pin_entry.get())
        except ValueError:
            messagebox.showerror("Erreur", "Le PIN doit être un entier.")
            return

        if account_number in self.accounts:
            messagebox.showerror("Erreur", "Ce numéro de compte existe déjà.")
            return

        if account_number and account_holder and pin:
            try:
                new_account = BankAccount_GUI(account_number, account_holder, pin)
                self.accounts[account_number] = new_account

                with sqlite3.connect('bank.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO accounts (account_number, account_holder, pin, balance) VALUES (?, ?, ?, ?)",
                                   (account_number, account_holder, pin, 0))
                    conn.commit()

                messagebox.showinfo("Succès", "Compte créé avec succès.")
            except ValueError as ve:
                messagebox.showerror("Erreur", str(ve))
        else:
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")

        self.clear_entries()  # Efface les champs après la création du compte

    def deposit(self):
        account_number = self.account_number_entry.get()
        try:
            amount = float(self.deposit_entry.get())
            pin = int(self.deposit_pin_entry.get())
        except ValueError:
            messagebox.showerror("Erreur", "Le montant du dépôt doit être un nombre et le PIN doit être un entier.")
            return

        account = self.accounts.get(account_number)
        if account and account.check_pin(pin):
            result = account.deposit(amount)
            messagebox.showinfo("Information", result)
            self.clear_entries()  # Efface les champs après dépôt réussi
        else:
            messagebox.showerror("Erreur", "Numéro de compte ou PIN incorrect.")

    def withdraw(self):
        account_number = self.account_number_entry.get()
        try:
            amount = float(self.withdraw_entry.get())
            pin = int(self.withdraw_pin_entry.get())
        except ValueError:
            messagebox.showerror("Erreur", "Le montant du retrait doit être un nombre et le PIN doit être un entier.")
            return

        account = self.accounts.get(account_number)
        if account and account.check_pin(pin):
            result = account.withdraw(amount)
            messagebox.showinfo("Information", result)
            self.clear_entries()  # Efface les champs après retrait réussi
        else:
            messagebox.showerror("Erreur", "Numéro de compte ou PIN incorrect.")

    def transfer(self):
        account_number = self.account_number_entry.get()
        target_account_number = self.transfer_to_entry.get()
        try:
            amount = float(self.transfer_amount_entry.get())
            pin = int(self.transfer_pin_entry.get())
        except ValueError:
            messagebox.showerror("Erreur", "Le montant du transfert doit être un nombre et le PIN doit être un entier.")
            return

        account = self.accounts.get(account_number)
        target_account = self.accounts.get(target_account_number)
        if account and account.check_pin(pin) and target_account:
            result = account.transfer(target_account, amount)
            messagebox.showinfo("Information", result)
            self.clear_entries()  # Efface les champs après transfert réussi
        else:
            messagebox.showerror("Erreur", "Numéro de compte ou PIN incorrect.")

    def check_balance(self):
        account_number = self.account_number_entry.get()
        try:
            pin = int(self.balance_pin_entry.get())
        except ValueError:
            messagebox.showerror("Erreur", "Le PIN doit être un entier.")
            return

        account = self.accounts.get(account_number)
        if account and account.check_pin(pin):
            balance = account.get_balance()
            messagebox.showinfo("Solde", f"Votre solde est {balance}.")
        else:
            messagebox.showerror("Erreur", "Numéro de compte ou PIN incorrect.")

    def display_account_details(self):
        account_number = self.account_number_entry.get()
        try:
            pin = int(self.display_pin_entry.get())
        except ValueError:
            messagebox.showerror("Erreur", "Le PIN doit être un entier.")
            return

        account = self.accounts.get(account_number)
        if account and account.check_pin(pin):
            details = account.display_account_details()
            messagebox.showinfo("Détails du compte", details)
        else:
            messagebox.showerror("Erreur", "Numéro de compte ou PIN incorrect.")

        self.clear_entries()  # Efface les champs après affichage des détails
        
    def clear_entries(self):
        self.account_number_entry.delete(0, 'end')
        self.account_holder_entry.delete(0, 'end')
        self.pin_entry.delete(0, 'end')
        self.deposit_entry.delete(0, 'end')
        self.deposit_pin_entry.delete(0, 'end')
        self.withdraw_entry.delete(0, 'end')
        self.withdraw_pin_entry.delete(0, 'end')
        self.transfer_to_entry.delete(0, 'end')
        self.transfer_amount_entry.delete(0, 'end')
        self.transfer_pin_entry.delete(0, 'end')
        self.balance_pin_entry.delete(0, 'end')
        self.display_pin_entry.delete(0, 'end')

# Exemple d'utilisation
if __name__ == "__main__":
    root = ctk.CTk()
    bank_app = BankApp_GUI(root)
    root.mainloop()
