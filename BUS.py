"""
BANKING USER SYSTEM

An intermediate python project that helps strengthen python skills by tying together various
python and object-oriented programming concepts.

This program allows a user to create a banking account, View/Edit User Profile and Deposit/Withdraw Money

"""

#PROGRAM START

#Import necessary packages.
#stdiomask helps mask your pasword while typing and must be installed using pip

import hashlib
import _pickle as pickle
from stdiomask import getpass
from datetime import datetime

#Customer class stores the User Profile and allows the User to perform Account Operations

class Customer:
	total_customers = 0

	#Initializes Instance variables through a dictionary
	def __init__(self, account_dict):
			
		for key in account_dict:
			setattr(self, key, account_dict[key])

		self.account_dict = account_dict


	#Allows User to View and Modify Profile
	def profile(self):
		print("\n_____PROFILE_____\n")
		print(f"\n1. Name: {self.name}\n2. Account Number: {self.accnum}\n3. Date of Birth: {self.dob}\n4. Mobile Number: {self.mobnum}\n5. Last Login: {self.last_login}")
		
		while True:
			profile_input = input("\nTo EDIT your profile type 'E' else type 'M' to go back to MAIN MENU: ").strip().upper()

			if (profile_input == "E"):
				account_dict = update_profile()
				self.name = account_dict['name']
				self.mobnum = account_dict['mobnum']
				self.dob = account_dict['dob']

				print("\nYour Profile has been Updated Successfuly!\n")

				with open(f"{self.uname}.pkl", "wb") as cdeets:
					pickle.dump(self, cdeets, -1)
				return "goto_main_menu"

			if (profile_input == "M"):
				return "goto_main_menu"

			else:
				print("\nError! Please Enter a Valid Response.")


	#Prints Account Summary and Transaction History (If Available)
	def account_summary(self):
		print("\n_____ACCOUNT SUMMARY_____\n")
		print(f"\n Name: {self.name}   |   Account Number: {self.accnum}   |   Account Balance: {self.accbalance}\n")
		print("\n*** Transaction History ***\n")

		if(len(self.acchistory.keys()) == 0):
			print("No Transactions Found!")

		else:
			print(f"No.       Date          Time         Type         Amount\n")
			for i, key in enumerate(self.acchistory, start=1):

				if(self.acchistory[key][0] == "Deposit"):
					print(f"{i}.     {key}      {self.acchistory[key][0]}        {self.acchistory[key][1]}")

				else:
					print(f"{i}.     {key}      {self.acchistory[key][0]}     {self.acchistory[key][1]}")

		while True:
			response = input("\nEnter 'M' to go back to MAIN MENU: ").strip().upper()

			if(response == 'M'):
				return "goto_main_menu"

			else:
				print("Please Enter a Valid Response.")
				continue

	
	#Allows User to Deposit and Withdraw Money to/from Account. 
	#Appends data to 'acchistory' to View Transaction History in Account Summary.
	def dw(self):
		print("\n_____DEPOSIT / WITHDRAWAL_____")

		while True:
			print(f"\n\n Current Account Balance: {self.accbalance}")
			dorw = input("\nEnter 'D' to DEPOSIT or 'W' to WITHDRAW money (Enter 'M' to go back to MAIN MENU): ").strip().upper()

			if (dorw == 'M'):
				return "goto_main_menu"

			elif (dorw == "D"):

				try:
					d_amount = int(input("\nEnter Amount to Deposit: ").strip())

				except:
					print("\n Error! Enter a Valid Number.")

				d_datetime = datetime.now().strftime("%d/%m/%Y     %H:%M:%S")	
				self.acchistory[d_datetime] = ['Deposit', d_amount]
				self.accbalance += d_amount

				with open(f"{self.uname}.pkl", "wb") as cdeets:
					pickle.dump(self, cdeets, -1)

				print("\n\nDeposit Successful!")

			elif (dorw == "W"):
				try:
					w_amount = int(input("\nEnter Amount to Withdraw: ").strip())

				except:
					print("\n Error! Enter a Valid Number.")
					continue

				if(w_amount > self.accbalance):
					print("\n Insufficient Balance in Account!")

				else:
					d_datetime = datetime.now().strftime("%d/%m/%Y     %H:%M:%S")
					date_key = d_date +"     "+ d_time	
					self.acchistory[date_key] = ['Withdrawal', w_amount]
					self.accbalance -= w_amount

					with open(f"{self.uname}.pkl", "wb") as cdeets:
						pickle.dump(self, cdeets, -1)

					print("\n\nWithdrawal Successful!")

			else:
				print("\nPlease Enter a Valid Response. \n\n")


#Create account with Useername and Password and Add Profile details.
#Creates and Stores data in pickle file named '<username>'
#Appends username to "UnameList.pkl" to check if Username exists while creating New Account.
def create_account():
	print("\n_____CREATE YOUR ACCOUNT_____\n")

	try:
		with open("UnameList.pkl", 'rb') as UnameList:
			temp_uname_list = pickle.load(UnameList)

	except:
		with open("UnameList.pkl", 'wb') as UnameList:
			temp_uname_list = []

	while True:
		uname = input("Enter a Username: ").strip()

		if (uname in temp_uname_list):
			print("Username already exists! Please choose another Username.\n")
			continue

		else:
			passw = input("Enter a Password: ").strip()
			passw_conf = input("Enter your Password again: ").strip()
			#passw = getpass(prompt="Enter a Password: ").strip()
			#passw_conf = getpass(prompt="Enter your Password again: ").strip()
					
			if(passw != passw_conf):
				print("Error! Passwords do not match. \n\n")
				continue

			elif(len(uname) == 0 or len(passw) == 0):
				print("Please Enter a Valid Response. \n\n")
				continue

			else:
				temp_uname_list.append(uname)
				passw = hashlib.sha256(passw.encode()).hexdigest()
				account_dict = update_profile()
				accnum = datetime.now().strftime("%d%m%Y%H%M%S%f")[0:-5]
				accbalance = 0
				acchistory = {}
				last_login = "Now"
				account_dict.update({"accnum":accnum, "accbalance":accbalance, "acchistory":acchistory, "last_login":last_login,"uname":uname, "passw":passw})

				customer1 = Customer(account_dict)

				with open(f"{uname}.pkl", "wb") as cdeets:
					pickle.dump(customer1, cdeets, -1)

				with open("UnameList.pkl", "wb") as UnameList:
					pickle.dump(temp_uname_list, UnameList, -1)

				print("\nUser Created Successfuly! Login to your account via Existing Customer.\n\n")
				
				return "goto_intro"


#Add/Modify User Profile Details
def update_profile():
	account_dict = {}
	print("\n_____PROFILE UPDATE_____\n")

	while True:
		date_error = False

		name = input("Enter your Name: ").strip().upper()
		mobnum = input("Enter your 10-digit Mobile Number: ").strip()
		dob = input("Enter your Date of Birth (DD/MM/YYYY): ").strip()

		try:
			dob = datetime.strptime(dob, "%d/%m/%Y").strftime("%d/%m/%Y")

		except:
			date_error = True

		if(len(name)==0 or not mobnum.isdigit() or len(mobnum)!=10 or date_error):
			print("\nERROR! Please Check your Input and Try Again!\n")

		else:
			account_dict.update({"name":name, "mobnum":mobnum, "dob":dob})
			return account_dict
			

#Login mechanism into User Account. 
#If Invalid Credentials are provided more than 3 times, EXIT Program.
def login_account():
	global customer
	global login_datetime
	trys_left = 3
	print("\n_____ACCOUNT LOGIN_____\n")

	while True and trys_left > 0:
		uname = input("Enter a Username: ").strip()
		passw = input("Enter a Password: ").strip() 
		passw = hashlib.sha256(passw.encode()).hexdigest()

		try:
			with open(f"{uname}.pkl", "rb") as unamepkl:
				customer = pickle.load(unamepkl)

		except:
			trys_left -= 1
			print(f"Invalid Credentials! You have {trys_left} attempts left.\n")
			continue
		
		if(passw != customer.passw):
			trys_left -= 1
			print(f"Invalid Credentials! You have {trys_left} attempts left.\n")

		else:
			global is_login 
			is_login = True
			login_datetime = datetime.now().strftime("%d/%m/%Y  %H:%M:%S")
			print(f"\nLogin Successful!     |     Last Login: {customer.last_login}")
			return "goto_main_menu"

	print("Error! Restart Program.\n\n\n")
	return "goto_intro"



#Intro Page when program is first run. Connects to other functions
def intro():
	
	print("*** x-x-x- WELCOME TO THE FUTURE BANK -x-x-x ***\n")
	c_type = input("Enter E for 'Existing Customer' or N for 'New Customer': ").strip().upper()

	if(c_type == 'N'):
		return create_account()

	if(c_type == 'E'):
		return login_account()

	else:
		print("\nError! Please Enter a Valid Response.\n\n")
		return intro()


#Main Menu Page when the User Logs in Successfully
def main_menu():
	print("\n_____MAIN MENU_____\n")
	print("1. Profile \n2. Account Summary \n3. Deposit/Withdrawal \n4. Logout")

	while True:
		response = input("Enter your Option Number (1-4): ").strip()

		if (response == '1'):
			return customer.profile()

		elif (response == '2'):
			return customer.account_summary()

		elif (response == '3'):
			return customer.dw()

		elif(response == '4'):
			customer.last_login = login_datetime
			with open(f"{customer.uname}.pkl", "wb") as cdeets:
				pickle.dump(customer, cdeets, -1)

			print("\nLogout Successful!\n\n")	
			return "goto_intro"

		else:
			print("\nError! Please Enter a Valid Response.\n")



#Main Program that loops, till User closes program manually
intro_result = intro()
while True:

	if (intro_result == "goto_intro"):
		intro_result = intro()

	elif (intro_result == "goto_main_menu"):
		intro_result = main_menu()

#PROGRAM END