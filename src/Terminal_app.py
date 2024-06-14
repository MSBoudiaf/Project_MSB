import sqlite3
import getpass

class BankAccount:
    def __init__(self, account_number, account_holder, pin, balance=0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.pin = pin
        self.balance = balance

    def check_pin(self, pin):
        return self.pin == pin

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.update_balance_in_db()
            return f"Déposé {amount}. Nouveau solde est {self.balance}."
        else:
            return "Le montant du dépôt doit être positif."

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

    def display_account_details(self):
        return f"Numéro de compte : {self.account_number}\nTitulaire du compte : {self.account_holder}\nSolde : {self.balance}"

    def update_balance_in_db(self):
        with sqlite3.connect('bank.db') as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE accounts SET balance = ? WHERE account_number = ?", (self.balance, self.account_number))
            conn.commit()

class BankApp:
    def __init__(self):
        self.accounts = {}
        self.init_db()
        self.load_accounts()

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
                self.accounts[account_number] = BankAccount(account_number, account_holder, pin, balance)

    def create_account(self):
        print("Création d'un compte.")
        account_number = input("Entrez le numéro de compte : ")
        account_holder = input("Entrez le titulaire du compte : ")
        try:
            pin = int(getpass.getpass("Entrez le PIN : "))
        except ValueError:
            print("Erreur : Le PIN doit être un entier.")
            return

        if account_number and self.validate_account_holder(account_holder) and pin:
            if account_number not in self.accounts:
                new_account = BankAccount(account_number, account_holder, pin)
                self.accounts[account_number] = new_account
                self.save_account(new_account)
                print("Compte créé avec succès.")
            else:
                print("Erreur : Le compte existe déjà.")
        else:
            print("Erreur : Veuillez saisir tous les détails requis.")

    def validate_account_holder(self, account_holder):
        # Vérifie que le titulaire du compte ne contient que des caractères alphabétiques et pas de chiffres
        return all(char.isalpha() or char.isspace() for char in account_holder)

    def deposit(self):
        print("Dépôt sur un compte.")
        account_number = input("Entrez le numéro de compte : ")
        pin = int(getpass.getpass("Entrez le PIN : "))
        if account_number in self.accounts:
            if self.accounts[account_number].check_pin(pin):
                try:
                    amount = float(input("Entrez le montant à déposer : "))
                except ValueError:
                    print("Erreur : Le montant du dépôt doit être un nombre.")
                    return
                message = self.accounts[account_number].deposit(amount)
                print(message)
            else:
                print("Erreur : PIN incorrect.")
        else:
            print("Erreur : Compte non trouvé.")

    def withdraw(self):
        print("Retrait d'un compte.")
        account_number = input("Entrez le numéro de compte : ")
        pin = int(getpass.getpass("Entrez le PIN : "))
        if account_number in self.accounts:
            if self.accounts[account_number].check_pin(pin):
                try:
                    amount = float(input("Entrez le montant à retirer : "))
                except ValueError:
                    print("Erreur : Le montant du retrait doit être un nombre.")
                    return
                message = self.accounts[account_number].withdraw(amount)
                print(message)
            else:
                print("Erreur : PIN incorrect.")
        else:
            print("Erreur : Compte non trouvé.")

    def transfer(self):
        print("Transfert entre comptes.")
        from_account_number = input("Entrez votre numéro de compte : ")
        to_account_number = input("Entrez le numéro de compte cible : ")
        pin = int(getpass.getpass("Entrez le PIN : "))
        if from_account_number in self.accounts and to_account_number in self.accounts:
            if self.accounts[from_account_number].check_pin(pin):
                try:
                    amount = float(input("Entrez le montant à transférer : "))
                except ValueError:
                    print("Erreur : Le montant du transfert doit être un nombre.")
                    return
                message = self.accounts[from_account_number].transfer(self.accounts[to_account_number], amount)
                print(message)
            else:
                print("Erreur : PIN incorrect.")
        else:
            print("Erreur : Un ou les deux comptes n'ont pas été trouvés.")

    def check_balance(self):
        print("Vérification du solde.")
        account_number = input("Entrez le numéro de compte : ")
        pin = int(getpass.getpass("Entrez le PIN : "))
        if account_number in self.accounts:
            if self.accounts[account_number].check_pin(pin):
                balance = self.accounts[account_number].get_balance()
                print(f"Solde : {balance}")
            else:
                print("Erreur : PIN incorrect.")
        else:
            print("Erreur : Compte non trouvé.")

    def display_account_details(self):
        print("Affichage des détails du compte.")
        account_number = input("Entrez le numéro de compte : ")
        pin = int(getpass.getpass("Entrez le PIN : "))
        if account_number in self.accounts:
            if self.accounts[account_number].check_pin(pin):
                details = self.accounts[account_number].display_account_details()
                print(details)
            else:
                print("Erreur : PIN incorrect.")
        else:
            print("Erreur : Compte non trouvé.")

    def save_account(self, account):
        with sqlite3.connect('bank.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO accounts (account_number, account_holder, pin, balance) VALUES (?, ?, ?, ?)",
                            (account.account_number, account.account_holder, account.pin, account.balance))
            conn.commit()

    def run(self):
        while True:
            print("\nApplication Bancaire")
            print("1. Créer un compte")
            print("2. Déposer")
            print("3. Retirer")
            print("4. Transférer")
            print("5. Vérifier le solde")
            print("6. Afficher les détails du compte")
            print("7. Quitter")
            choice = input("Entrez votre choix : ")
            if choice == '1':
                self.create_account()
            elif choice == '2':
                self.deposit()
            elif choice == '3':
                self.withdraw()
            elif choice == '4':
                self.transfer()
            elif choice == '5':
                self.check_balance()
            elif choice == '6':
                self.display_account_details()
            elif choice == '7':
                print("Fermeture de l'application.")
                break
            else:
                print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    app = BankApp()
    app.run()
