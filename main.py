from decimal import Decimal
#SQL
import mysql.connector 

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Ashdazoi.23",
    database="bankAccount"
)

mycursor = db.cursor()

#Create SQL Table for User Accounts
#mycursor.execute("CREATE TABLE Person (username VARCHAR(50) NOT NULL, email mediumtext NOT NULL, password VARCHAR(50) NOT NULL, currentBalance DECIMAL(19,2) DEFAULT 0, userID int PRIMARY KEY AUTO_INCREMENT)")

newQ1 = "INSERT INTO Person (username, email, password) VALUES (%s, %s, %s)"

#Add Testing Authorized User to Person Table
#mycursor.execute("INSERT INTO Person (username, email, password) VALUES (%s, %s, %s)", ("authorized", "authorized@authorized.com", "authorized"))
#db.commit()

#Create SQL Table for Transaction
#mycursor.execute("CREATE TABLE Transaction (transactionID INT AUTO_INCREMENT PRIMARY KEY, currentBalance INT DEFAULT 0, money DECIMAL(19,2) NOT NULL, type ENUM('deposit','withdraw') NOT NULL, userID INT NOT NULL, FOREIGN KEY (userID) REFERENCES Person(userID))")
newQ2 = "INSERT INTO Transaction (money, type, userID) VALUES (%s, %s, %s)"

#Python 
current_balance = 0
program_loop = True
username = None

#Creates a function for the options
def options():
    print("----------------------------")
    print("1. Make a Transaction")
    print("2. Account Settings")
    print("3. Exit")
    print("----------------------------")

#Creates a function for user selection
def user_selection(): 
    global username
    in_use = True
    choice = int(input("What would you like to do? "))
    print("\n")

    #Make a Transaction
    if choice == 1:
        makeTransaction(username)
    
    #Account Settings
    elif choice == 2:
        accountSettings()
    
    #Exit
    elif choice == 3:
        print("Thank you for choosing Bank of America. Goodbye!")
        in_use = False

    else:
        print("Sorry, that is not a valid choice. Please pick a number 1-3.")
    return in_use

def fetchCurrentBalance(username):
    mycursor.execute("SELECT currentBalance FROM Person WHERE username = %s", (username,))
    result = mycursor.fetchone()
    if result:
        return result[0]  # Return the current balance
    else:
        return None

def updateCurrentBalance(username, new_balance):
    mycursor.execute("UPDATE Person SET currentBalance = %s WHERE username = %s", (new_balance, username))
    db.commit()

#Creates Function for making a transaction
def makeTransaction(username):
    print("Make a Transaction:")
    print("1. Deposit")
    print("2. Withdraw")
    print("3. Check Balance")
    print("4. Go to Home")
    transactionChoice = int(input("What type of transaction would you like to do? "))
    print("----------------------------")
    while transactionChoice != 1 and transactionChoice != 2 and transactionChoice != 3 and transactionChoice != 4:
        print("Sorry, that is not a valid choice. Please pick a number 1-4.")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Go to Home")
        transactionChoice = int(input("What type of transaction would you like to do? "))
        print("----------------------------")
    #deposit
    if transactionChoice == 1:
        money = Decimal(input("Enter the amount you want to deposit: $"))
        current_balance = fetchCurrentBalance(username)
        if current_balance is not None:
            new_balance = current_balance + money
            updateCurrentBalance(username, new_balance)
            print(f"${money} has been deposited into your account.")
            print("----------------------------")
        else:
            print(f"Failed to deposit ${money}.")
            print("----------------------------")

    #withdraw
    elif transactionChoice == 2:
        money = Decimal(input("Enter the amount you want to withdraw: $"))
        current_balance = fetchCurrentBalance(username)
        if current_balance is not None:
            if money <= current_balance:
                new_balance = current_balance - money
                updateCurrentBalance(username, new_balance)
                print(f"${money} has been withdrawn from your account.")
                print("----------------------------")
            else:
                print("Insufficient funds. Withdrawal failed.")
                print("----------------------------")
        else:
            print("Failed to get balance.")
            print("----------------------------")

    #check balance
    elif transactionChoice == 3:
        current_balance = fetchCurrentBalance(username)
        if current_balance is not None:
            print(f"Your account balance is: {current_balance}")
        else:
            print("Failed to get current balance.")
            print("----------------------------")
    else:
        print("Redirecting to home page.")

#Creates Function for creating an account
def createAccount():
    print("Create a New Account:")
    newUsername = input("Username: ")
    newEmail = input("Email: ")
    newPassword = input("Password: ")
    newAcc = (newUsername, newEmail, newPassword)
    #Adds new account to database
    mycursor.execute(newQ1, newAcc)
    db.commit()
    print("Account creation successful. Thank you for choosing Bank of America!")

#Creates a function to delete the logged in account
def deleteAccount():
    confirm = input("Are you sure you want to delete your account? (Y/N): ")
    if confirm.upper() == 'Y':
        # Get the username of the logged-in user
        logged_in_user = getLoggedInUsername()
        if logged_in_user:
            # Delete the user's account from the database
            mycursor.execute("DELETE FROM Person WHERE username = %s", (logged_in_user,))
            db.commit()
            print("Your account has been successfully deleted.")
        else:
            print("There has been an issue deleting your account.")
    else:
        print("Account deletion canceled.")

#Creates a function to access the logged in account
def getLoggedInUsername():
    #Verifies the account login
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    mycursor.execute("SELECT username FROM Person WHERE username = %s AND password = %s", (username, password))
    user = mycursor.fetchone()

    if user:
        return user[0]  # Return the username if login is successful
    else:
        print("Invalid username or password.")
        return None

#Creates a function to modify account details
def modifyAccountDetails():
    # Get the username of the logged-in user
    logged_in_user = getLoggedInUsername()
    if logged_in_user:
        print("----------------------------")
        print("Modify Account Details:")
        print("1. Username")
        print("2. Email")
        print("3. Password")
        modifyChoice = int(input("What would you like to modify? "))
        print("----------------------------")
        while modifyChoice != 1 and modifyChoice != 2 and modifyChoice != 3:
            print("Sorry, that is not a valid option.")
            print("----------------------------")
            print("1. Username")
            print("2. Email")
            print("3. Password")
            modifyChoice = int(input("Please pick a number 1-3: "))
            print("----------------------------")
        if modifyChoice == 1:
            #Changes username
            newUsername = input("New Username: ")
            mycursor.execute("UPDATE Person SET username = %s WHERE username = %s", (newUsername, logged_in_user))
            db.commit()
            print("Your username has been updated.")
            
            #Testing
            mycursor.execute("SELECT * FROM Person")

            for x in mycursor:
                print(x)

        elif modifyChoice == 2:
            #Changes email
            newEmail = input("New Email: ")
            mycursor.execute("UPDATE Person SET email = %s WHERE username = %s", (newEmail, logged_in_user))
            db.commit()
            print("Your email has been updated.")

            #Testing
            mycursor.execute("SELECT * FROM Person")

            for x in mycursor:
                print(x)
        else:
            #Changes password
            newPassword = input("New Password: ")
            mycursor.execute("UPDATE Person SET password = %s WHERE username = %s", (newPassword, logged_in_user))
            db.commit()
            print("Your password has been updated.")

            #Testing
            mycursor.execute("SELECT * FROM Person")

            for x in mycursor:
                print(x)
    else:
        print("Sorry, we cannot find that account.")

#Creates function for the account settings options
def accountSettings():
    print("Account Settings:")
    print("1. Create a New Account")
    print("2. Delete Your Account")
    print("3. Modify Your Account Details")
    print("4. Go to Home")
    accountChoice = int(input("What would you like to do? ")) #Prompts user for what they want to do
    print("----------------------------")
    #If the user choice is not available
    while accountChoice != 1 and accountChoice != 2 and accountChoice != 3 and accountChoice != 4:
        print("Sorry, that is not a valid choice. Please pick a number 1-4.")
        print("1. Create a New Account")
        print("2. Delete Your Account")
        print("3. Modify Your Account Details")
        print("4. Go to Home")
        accountChoice = int(input("What would you like to do? "))
        print("----------------------------")
    #creates a new account
    if accountChoice == 1:
        createAccount() #Calls createAccount function
    
    #deletes account
    elif accountChoice == 2:
        print("Delete Your Account:")
        deleteAccount() #Calls deleteAccount function

    #modify account details
    elif accountChoice == 3:
        modifyAccountDetails() #Calls modifyAccountDetails function

    else:
        print("Redirecting to home page.")

#Makes the user select to login to their account or sign up for one
print("Welcome to Bank of America!")
print("1. Login")
print("2. Sign-Up")
starting = int(input("Enter 1 or 2: "))
print("----------------------------")

#If they do not pick 1 or 2
while starting != 1 and starting != 2:
    print("Sorry, that is an invalid choice.")
    print("1. Login")
    print("2. Sign-Up")
    starting = int(input("Enter a number 1 or 2: "))
    print("----------------------------")

#Logs in to account
if starting == 1:
    login_success = False  #Tracks if login is successful
    while not login_success:
        username = input("Username: ")
        password = input("Password: ")

        # Query the database to check if the username and password match
        mycursor.execute("SELECT * FROM Person WHERE username = %s AND password = %s", (username, password))
        user = mycursor.fetchone()  # Fetches the first matching row
    
        if user:
            print("Login successful!")
            login_success = True #Changes to true so it doesn't re-loop
        else:
            print("Invalid username or password. Please try again.\n") #Prompts user again

#Creates New Account
else:
    createAccount()

while program_loop:
    options()
    program_loop = user_selection()