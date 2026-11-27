# ***** ----- ***** ----- USERS FEATURES ----- ***** ----- *****

class RailwayManagementSystem():

    # ---------------- FILE HANDLING ----------------

    # for saving trains
    def save_trains(self):
        # In this we dont have to close file because we use "with"
        with open("Text files/trains.txt", "w") as file: # in write mode
            # write train in this file with the help of for loop
            for train in self.Trains:
                file.write(str(train) + "\n")

    # This function is joining with the save_trains function
    def load_trains(self):
        # importing ast
        import ast
        # start exception handling with 'try'
        try:
            with open("Text files/trains.txt", "r") as file:
                self.Trains = []
                # the line will add in the empty self.Trains[] list that is in the function of save_trains 
                for line in file:
                    self.Trains.append(ast.literal_eval(line.strip()))
        # except case of exception handling
        except FileNotFoundError:
            pass

    # for saving passengers
    def save_passengers(self):
        with open("Text files/passengers.txt", "w") as file:
            # write passenger in this file with the help of for loop
            for passenger in self.passengers:
                file.write(str(passenger) + "\n")

    # This function is joining with the save_passengers function
    def load_passengers(self):
        # importing ast
        import ast
        # start exception handling with 'try'
        try:
            with open("Text files/passengers.txt", "r") as file:
                self.passengers = []
                # the line will add in the empty self.passengers[] list that is in the function of save_passengers
                for line in file:
                    self.passengers.append(ast.literal_eval(line.strip()))
        # except case of exception handling
        except FileNotFoundError:
            pass

    # for saving bookings
    def save_bookings(self):
        with open("Text files/bookings.txt", "w") as file:
            # write booking in this file with the help of for loop
            for booking in self.all_booked_tickets:
                file.write(str(booking) + "\n")

    # This function is joining with the save_bookings function
    def load_bookings(self):
        # importing ast
        import ast
        # start exception handling with 'try'
        try:
            with open("Text files/bookings.txt", "r") as file:
                self.all_booked_tickets = []
                # the line will add in the empty self.all_booked_tickets[] list that is in the function of save_bookings
                for line in file:
                    self.all_booked_tickets.append(ast.literal_eval(line.strip()))
        # except case of exception handling
        except FileNotFoundError:
            pass

    # for saving admins
    def save_admins(self):
        with open("Text files/admins.txt", "w") as file:
            # write booking in this file with the help of for loop
            for admin in self.admin_account_details:
                file.write(str(admin) + "\n")

    # This function is joining with the save_admins function
    def load_admins(self):
        # importing ast
        import ast
        # start exception handling with 'try'
        try:
            with open("Text files/admins.txt", "r") as file:
                self.admin_account_details = []
                # the line will add in the empty self.admin_account_details[] list that is in the function of load_admins
                for line in file:
                    self.admin_account_details.append(ast.literal_eval(line.strip()))
        # except case of exception handling
        except FileNotFoundError:
            pass

    # for saving OTP
    def save_otp(self):
        with open("Text files/OTP.txt","w") as file:
            # write otp in this file with the help of for loop
            for otp in self.OTP:
                file.write(str(otp)+"\n")

    # This function is joining with the save_otp function
    def load_otp(self):
        # importing ast
        import ast
        # start exception handling with 'try'
        try:
            with open("Text files/OTP.txt","r") as file:
                self.OTP=[]
                # the line will add in the empty self.otp[] list that is in the function of load_otp
                for line in file:
                    self.OTP.append(ast.literal_eval(line.strip()))
        # except case of exception handling
        except FileNotFoundError:
            pass
        
    # ********** ----- ***** -----********** ----- ***** ----- Magic Method ----- ***** ----- **********----- ***** ----- ******* ------ ********** --------

    # Magic Method 
    def __init__(self):
        # List of All Trains
        self.Trains=[("Jan Shatabdi",142809, "4", "Saharanpur", "New Delhi", "11:08 PM", "12:05 AM",58),
        ("Vande Bharat",221458, "5", "Jaipur", "Anand Vihar", "03:05 AM", "03:55 AM",45),
        ("Passenger",645378, "4", "Jaipur", "Anand Vihar", "02:15 AM", "03:50 AM",0)]
        
        # Empty passenger[] list
        self.passengers=[]
        
        # Empty all booked tickets[] list
        self.all_booked_tickets=[]
        
        # Admin Account Details[] list
        self.admin_account_details=[]

        self.OTP=[]

        # Calling all loading methods
        self.load_trains()
        self.load_passengers()
        self.load_bookings()
        self.load_admins()
        self.load_otp()

    # ********** ----- ***** -----********** ----- ***** ----- search_stations_from_api ----- ***** ----- **********----- ***** ----- *******

    def search_stations_from_api(self, search_text, limit=10):

        import os
        import requests
        from dotenv import load_dotenv

        load_dotenv()

        api_key = os.getenv("RAILCORE_KEY")

        if not api_key:
            return False, "API key not found. Check your .env file."

        url = "https://ir.railcore.tech/v1/stations/search"

        params = {
            "q": search_text.strip(),
            "limit": limit
        }

        headers = {
            "X-RailCore-Key": api_key
        }

        try:
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=20
            )
            response.raise_for_status()
            api_data = response.json()

            print("\nSEAT API RESPONSE:", api_data)

            if not api_data.get("success"):
                error = api_data.get("error", {})
                return False, error.get("message", "Unable to search stations.")

            stations = api_data.get("data", {}).get("results", [])

            return True, stations

        except requests.exceptions.HTTPError:
            try:
                error = response.json().get("error", {})
                message = error.get("message", "API request failed.")
            except ValueError:
                message = "API request failed."

            return False, f"HTTP {response.status_code}: {message}"

        except requests.exceptions.RequestException as error:
            return False, f"Connection error: {error}"

        except ValueError:
            return False, "Invalid response received from the API."

    # ********** ----- ***** -----********** ----- ***** ----- search_trains_from_api ----- ***** ----- **********----- ***** ----- *******

    def search_trains_from_api(self, from_station_code, to_station_code, journey_date, quota="GN"):

        import os
        import requests
        from dotenv import load_dotenv

        # Load API key from .env file
        load_dotenv()

        api_key = os.getenv("RAILCORE_KEY")

        if not api_key:
            return False, "API key not found. Check your .env file."

        # API endpoint
        url = "https://ir.railcore.tech/v1/routes/trains"

        # Request parameters
        params = {
            "from": from_station_code.strip().upper(),
            "to": to_station_code.strip().upper(),
            "date": journey_date,
            "quota": quota,
            "match": "city"
        }

        # Authentication header
        headers = {
            "X-RailCore-Key": api_key
        }

        try:
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=20
            )

            response.raise_for_status()

            api_data = response.json()

            if not api_data.get("success"):
                error = api_data.get("error", {})
                return False, error.get("message", "Unable to fetch trains.")

            trains = api_data.get("data", {}).get("trains", [])

            return True, trains

        except requests.exceptions.HTTPError:
            try:
                error = response.json().get("error", {})
                message = error.get("message", "API request failed.")
            except ValueError:
                message = "API request failed. Please try again."

            return False, f"HTTP {response.status_code}: {message}"

        except requests.exceptions.RequestException as error:
            return False, f"Connection error: {error}"

        except ValueError:
            return False, "Invalid response received from the API."

    # ********** ----- ***** -----********** ----- ***** ----- get_train_platform_from_api ( User function ) ----- ***** ----- **********----- ***** ----- *******

    def get_train_platform_from_api(self, train_number, station_code):
        import os
        import requests
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("RAILCORE_KEY")

        if not api_key:
            return False, "API key not found. Check your .env file."
        url = f"https://ir.railcore.tech/v1/trains/{train_number}/live"

        headers = {
            "X-RailCore-Key": api_key
        }

        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=20
            )
            response.raise_for_status()
            api_data = response.json()
            if not api_data.get("success"):
                error = api_data.get("error", {})
                return False, error.get("message", "Unable to fetch platform.")
            stations = api_data.get("data", {}).get("stations", [])

            for station in stations:
                if station.get("station_code") == station_code:
                    platform = station.get("platform_number")
                    if platform is not None and str(platform).strip() not in ("", "0"):
                        return True, platform
                    return False, "Platform not available."
            return False, "Station not found in train route."
        except requests.exceptions.HTTPError:
            return False, f"HTTP Error: {response.status_code}"
        except requests.exceptions.RequestException as error:
            return False, f"Connection error: {error}"
        except ValueError:
            return False, "Invalid response received from API."
        
    # ********** ----- ***** -----********** ----- ***** ----- get_train_seat_availability_from_api ( User function ) ----- ***** ----- **********----- ***** ----- *******

    def get_train_seat_availability_from_api(
            self, train_number, from_station_code,
            to_station_code, journey_date, train_classes, quota="GN"
        ):
            import os
            import requests
            from dotenv import load_dotenv

            load_dotenv()
            api_key = os.getenv("RAILCORE_KEY")

            if not api_key:
                return False, "API key not found. Check your .env file."

            if not train_classes:
                return False, "Train class information not available."

            url = "https://ir.railcore.tech/v1/availability/seats"
            headers = {"X-RailCore-Key": api_key}
            counts = []

            for class_code in train_classes:
                params = {
                    "train_number": train_number,
                    "from": from_station_code,
                    "to": to_station_code,
                    "date": journey_date,
                    "class": class_code,
                    "quota": quota
                }

                try:
                    response = requests.get(
                        url,
                        headers=headers,
                        params=params,
                        timeout=20
                    )
                    response.raise_for_status()

                    api_data = response.json()
                    print("\nSEAT API RESPONSE:", api_data)

                except requests.exceptions.HTTPError:
                    print(
                        f"HTTP Error for class {class_code}: "
                        f"{response.status_code}"
                    )
                    continue

                except requests.exceptions.RequestException as error:
                    print(
                        f"Connection error for class {class_code}: {error}"
                    )
                    continue

                except ValueError:
                    print(f"Invalid response for class {class_code}.")
                    continue

                if not api_data.get("success"):
                    continue

                classes = api_data.get("data", {}).get("classes", [])

                for item in classes:
                    available_count = item.get("available_count")

                    if (
                        isinstance(available_count, int)
                        and not isinstance(available_count, bool)
                    ):
                        counts.append(available_count)

            print("AVAILABLE SEAT COUNTS:", counts)

            if counts:
                return True, max(counts)

            return False, "Numeric seat availability not provided."
    
    # ********** ----- ***** -----********** ----- ***** ----- Train Details Function ( User function ) ----- ***** ----- **********----- ***** ----- *******

    def train_details(self):
        # Input from user
        source=str(input("\nFrom station :- "))
        destination=str(input("To station :- "))
        found=False
        
        # Printing all trains that is available in the list of Trains using (For loop)
        for train in self.Trains:
            (Train_name,Train_number,Train_platform,From_station,To_station,Departure,Arrival,Available_Seats)=train    
            if From_station.lower()==source.lower() and To_station.lower()==destination.lower():
                print(f"""
*-----------------------------------*
|            TRAIN DETAILS          |
*-----------------------------------*
Train Name       :-   {Train_name}
Train Number     :-   {Train_number}
Platform         :-   {Train_platform}
From             :-   {From_station}
To               :-   {To_station}
Departure Timing :-   {Departure}
Arrival Timing   :-   {Arrival}
Available Seats  :-   {Available_Seats}
*-----------------------------------*""")
                found=True
                
        # If not found condition
        if not found:
            print(f"""
|  No trains are available from "{source}" to "{destination}".  |""")

    # ********** ----- ***** -----********** ----- ***** -- Show available Trains Function ( User function ) ----- ***** ----- **********----- ***** ----- **

    def available_trains(self):
        
        # Input from user
        from_station=str(input("\nFrom station :- "))
        to_station=str(input("To Station :- "))
        found=False
        
        # Printing all trains by putting from and to_station that is available in the list of Trains using (For loop) 
        for train in self.Trains:
            (Train_name,Train_number,Train_platform,From_station,To_station,Departure,Arrival,Available_Seats)=train
            
            if from_station.lower()==From_station.lower() and to_station.lower()==To_station.lower():
                print(f"""
*----------------------------------*
Train Name       :- {Train_name}
Train Number     :- {Train_number}
Platform Number  :- {Train_platform}
Departure Timing :- {Departure}
Arrival Timing   :- {Arrival}
*----------------------------------*""")
                found=True
                
        # If not found condition
        if not found:
            print(f"""
|  No trains are available from "{from_station}" to "{to_station}".  |""")
            
    # ********** ----- ***** -----********** ----- ***** ----- Available Seats Function ( User function ) ----- ***** ----- **********----- ***** ----- *****

    def available_seats(self):
        # Input from user
        train_number=int(input("\nEnter train number , and check seats availability :- "))
        found=False
        
        # Printing train seats by train_number that is available in the list of Trains using (For loop)
        for train in self.Trains:
            (Train_name,Train_number,Train_platform,From_station,To_station,Departure,Arrival,Available_Seats)=train
            
            if train_number==Train_number:
                print(f"""
*------------------------------------*
Train Name        :- {Train_name}
Train Number      :- {Train_number}
Available Seats   :- {Available_Seats}
*------------------------------------*""")
                found = True
                break
            
        # If not found condition
        if not found:
            print("""
 -------------------------------------------------
|  No train found with the entered train number.  |
 -------------------------------------------------""")

    # ********** ----- ***** -----********** ----- ***** ----- Book Tickets Function ( User function ) ----- ***** ----- **********----- ***** ----- *******

    def book_tickets(self):
        # import random and regular expression module
        import re
        import random
        # Input from user
        from_station=str(input("\nFrom Station :- "))
        to_station=str(input("To Station :- "))
        found=False
        
        # Empty Train list
        train2=[]
        
        # Printing all trains by putting from_station and to_station that is available in the list of Trains using (For loop)
        for train in self.Trains:
            (Train_name,Train_number,Train_platform,From_station,To_station,Departure,Arrival,Available_seats)=train
            
            if from_station.lower()==From_station.lower() and to_station.lower()==To_station.lower():
                print(f"""
    "{Train_name}" Available !
*---------------------------------*
Train Number     :- {Train_number}
Departure Timing :- {Departure}
Arrival Timing   :- {Arrival}
*---------------------------------*""")
                
                # It will append the selected train in the train2[] list
                train2.append(train)
                found=True
                
        # If not found condition
        if not found:
            print(f"""
|  There is no train available from "{from_station}" to "{to_station}"  |""")
            return
        
        # Book ticket input
        book_t=input("\nDo you want to Book Tickets? (Yes/No)\nEnter :-  ").lower()

        # if input is "no"
        if book_t=="no":
            print("""
 --------------------------------------
|  Ticket Booking has been cancelled.  |
 --------------------------------------""")
        
        elif book_t!="yes" and book_t!="no":
            print("""
 -------------------------------------------
|  Please respond with "Yes" or "No" only.  |
 -------------------------------------------""")
        
        # If input is "yes"
        elif book_t=="yes":
            print("""
 -----------------------------------
|  Ticket Booking process started.  |
 -----------------------------------""")
            # Input train number
            while True:
                # with ( try except ) this will throw valueerror
                try:
                    train_number=int(input("\nEnter Train Number to Book :- "))
                    break
                except ValueError:
                    print("Please enter an Integer Value !")
            selected_train=None
            
            # Select train in train2[] list
            for t in train2:
                if t[1]==train_number:
                    selected_train=list(t)  # convert tuple → list
                    break
                
            # If selected is None
            if selected_train is None:
                print("""
 -------------------------------------------------
|  No train found with the entered train number.  |
 -------------------------------------------------""")
                return
            
            print(f"\nAvailable seats :- {selected_train[7]}")
            
            # Input for the no. of seats booking
            while True:
                try:
                    no_of_seats_book=int(input("\nHow many seats you want to book :- "))
                    if no_of_seats_book<=0:
                        print("""
|  Please Enter Seats more then 0 !  |""")
                        continue
                    break
                
                except ValueError:
                    print("Please enter an Integer Value !")
                    
            # Seat check
            if selected_train[7] < no_of_seats_book:
                print("""
|  Not enough seats available.  |""")
                return
            
            # Input Passengers details
            new_passengers=[]

            Booking_id=random.randint(10000,99999)
            # Checking Duplicate id
            while True:
                duplicate = False

                # Check existing bookings
                for booking in self.all_booked_tickets:
                    if Booking_id==booking["Booking ID"]:
                        duplicate=True
                        break

                # Generate another ID if duplicate is found
                if duplicate:
                    Booking_id=random.randint(10000, 99999)
                else:
                    break
    
            # for loop runs ("no_of_seats_book") times
            for i in range(no_of_seats_book):
                print(f"""
***********************
     Passenger {i+1}
***********************""")
                while True:
                    Name=input("Enter Name :- ")
                    # Checking Entered name
                    if Name.strip()=="":
                        print("""
 -------------------------------
|  Please enter a valid name !  |
 -------------------------------""")
                        continue
                    break
                
                # Checking email
                while True:
                    pattern_email=r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
                    Email=input("Enter E-mail :- ")
                    if not re.fullmatch(pattern_email,Email):
                        print("""
 -----------------
|  Invalid E-mail  |
 -----------------""")
                        continue
                    break
                
                # Checking Mobile Number
                while True:
                    pattern_mob_no=r"^[6-9]\d{9}$"
                    Mobile_Number=input("Enter Mobile Number :- ")
                    if re.fullmatch(pattern_mob_no,Mobile_Number):
                        break
                    else:
                        print("""
 -------------------------
|  Invalid Mobile Number  |
 -------------------------""")
                        continue

                print("Booking ID of this passenger is :- ", Booking_id)

                # append in new_passsengers[] list
                new_passengers.append({
                    "Booking ID": Booking_id,
                    "Name": Name,
                    "Email": Email,
                    "Mobile": int(Mobile_Number),
                    "Train Name": selected_train[0],
                    "Train Number": selected_train[1],
                    "Platform": selected_train[2],
                    "From": selected_train[3],
                    "To": selected_train[4],
                    "Departure": selected_train[5],
                    "Arrival": selected_train[6]
                })
                
            print("""
----------------------------------------
       Ticket Booked Successfully !
----------------------------------------""")
            # Extend new_passengers in __init__ ( Passengers[] and booked_tickets[] list ) variable
            self.passengers.extend(new_passengers)
            self.all_booked_tickets.extend(new_passengers)
            
            # Update seats in main Trains[] list
            for i in range(len(self.Trains)):
                if self.Trains[i][1]==selected_train[1]:
                    temp=list(self.Trains[i])
                    temp[7]=temp[7]-no_of_seats_book
                    self.Trains[i]=tuple(temp)
                    remaining=temp[7]
                    break
                
            self.save_trains()
            self.save_passengers()
            self.save_bookings()

    # ********** ----- ***** -----********** ----- ***** ----- View Booked Tickets Function ( User function ) ----- ***** ----- **********----- ***** ----- *

    def view_booked_tickets(self):
        found=False
        print(f"""
-------------------------
   View Booked Tickets
-------------------------""")
        
        # printing all details from the all_booked_tickets[] list
        for train in self.all_booked_tickets:
            print(f"""
Booking ID        : {train['Booking ID']}
Train Name        : {train['Train Name']}
Train Number      : {train['Train Number']}
Passengers Mobile : {train['Mobile']}
PassengersName    : {train['Name']}
Passengers E-mail : {train['Email']}
Seats Booked      : 1""")
            found=True
            
        # If not found condition
        if not found:
            print("There is no Booked Tickets...")

    # ********** ----- ***** -----********** ----- ***** ----- Generate Ticket Details Function ( User function ) ----- ***** ----- **********----- ***** ---

    def generate_ticket_details(self):
        found=False
        print("""
*****---------*****---------*****
-------- Ticket Details --------
*****---------*****---------*****""")
        
        # Printing all passengers Ticket details from passengers[] list
        i=0
        for passenger in self.passengers:
            print(f"""
           TICKET {i+1}
*-------------------------------*
Booking ID       : {passenger['Booking ID']}
Name             : {passenger['Name']}
Email            : {passenger['Email']}
Mobile Number    : {passenger['Mobile']}
Train Name       : {passenger['Train Name']}
Train Number     : {passenger['Train Number']}
Platform         : {passenger['Platform']}
From             : {passenger['From']}
To               : {passenger['To']}
Departure        : {passenger['Departure']}
Arrival          : {passenger['Arrival']}
Seats Booked     : 1
*-------------------------------*""")
            i=i+1
            found=True
            
        # If not found condition
        if not found:
            print("There is no Booked Tickets...")
        
    # ********** ----- ***** -----********** ----- ***** ----- Cancel Tickets Function ( User function ) ----- ***** ----- **********----- ***** ----- ******

    def cancel_ticket(self):
        cancel_t=input("\nDo you want to cancel ticket ( Yes/No ) ?\nEnter :- ").lower()
        
        # If no Condition
        if cancel_t=="no":
            print("""
 -------------------------------------------
|  Ticket Cancellation has been cancelled.  |
 -------------------------------------------""")

        elif cancel_t!="yes" and cancel_t!="no":
            print("""
 -------------------------------------------
|  Please respond with "Yes" or "No" only.  |
 -------------------------------------------""")
            
        elif cancel_t == "yes":
            total_cancel_ticket=input("\nHow many Bookings you want to Cancel :- ")

            # Validate integer input
            try:
                total_cancel_ticket = int(total_cancel_ticket)
            except ValueError:
                print("Please enter an integer value.")
                return

            if total_cancel_ticket <= 0:
                print("""
 -----------------------------------------
|  Please enter a number greater than 0.  |
 -----------------------------------------""")
                return

            for i in range(total_cancel_ticket):

                # Enter Booking ID
                try:
                    Booking_i_d = int(input(f"\nEnter Booking ID of booking {i+1} :- "))
                except ValueError:
                    print("Please enter a valid Booking ID.")
                    continue

                # Find all passengers with the same Booking ID
                matched_passengers = [
                    passenger
                    for passenger in self.passengers
                    if Booking_i_d == passenger["Booking ID"]
                ]

                if matched_passengers:
                    
                    # Restore seats for all passengers in this booking
                    for passenger in matched_passengers:
                        for j, train in enumerate(self.Trains):
                            if train[1] == passenger["Train Number"]:
                                temp = list(train)
                                temp[7] = temp[7] + 1
                                self.Trains[j] = tuple(temp)
                                break

                        # Remove passenger record
                        self.passengers.remove(passenger)

                    # Remove all associated booking records
                    self.all_booked_tickets = [
                        booking
                        for booking in self.all_booked_tickets
                        if booking["Booking ID"] != Booking_i_d
                    ]

                    print("""
 -----------------------------------
|  Ticket Cancelled Successfully !  |
 -----------------------------------""")

                    # Save updated data
                    self.save_trains()
                    self.save_passengers()
                    self.save_bookings()

                else:
                    print("""
 --------------------------------
|  Booking ID not found.         |
 --------------------------------""")




                                                # ***** ----- ***** ----- ADMIN FEATURES ----- ***** ----- *****

    # ********** ----- ***** -----********** ----- ***** ----- Create Account Function ( Admin function ) ----- ***** ----- **********----- ***** ----- *****

    def create_account(self):
        # Import Random and regular expression
        import re
        import random
        print("""
 ----------------------
|  ENTER YOUR DETAILS  |
 ----------------------""")
        
        # Enter Details For creating the account
        Name=input("Enter Name :- ")
        # Checking Entering name
        if Name.strip()=="":
            print("""
 --------------------------
|  Please enter the name.  |
 --------------------------""")
            return
        # Checking email
        pattern_email=r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        Email=input("Enter E-mail :- ")
        if not re.fullmatch(pattern_email,Email):
            print("""
 -----------------
|  Invalid E-mail  |
 -----------------""")
            return
        # Checking Mobile Number
        pattern_mob_no=r"^[6-9]\d{9}$"
        Mobile_Number=input("Enter Mobile Number :- ")
        if not re.fullmatch(pattern_mob_no,Mobile_Number):
            print("""
 -------------------------
|  Invalid Mobile Number  |
 -------------------------""")
            return
        # Making password Strong by pattern
        pattern_password=r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&*!])[A-Za-z\d@#$%^&*!]{8,}$"
        password=input("Create password :- ")
        if not re.fullmatch(pattern_password,password):
            print("""
 ----------------------------------------------------------------------------------------------------------------------------
|  Password must contain at least 8 characters , 1 uppercase letter , 1 lowercase letter , 1 digit and 1 special character.  |
 ----------------------------------------------------------------------------------------------------------------------------""")
            return
        # Input confirm password
        confirm_password=input("Confirm password :- ")
        # Creating admin ID
        admin_id=random.randint(10000,99999)
        
        # If not condition
        if confirm_password!=password:
            print("""
 -----------------------------------
|  Confirm Password is Incorrect !  |
 -----------------------------------""")
            return
        found=False
        
        # Comparing input in the admin_account_details[] list
        for admin_account in self.admin_account_details:
            if (admin_account['Admin ID']==admin_id or
                admin_account['E-mail'].lower()==Email.lower() or
                admin_account['Mobile']==int(Mobile_Number)):
                found = True
                break
            
        # If found condition
        if found:
            print("""
 ---------------------------------
|  User Already has an account !  |
 ---------------------------------""")   
        else:
            
            # Append details in admin_account_details[] list in the form of dict
            self.admin_account_details.append({
                'Admin ID':admin_id,
                'User Name':Name,
                'E-mail':Email,
                'Mobile':Mobile_Number,
                'Password':password})
            
            # printing for confirmation
            print(f"\n|  Admin Id Of {Name} is :- {admin_id}  |")
            print("""
 -----------------------------------
|   Account Created Successfully !  |
 -----------------------------------\n""")
        self.save_admins()

    # ********** ----- ***** -----********** ----- ***** ----- Login Account Function ( Admin function ) ----- ***** ----- **********----- ***** ----- ******

    def login_account(self):
        print("""
 ----------------------
|  ENTER YOUR DETAILS  |
 ----------------------""")
        
        # input Login details as per the Account
        admin_id=int(input("Enter Admin ID :- "))
        password=input("Enter Password :- ")
        
        # Comparing Input in the admin_account_details[] list
        for admin_account in self.admin_account_details:
            
            # if condition for the admin ID
            if admin_id==admin_account['Admin ID']:
                
                # if condition for the password
                if password==admin_account['Password']:
                    print(f"""
|  Welcome {admin_account['User Name']}!  |""")
                    return admin_id
                
                # else for the wrong password
                else:
                    print("""
 ---------------------------
|  Password is Incorrect !  |
 ---------------------------""")
                    return False
                
        # condition for the account not found
        print("""
 ----------------------------
|  ACCOUNT DOES NOT EXIST !  |
 ----------------------------""")
        return False

    # ********** ----- ***** -----********** ----- ***** ----- Add Trains Function ( Admin function ) ----- ***** ----- **********----- ***** ----- *********

    def adding_trains(self):
        print("""
 ---------------------------------------
|  ENTER TRAIN DETAILS YOU WANT TO ADD  |
 ---------------------------------------""")
        
        # input Details For The Adding Train
        train_name=str(input("Enter Train Name :- "))
        if train_name.strip()=="":
            print("""
 ---------------------------------
| Fill Train Name column , First! |
 ---------------------------------""")
            return

        # Train number must contain 4 or 5 digits               
        train_number=int(input("Enter Train Number :- "))
        if train_number<1000 or train_number>99999:
            print("""
 ------------------------------------
| Enter a 4 or 5 digit Train Number. |
 ------------------------------------""")
            return
        
        # Checking Duplicate train number
        for train in self.Trains:
            if train[1]==train_number:
                print("""
 -------------------------------------------------------------------
| Train Number already exists! Please enter another Train Number! |
 -------------------------------------------------------------------""")
                return

        # Checking Platform Number
        Platform=int(input("Enter Platform Number :- "))
        if Platform <= 0:
            print("""
 -------------------------------------
| Please enter a valid platform number. |
 -------------------------------------""")
            return

        # Input from station
        From=str(input("Enter From Station :- "))
        if From.strip()=="":
            print("""
 ------------------------------------------------------------------
| First Put the station from Where you want to start the jounrey ! |
 ------------------------------------------------------------------""")
            return

        # Input to station
        To=str(input("Enter To Station :- "))
        if To.strip()=="":
            print("""
 ------------------------------------------
| Enter the station Where you want to go ! |
 ------------------------------------------""")
            return

        # From and To stations can't Be same
        if From.strip().lower()==To.strip().lower():
            print("""
 ----------------------------------------------
| 'From' and 'To' stations cannot be the same! |
 ----------------------------------------------""")
            return

        # Departure Timing
        Departure=str(input("Enter departure Timing :- "))
        if Departure.strip()=="":
            print("""
 --------------------------------------
| Please enter a valid departure time. |
 --------------------------------------""")
            return

        # Arrival Timing
        Arrival=str(input("Enter Arrival Timing :- "))
        if Arrival.strip()=="":
            print("""
 ------------------------------------
| Please enter a valid Arrival time. |
 ------------------------------------""")
            return

        # Checking Avalaible seats
        Available_seats=int(input("Enter Available Seats :- "))
        if Available_seats<=0:
            print("""
 ---------------------------------------
| Please enter a valid number of seats. |
 ---------------------------------------""")
            return
        
        # Append train in the self.Trains[] list
        self.Trains.append((
            train_name,
            train_number,
            Platform,
            From,
            To,
            Departure,
            Arrival,
            Available_seats))
        
        # printing confirmation
        print("""
 ------------------------------
|  Train Added Successfully !  |
 ------------------------------""")
        self.save_trains()

    # ********** ----- ***** -----********** ----- ***** ----- Update Trains Details Function ( Admin function ) ----- ***** ----- **********----- ***** ----- *****

    def update_train_details(self):
        print("""
 -------------------------
|  UPDATE TRAINS DETAILS  |
 -------------------------
Which Train you want to Update ?""")
        
        # for updating train details input train number
        train_no=int(input("Enter Train Number :- "))
        found=False
        
        # check train number in train in self.Trains[] list
        for train in self.Trains:
            train=list(train)
            if train_no==train[1]:
                found=True
                train=tuple(train)
                
                # remove train
                self.Trains.remove(train)
                print("""
 -------------------------
|  Enter Updated Details  |
 -------------------------""")
                
                # Input Updated details      
                train_name=str(input("Enter Train Name :- "))
                train_number=int(input("Enter Train Number :- "))
                Platform=int(input("Enter Platform Number :- "))
                From=str(input("Enter From Station :- "))
                To=str(input("Enter To Station :- "))
                Departure=str(input("Enter departure Timing :- "))
                Arrival=str(input("Enter Arrival Timing :- "))
                Available_seats=int(input("Enter Available Seats :- "))
                
                # append updated details in the self.Trains[] list
                self.Trains.append((
                    train_name,
                    train_number,
                    Platform,
                    From,
                    To,
                    Departure,
                    Arrival,
                    Available_seats))
                print("""
 -----------------
|  Train Updated  |
 -----------------""")
                break
            
        # else condition for the Train number not found                        
        if not found:
            print("""
 ---------------------------------
|  This Train Number Not Found !  |
 ---------------------------------""")
        self.save_trains()
                                        
    # ********** ----- ***** -----********** ----- ***** ----- Removing Trains Function ( Admin function ) ----- ***** ----- **********----- ***** ----- ****

    def removing_train(self):
        found=False
        
        # for removing train input train number
        train_no=int(input("\nWhich Train you want to Remove (Enter Train Number) :- "))
        
        # check train number in the self.Trains[] list      
        for train in self.Trains:
            train=list(train)   
            if train_no==train[1]:           
                train=tuple(train)
                
                # remove train
                self.Trains.remove(train)
                
                # Confirmation Message
                print("Train Removed Successfully !")
                found=True
                break
            
        # If not f condition                  
        if not found:
            print("Train Number Not Found !")
        self.save_trains()

    # ********** ----- ***** -----********** ----- ***** ----- Viewing All Bookings Function ( Admin function ) ----- ***** ----- **********----- ***** -----

    def viewing_all_bookings(self):
        view_all_booking=False

        # finding booking from the all_booked_tickets
        for booking in self.all_booked_tickets:
            view_all_booking=True
            print(f"""
Booking ID        : {booking['Booking ID']}
Train Name        : {booking['Train Name']}
Train Number      : {booking['Train Number']}
Passengers Mobile : {booking['Mobile']}
PassengersName    : {booking['Name']}
Passengers E-mail : {booking['Email']}
Seats Booked      : 1""")
            
        # if not found condition
        if not view_all_booking:
            print("""
 --------------------------
|  No Booking Available !  |
 --------------------------""")

    # ********** ----- ***** -----********** ----- ***** ----- Delete login account ( Admin function ) ----- ***** ----- **********----- ***** -----

    def delete_account(self,admin_id):
        # importing random
        import random
        # inputting option ( Yes\No )
        yes_no=input("Are you sure you want to delete ?   ( yes / no )\nEnter :- ").lower()
        # If not 'yes','no' condition
        if yes_no!='yes' and yes_no!='no':
            print("""
 -------------------------------------------
 |  Please respond with "Yes" or "No" only.  |
 -------------------------------------------""")
            return False
        # If 'no' condition
        elif yes_no=='no':
            print("""
 ---------------------------------------
|  Account deletion has been canceled.  |
 ---------------------------------------""")
            return False
        # If 'yes' condition
        elif yes_no=="yes":
            
            # admin in admin_account_details[] list by for loop
            for admin in self.admin_account_details:
                # if admin_id of delete_account is equal to login_accout admin id 
                if admin['Admin ID']==admin_id:
                    # generate otp
                    otp=random.randint(10000,99999)
                    # appending otp in file
                    self.OTP.append(otp)
                    self.save_otp()
                    
                    # Enter otp
                    entered_otp=int(input("""
OTP for account deletion is sent to your registered Mobile Number!
Enter OTP For delete this account :- """))
                    # if entered_otp in self.otp file
                    if entered_otp in self.OTP:
                        # remove otp
                        self.OTP.remove(entered_otp)
                        self.save_otp()
                        # remove admin ( delete )
                        self.admin_account_details.remove(admin)
                        self.save_admins()
                        print("""
 ----------------------------------
|  Account deleted Successfully !  |
 ----------------------------------""")
                        return True
                    
                    # elif condition
                    elif entered_otp!=otp:
                        print("|  Incorrect OTP  |")
                        return False

if __name__ == "__main__":

    # Reference of Class object ( User Function )
    rms=RailwayManagementSystem()

        # ********** ----- ***** -----********** ----- ***** ----- Inputting ( Admin or User ) ----- ***** ----- **********----- ***** ----- **********----- *****

    while True:
        
        # Choosing [ Admin or User ] by input
        print("""
    +++++++++++++++++++++++++
    WELCOME TO INDIAN RAILWAY
    +++++++++++++++++++++++++

    ARE YOU A "USER" OR "ADMIN" ?     ||     EXIT = 0""")
        # Taking input
        user_admin=input("Enter :- ").lower().strip()

        # If input=0
        if user_admin=="0":
            print("""
    ----------------------------------------
    |  Thank You for Using Indian Railway!   |
    ----------------------------------------""")
            break
        
        # elif Condition when user and admin not correct
        elif user_admin!="user" and user_admin!="admin":
            print("""
    **-------------------------------------------------------**
    |   Invalid input. Please enter "User" or "Admin" only.   |
    **-------------------------------------------------------**""")

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ |   User Features   | +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        # elif Condition when Input is "User"
        elif user_admin=="user":

            # Starting of While condition
            count=True
            while count:
                
                print("""
                WELCOME TO INDIAN RAILWAY
    ------------------------------------------------
                    | OPTIONS |
    ----------------------------------------------
    || 1. Train Details                            ||
    || 2. Available Trains                         ||
    || 3. Check Seats Availability                 ||
    || 4. Book Tickets                             ||
    || 5. Cancel Tickets                           ||
    || 6. View Booked Tickets                      ||
    || 7. Generate Ticket Details                  ||
    || 8. EXIT                                     ||
    ----------------------------------------------""")

                # Exeption handling starting (try)
                try:
                
                    # Input Button
                    button=int(input("\nENTER YOUR OPTION :- "))

                    # Calling View Train Details ( User Function )
                    if button==1:
                        rms.train_details()

                    # Calling View Available Trains ( User Function )
                    elif button==2:
                        rms.available_trains()

                    # Calling Check Seat Availability ( User Function )
                    elif button==3:
                        rms.available_seats()

                    # Calling Book Tickets ( User Function )
                    elif button==4:
                        rms.book_tickets()

                    # Calling Cancel Tickets ( User Function )
                    elif button==5:
                        rms.cancel_ticket()

                    # View Booked Tickets ( User Function )
                    elif button==6:
                        rms.view_booked_tickets()

                    # Generate Ticket Details ( User Function )
                    elif button==7:
                        rms.generate_ticket_details()

                    # Exit ( User Function )
                    elif button==8:
                        count=False
                        print("""
    ------------------------------------------
    |  Thank You , For using Indian Railway !  |
    ------------------------------------------""")
                        break
                        
                    # Invalid input output ( User Function )
                    else:
                        print("""
    --------------------
    |  Invalid Option !  |
    --------------------""")

                # exception handling (except)
                except ValueError:
                    print("""
    ----------------------------------
    |  Please enter an integer value.  |
    ----------------------------------""")


                    

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ |   Admin Features   | +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        # elif Condition when Input is "Admin"
        elif user_admin=="admin":

            # Starting of While condition
            count=True
            while count:

                print("""
    --------------------------------------
    |             | OPTIONS |              |
    --------------------------------------
    ||  1. Create Account                 ||
    ||  2. Login Account                  ||
    ||  3. EXIT                           ||
    --------------------------------------""")

                # Exeption handling starting (try)
                try:
                
                    # input button
                    button=int(input("\nENTER YOUR OPTION :- "))

                    # Calling Create account ( Admin Function )
                    if button==1:
                        rms.create_account()

                    # Calling Login account ( Admin Function )
                    elif button==2:
                        login_id=rms.login_account()
                        # if login
                        if login_id:

                            # while condition for login account ( Admin Function )
                            while True:
                                print("""
    ------------------------------------------
    |                 OPTIONS                  |
    ------------------------------------------
    ||  1. Add Trains                         ||
    ||  2. Update Trains                      ||
    ||  3. Remove Trains                      ||
    ||  4. View All Bookings                  ||
    ||  5. Delete account                     ||                  
    ||  6. LOG OUT                            ||
    ------------------------------------------""")

                                # input button
                                option=int(input("\nENTER YOUR OPTION :- "))

                                # Calling Adding Train ( Admin [ Login ] Function )
                                if option==1:
                                    rms.adding_trains()

                                # Calling Updating Train ( Admin [ Login ] Function )
                                elif option==2:
                                    rms.update_train_details()

                                # Calling Removing Train ( Admin [ Login ] Function )
                                elif option==3:
                                    rms.removing_train()

                                # Calling Viewing all bookings ( Admin [ Login ] Function )
                                elif option==4:
                                    rms.viewing_all_bookings()

                                # Calling delete account ( Admin [ Login ] Function )
                                elif option==5:
                                    # if rms.delete_account(login_id) will correct
                                    if rms.delete_account(login_id):
                                        break

                                # Exit Function ( Admin [ Login ] Function )
                                elif option==6:
                                    print("Logged Out Successfully !")
                                    break

                                # Invalid input Output ( Admin [ Login ] Function )
                                else:
                                    print("Invalid option ! Please try again Later.")

                    # Exiting login Function [ Admin Function ]
                    elif button==3:
                        count=False
                        print("""
    ---------------------------
    |  Thank You for Coming...  |
    ---------------------------""")
                        break

                    # Invalid Input output ( Admin Function )
                    else:
                        print("Invalid Option !")

                # exception handling (except)
                except ValueError:
                    print("""
    ----------------------------------
    |  Please enter an integer value.  |
    ----------------------------------""")