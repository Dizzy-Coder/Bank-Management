from time import gmtime, strftime

class Account:
    def __init__(self, name, email, address, account_type, account_id):
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.id = account_id
        self.balance = 0
        self.loan_count = 0
        self.loan = 0
        self.transaction_history = []

    def deposit(self, amount):
        self.balance += amount
        Bank.total_balance += amount
        print(f"{amount} taka deposit successful.")
        self.transaction_history.append(f"{amount} taka was deposited at {strftime('%Y-%m-%d %H:%M:%S', gmtime())}.")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Withdrawal amount exceeded.")
        elif self.balance>Bank.total_balance:
            print("Bank is bankrupt.")
        else:
            self.balance -= amount
            Bank.total_balance -= amount
            print(f"{amount} taka withdrawal successful.")
            self.transaction_history.append(f"{amount} taka was withdrawn at {strftime('%Y-%m-%d %H:%M:%S', gmtime())}.")

    def check_balance(self):
        print(f"Current balance: {self.balance} taka")

    def take_loan(self, amount):
        if self.loan_count < 2:
            if amount > Bank.total_balance:
                print("Loan amount exceeded.")
            else:
                self.loan_count += 1
                self.loan += amount
                Bank.total_balance -= amount
                Bank.total_loan+=amount
                print(f"{amount} taka loan was taken")
                self.transaction_history.append(f"{amount} taka loan was taken at {strftime('%Y-%m-%d %H:%M:%S', gmtime())}.")
        else:
            print("Loan limit exceeded.")

    def transfer(self, recipient_id, amount):
        if recipient_id not in Bank.account_list:
            print("Account does not exist.")
        elif amount > self.balance:
            print("Transfer amount exceeds your balance.")
        else:
            self.balance -= amount
            Bank.account_list[recipient_id].balance += amount
            self.transaction_history.append(f"{amount} taka was transferred to account {recipient_id} at {strftime('%Y-%m-%d %H:%M:%S', gmtime())}.")
            Bank.account_list[recipient_id].transaction_history.append(f"{amount} taka was transferred from account {recipient_id} at {strftime('%Y-%m-%d %H:%M:%S', gmtime())}.")
            print(f"{amount} taka transferred successfully.")
    
    def view_trac_history(self):
        for i in self.transaction_history:
            print(i)

class Bank:
    total_balance = 0
    total_loan = 0
    loan_feature = True
    account_list = {}
    admin_list = {}

class User(Account):
    user_id = 1

    def __init__(self, name, email, address, account_type):
        self.id = User.user_id
        super().__init__(name, email, address, account_type, self.id)
        Bank.account_list[self.id] = self
        User.user_id += 1

class Admin:
    admin_id = 1

    def __init__(self, name, email, address):
        self.id = Admin.admin_id
        self.name = name
        self.email = email
        self.address = address
        Bank.admin_list[self.admin_id] = self
        Admin.admin_id += 1

    def del_acc(self, user_id):
        if user_id in Bank.account_list:
            Bank.account_list.pop(user_id)
            print(f"Account {user_id} deleted successfully.")
        else:
            print("Account does not exist.")

    def view_acc(self):
        if Bank.account_list:
            for id, acc in Bank.account_list.items():
                print(f"Account: {id} Name: {acc.name} E-mail: {acc.email} Address: {acc.address}")
        else:
            print("No accounts available.")

    def check_total_balance(self):
        print(f"Total Balance: {Bank.total_balance}")

    def check_total_loan(self):
        print(f"Total Loan: {Bank.total_loan}")

    def loan_feat_on(self):
        Bank.loan_feature = True
        print("Loan feature is on.")

    def loan_feat_off(self):
        Bank.loan_feature = False
        print("Loan feature is off.")

def user_dash():
    while True:
        action = int(input("User Dashboard \n1. Create Account \n2. Deposit \n3. Withdraw \n4. Check Balance \n5. Take Loan \n6. Transfer \n7. View Transaction History \n8. Exit\nChoose an action: "))

        if action == 1:
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            address = input("Enter your address: ")
            account_type = input("Enter account type \n1. Savings \n2. Current\nChoose an option: ")
            account_type = "Savings" if account_type == "1" else "Current"
            user = User(name, email, address, account_type)
            print(f"Account No: {user.id} was created successfully.")

        elif action in [2, 3, 4, 5, 6, 7]:
            id = int(input("Enter your ID: "))
            if id in Bank.account_list:
                if action == 2:
                    amount = int(input("Enter amount to deposit: "))
                    Bank.account_list[id].deposit(amount)
                elif action == 3:
                    amount = int(input("Enter amount to withdraw: "))
                    Bank.account_list[id].withdraw(amount)
                elif action == 4:
                    Bank.account_list[id].check_balance()
                elif action == 5:
                    amount = int(input("Enter amount to loan: "))
                    Bank.account_list[id].take_loan(amount)
                elif action == 6:
                    recipient_id = int(input("Enter recipient account ID: "))
                    amount = float(input("Enter amount to transfer: "))
                    Bank.account_list[id].transfer(recipient_id, amount)
                elif action ==7:
                    Bank.account_list[id].view_trac_history()
            else:
                print("Please create an account first.")
        elif action == 8:
            break

        else:
            print("Invalid action.")

def admin_dash():
    admin = Admin("Admin", "admin@example.com", "Admin Address")

    while True:
        action = int(input("Admin Dashboard \n1. Create Account \n2. View Accounts \n3. Delete Account \n4. Check Total Balance \n5. Check Total Loan \n6. Turn On Loan Feature \n7. Turn Off Loan Feature \n8. Exit \nChoose an action: "))

        if action == 1:
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            address = input("Enter your address: ")
            Admin(name, email, address)
            print(f"Admin account created successfully.")
        elif action == 2:
            admin.view_acc()
        elif action == 3:
            user_id = int(input("Enter user ID to delete: "))
            admin.del_acc(user_id)
        elif action == 4:
            admin.check_total_balance()
        elif action == 5:
            admin.check_total_loan()
        elif action == 6:
            admin.loan_feat_on()
        elif action == 7:
            admin.loan_feat_off()
        elif action == 8:
            break
        else:
            print("Invalid action.")

while True:
    bank = Bank()
    print("Welcome to the bank!!")
    print("1. User")
    print("2. Admin")
    print("3. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        user_dash()
    elif choice == 2:
        username = input("Enter Username: ")
        password = input("Enter password: ")
        if (username == "admin" and password == "123"):
            admin_dash()
        else:
            print("Wrong username or password.")
            break
    elif choice == 3:
        break
    else:
        print("Invalid Input!!")
