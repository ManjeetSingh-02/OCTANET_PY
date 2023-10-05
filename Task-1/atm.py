# Import database package
import sqlite3
import datetime

# Function to login a user in ATM
def login_user() :
    
    #Account details entry
    print("\nPlease input your details to login\n")
    account_number = input("Enter your account number(8 digits): ")
    pin = input("Enter your account number pin(4 digits): ")
    
    if len(account_number) != 8 :
        print("Account number must be of 8 digits")
    elif len(pin) != 4 :
        print("Account Pin must be of 4 digits")
    else :    
        #Checking database for account existence
        account_obj_cursor.execute('SELECT * FROM accounts WHERE account_number = ?', (account_number,))
        result = account_obj_cursor.fetchone()
        
        if result is None :
            #Database entry of new account
            default_account_balance = str(1000.00)
            account_obj_cursor.execute('INSERT INTO accounts (account_number, pin, balance) VALUES (?, ?, ?)', (account_number, pin, default_account_balance))
            accounts_db_connection.commit()
            
            #Database entry of default transaction
            default_transaction_id = 1
            default_transaction_type = "Credit"
            default_transaction_amount = str(1000.00)
            main_account_number = account_number
            from_account_number = account_number
            to_account_number = account_number
            current_date_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            transaction_obj_cursor.execute('INSERT INTO transactions (transaction_id, account_number, from_account_number, type, amount, total_amount, to_account_number, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (default_transaction_id, main_account_number, from_account_number, default_transaction_type, default_transaction_amount, default_transaction_amount, to_account_number, current_date_time))
            transactions_db_connection.commit()
        
        #Database check for account existence
        account_obj_cursor.execute('SELECT * FROM accounts WHERE account_number = ?', (account_number,))
        result = account_obj_cursor.fetchone()
            
        if result[1] == pin :
            print("\nSuccessfully Logged In\n")
            task_select_menu(account_number)
        else :
            print("\nWrong account number or pin\n")
    
    
# Function to get account transaction history
def get_transaction_history(account_number) :
        
    transaction_obj_cursor.execute('SELECT * FROM transactions WHERE account_number = ?', (account_number,))
    result = transaction_obj_cursor.fetchall()
    
    for transaction in result :
        print("\n")
        print("Transaction ID - ", transaction[1])
        print("Main Account Number - ", transaction[2])
        print("(Debited/Credited) From Account Number - ", transaction[3])
        print("Transaction Type - ", transaction[4])
        print("Transaction Amount - ", transaction[5])
        print("Total Amount - ", transaction[6])
        print("(Debited/Credited) To Account Number - ", transaction[7])
        print("Transaction Date & Time - ", transaction[8])
        print("\n")


# Function to deposit money in account
def deposit_amount(account_number) :
    
    #Amount entry details
    credit_amount = float(input("Enter the amount you want to deposit: "))
    
    if credit_amount < 1 :
        print("Minimum deposit is Rs.1")
    else :
        #Fetching the account
        account_obj_cursor.execute('SELECT * FROM accounts WHERE account_number = ?', (account_number,))
        result = account_obj_cursor.fetchone()
        
        total_amount = credit_amount + result[2]
        
        #Updating the balance
        account_obj_cursor.execute('UPDATE accounts SET balance = ? WHERE account_number = ?', (total_amount, account_number))
        accounts_db_connection.commit()
        
        transaction_obj_cursor.execute('SELECT * FROM transactions WHERE account_number = ? ORDER BY transaction_id DESC LIMIT 1', (account_number,))
        result = transaction_obj_cursor.fetchone()
        
        #Updating the transactions
        transaction_id = result[1] + 1
        transaction_type = "Credit"
        transaction_amount = str(credit_amount)
        current_date_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        main_account_number = account_number
        from_account_number = account_number
        to_account_number = account_number
        transaction_obj_cursor.execute('INSERT INTO transactions (transaction_id, account_number, from_account_number, type, amount, total_amount, to_account_number, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (transaction_id, main_account_number, from_account_number, transaction_type, transaction_amount, total_amount, to_account_number, current_date_time))
        transactions_db_connection.commit()
        
        print("\nAmount Deposited, New Balance - ", total_amount)
    
    
# Function to withdraw money in account
def withdraw_amount(account_number) :
    
    #Amount entry details
    debit_amount = float(input("Enter the amount you want to withdraw: "))
    
    if debit_amount < 1 :
        print("Minimum withdraw is Rs.1")
    else :    
        #Fetching the account
        account_obj_cursor.execute('SELECT * FROM accounts WHERE account_number = ?', (account_number,))
        result = account_obj_cursor.fetchone()
        
        #Amount Check
        if result[2] < debit_amount :
            print("Your Balance is less than the amount you have entered to withdraw")
        else :
            total_amount = result[2] - debit_amount
            
            #Updating the balance
            account_obj_cursor.execute('UPDATE accounts SET balance = ? WHERE account_number = ?', (total_amount, account_number))
            accounts_db_connection.commit()
            
            transaction_obj_cursor.execute('SELECT * FROM transactions WHERE account_number = ? ORDER BY transaction_id DESC LIMIT 1', (account_number,))
            result = transaction_obj_cursor.fetchone()
            
            #Updating the transactions
            transaction_id = result[1] + 1
            transaction_type = "Debit"
            transaction_amount = str(debit_amount)
            current_date_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            main_account_number = account_number
            from_account_number = account_number
            to_account_number = account_number
            transaction_obj_cursor.execute('INSERT INTO transactions (transaction_id, account_number, from_account_number, type, amount, total_amount, to_account_number, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (transaction_id, main_account_number, from_account_number, transaction_type, transaction_amount, total_amount, to_account_number, current_date_time))
            transactions_db_connection.commit()
            
            print("\nAmount Withdrawn, New Balance - ", total_amount)
    

# Function to transfer money in account
def transfer_amount(account_number) :
    
    #Account input details
    transfer_account_number = input("Enter the account number where you want to transfer the amount(8 digits): ")
    
    if len(transfer_account_number) != 8 :
        print("Account number must be of 8 digits")
    elif transfer_account_number == account_number :
        print("You can't transfer amount from and to your account")
    else :
        #Fetching & checking the account
        account_obj_cursor.execute('SELECT * FROM accounts WHERE account_number = ?', (transfer_account_number,))
        result = account_obj_cursor.fetchone()
        
        if result is None :
            print("No account exist with that number")
        else :
            account_transfer_amount = float(input("Enter the amount you want to transfer: "))
            
            if account_transfer_amount < 1 :
                print("Minimum transfer amount is Rs.1")
            else :
                account_obj_cursor.execute('SELECT * FROM accounts WHERE account_number = ?', (account_number,))
                result = account_obj_cursor.fetchone()
                
                if result[2] < account_transfer_amount :
                    print("Your balance is less than the transfer amount")
                else :
                    total_amount = result[2] - account_transfer_amount
                    
                    #Updating the balance
                    account_obj_cursor.execute('UPDATE accounts SET balance = ? WHERE account_number = ?', (total_amount, account_number))
                    accounts_db_connection.commit()
                    
                    transaction_obj_cursor.execute('SELECT * FROM transactions WHERE account_number = ? ORDER BY transaction_id DESC LIMIT 1', (account_number,))
                    result = transaction_obj_cursor.fetchone()
                    
                    #Updating the transactions
                    transaction_id = result[1] + 1
                    transaction_type = "Debit"
                    transaction_amount = str(account_transfer_amount)
                    current_date_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    main_account_number = account_number
                    from_account_number = account_number
                    to_account_number = transfer_account_number
                    transaction_obj_cursor.execute('INSERT INTO transactions (transaction_id, account_number, from_account_number, type, amount, total_amount, to_account_number, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (transaction_id, main_account_number, from_account_number, transaction_type, transaction_amount, total_amount, to_account_number, current_date_time))
                    transactions_db_connection.commit()
                    
                    account_obj_cursor.execute('SELECT * FROM accounts WHERE account_number = ?', (transfer_account_number,))
                    result = account_obj_cursor.fetchone()
                    
                    new_total_amount = result[2] + account_transfer_amount
                    
                    account_obj_cursor.execute('UPDATE accounts SET balance = ? WHERE account_number = ?', (new_total_amount, transfer_account_number))
                    accounts_db_connection.commit()
                    
                    
                    transaction_obj_cursor.execute('SELECT * FROM transactions WHERE account_number = ? ORDER BY transaction_id DESC LIMIT 1', (transfer_account_number,))
                    result = transaction_obj_cursor.fetchone()
                    
                    #Updating the transactions
                    transaction_id = result[1] + 1
                    transaction_type = "Credit"
                    transaction_amount = str(account_transfer_amount)
                    current_date_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    main_account_number = transfer_account_number
                    from_account_number = account_number
                    to_account_number = transfer_account_number
                    transaction_obj_cursor.execute('INSERT INTO transactions (transaction_id, account_number, from_account_number, type, amount, total_amount, to_account_number, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (transaction_id, main_account_number, from_account_number, transaction_type, transaction_amount, new_total_amount, to_account_number, current_date_time))
                    transactions_db_connection.commit()
                    
                    print("\nAmount Transferred, New Balance - ", total_amount)
        
    
    
# Function to select the task to perform in to-do-list
def task_select_menu(account_number) :
    print("Enter 1 - Get your Transaction History\nEnter 2 - Deposit Amount\nEnter 3 - Withdraw Amount\nEnter 4 - Transfer Amount\nEnter any key to close the ATM")
    task_op = int(input("Select Operation: "))

    if task_op == 1 :
        get_transaction_history(account_number)
    elif task_op == 2 :
        deposit_amount(account_number)
    elif task_op == 3 :
        withdraw_amount(account_number)
    elif task_op == 4 :
        transfer_amount(account_number)
    else :
        print("Thanks for using the ATM")






#Start of program
print("Welcome to ATM")


#Creating , Connecting database and creating a object for accounts
accounts_db_connection = sqlite3.connect("db/accounts.db")
account_obj_cursor = accounts_db_connection.cursor()


#Checking database for accounts table existence
account_obj_cursor.execute('SELECT name FROM sqlite_master WHERE type=\'table\' AND name=\'accounts\';')
result = account_obj_cursor.fetchone()
if result is None :
    #Database entry of accounts table if doesn't exist
    account_obj_cursor.execute('CREATE TABLE accounts (account_number INTEGER PRIMARY KEY NOT NULL, pin VARCHAR(4) NOT NULL, balance DECIMAL(10,2) NOT NULL);')
    accounts_db_connection.commit()
    
    
#Creating , Connecting database and creating a object for transactions
transactions_db_connection = sqlite3.connect("db/transactions.db")
transaction_obj_cursor = transactions_db_connection.cursor()


#Checking database for transactions table existence
transaction_obj_cursor.execute('SELECT name FROM sqlite_master WHERE type=\'table\' AND name=\'transactions\';')
result = transaction_obj_cursor.fetchone()
if result is None :
    #Database entry of transactions table if doesn't exist
    transaction_obj_cursor.execute('CREATE TABLE transactions (id INTEGER PRIMARY KEY AUTOINCREMENT, transaction_id INTEGER NOT NULL, account_number INT NOT NULL, from_account_number INT NOT NULL, type VARCHAR(10) NOT NULL, amount DECIMAL(10,2) NOT NULL, total_amount DECIMAL(10,2) NOT NULL, to_account_number INT NOT NULL, date DATETIME NOT NULL, FOREIGN KEY (account_number) REFERENCES accounts(account_number));')
    transactions_db_connection.commit()
    

#User Select Menu
print("Enter 1 - Login to manage your account\nEnter any key to close the ATM")
user_op = int(input("Select Operation: "))
if user_op == 1 :
    login_user()
else :
    print("Thanks for using the ATM")
    
    
accounts_db_connection.close()
transactions_db_connection.close()