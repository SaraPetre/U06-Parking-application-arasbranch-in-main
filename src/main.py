"""Parking application"""
#from tkinter import *
#from email.mime import image
from tkinter import Label, Toplevel, StringVar, Entry, END, Button, messagebox, Tk, Canvas, Image
import sqlite3
from time import strftime
import re
from tkinter import Tk, Canvas
from tkinter import messagebox
from PIL import ImageTk, Image

# Create root window
rootA = Tk()
# root title
rootA.title("Parking application")
# root size and not resizable
rootA.geometry("620x650")
rootA.resizable(width=False, height=False)
# background color for window
rootA.configure(bg="#F5F5F5")
# icon for application window
rootA.iconbitmap('phouse.ico')

# Parking spaces variable
TOTAL_PARKING_SPACES = 50


# Function to show date and keep time dynamic at root
def current_time_date():
    """This function is for the main menu (root).

    It keeps the time dynamic and stores it in the time_label.

    The function also shows the current date and stores it in the date_label."""
    my_time = strftime(' Local time: %H:%M:%S')
    time_label.config(text=str(my_time), font=("Verdana", 10), fg="White", bg="black")
    time_label.after(1000, current_time_date)
    todays_date = strftime('Date: %d/%m/%y')
    date_label.config(text=str(todays_date), font=("Verdana", 10), fg="White", bg="black")


# Function to show info about prices (connected to the 'View price list'-button)
def prices():
    """This function shows the price list when the 'View price list'-button is clicked.
    The price list appears in a messagebox.showinfo"""

    messagebox.showinfo("Price list", "Minute 0-60 are FREE of charge.\n\n"
                        "From minute 61 onwards the price is 0.25 SEK/min\n(15 SEK/hour).")


# Function that takes user to new window after clicking on start parking in root menu (connected to 'Start parking'-button)
def start_parking():
    """The start_parking function is activated when the user clicks on start parking button in the main menu.
    The purpose of the function is to insert a registration number into the tables and start parking session for a car.

    First it creates a new window, named start_pop_up. While inside start_pop_up the root buttons gets disabled.

    In this window the user has to type in a registration number that is limited to 6 upper case characters in the entrybox.
    If the reg num is valid and unique it gets inserted into to car and parked_cars table with reg num and start time.
    If the reg num is invalid --> messagebox(showerror).
    If the reg num is valid and not unique --> messagebox(showerror).

    When the parking session is started successfully, start_pop_up closes, root button gets activated and parking spaces decreases by 1.
    """
    # Create new window called start_pop_up for start parking-button
    start_pop_up = Toplevel(rootA)
    start_pop_up.iconbitmap('phouse.ico')
    start_pop_up.title("Start parking")
    start_pop_up.geometry("400x200")
    start_pop_up.resizable(width=False, height=False)
    start_pop_up.config(bg="#F5F5F5")

    # Disable root menu buttons while inside start_pop_up
    def disable_main_buttons():
        start_parking_button.config(state='disabled')
        stop_parking_button.config(state='disabled')
        status_parking_button.config(state='disabled')
    disable_main_buttons()

    # function to activate root menu buttons
    def activate_root_buttons():
        start_parking_button.config(state='normal')
        stop_parking_button.config(state='normal')
        status_parking_button.config(state='normal')

    # Label with the text that asks for users reg num.
    def create_labels():
        regnum_label = Label(start_pop_up, text="Please enter your registration number", font=("Verdana", 11), fg="black", bg='#F5F5F5')
        regnum_label.pack(pady=20)
    create_labels()

    # Entry box for user to type in reg num
    entry_text = StringVar()
    entry_regnum = Entry(start_pop_up, width=10, borderwidth=4, font=("Verdana", 9), textvariable=entry_text)
    entry_regnum.pack()

    # Function that limits reg num entry to 6 upper case characters.
    def character_limit(entry_text):
        if len(entry_text.get()) > 0:
            entry_text.set(entry_text.get().upper()[:6])
    entry_text.trace("w", lambda *args: character_limit(entry_text))

    # Function for when start button inside start_pop_up is clicked
    def start_click():
        global TOTAL_PARKING_SPACES
        date_time = strftime("%m/%d/%Y, %H:%M:%S")

        # Create a connection to DB
        connection = sqlite3.connect('park.db')

        # Create cursor
        cursor = connection.cursor()

        # Enable foreign keys
        # cur.execute("PRAGMA foreign_keys=1")

        # Check if reg num is valid
        regnum = entry_text.get()
        if re.match(r"^[A-Za-z]{3}[0-9]{2}[0-9A-Za-z]{1}$", regnum):
            # Check if reg num is already in the database, if yes -> showerror.
            cursor.execute("SELECT car_id FROM car WHERE car_id=?", (regnum,))
            result = cursor.fetchone()
            if result:
                messagebox.showerror(title='Already in use,', message=f'{regnum} is already in use!\nPlease try again with a different registration number.')
                start_pop_up.destroy()
                activate_root_buttons()
            # If reg num is valid and unique insert into car and parked_cars table
            else:
                cursor.execute("INSERT INTO car (car_id) VALUES (?)", (regnum,))
                cursor.execute("INSERT INTO parked_cars (parked_car) VALUES (?)", (regnum,))
                TOTAL_PARKING_SPACES -= 1
            # Commit changes
                connection.commit()
            # Clear entry box
                entry_regnum.delete(0, END)
                park_space_label.config(text='Available spots: ' + str(TOTAL_PARKING_SPACES))
                messagebox.showinfo(title='Park started', message=f'Parking for {regnum} started at {date_time}')
        else:
            messagebox.showerror(title='Not valid', message=f'{regnum} is not a valid registration number\nPlease try again.')
            entry_regnum.delete(0, END)
        # Close window and activate root menu buttons
        start_pop_up.destroy()
        activate_root_buttons()

    # Create start button for start_pop_up
    start_button = Button(start_pop_up, command=start_click, height=0, width=30, relief="solid", text="Start parking", font=('Verdana', 10), fg='#F5F5F5', bg='#2E8B57')
    start_button.pack(pady=20)

    # Activate root buttons and close start_pop_up page when clicking 'X' on Windows Manager
    def on_close():
        start_parking_button.config(state='normal')
        stop_parking_button.config(state='normal')
        status_parking_button.config(state='normal')
        start_pop_up.destroy()

    start_pop_up.protocol("WM_DELETE_WINDOW", on_close)


# Function to see parked car status (connected to 'See status for parked car'-button)
def car_status():
    """The car_status function is activated when the user clicks on see status for parked button in the main menu.
    The purpose of the function is to look for a registration number in the db-tables and show value for the chosen reg num.

    First it creates a new window, named status_pop_up. While inside status_pop_up the root buttons gets disabled.
    After the user click on 'check status'-button the 'check status'-button gets disabled.

    In this window the user has to type in a registration number that is limited to 6 upper case characters in the entrybox.
    If the reg num is valid and in the db --> reg num, start time, stop time, total time and price will be shown for the chosen reg num.
    If the reg num is invalid --> messagebox(showerror).
    If the reg num is valid and not in the db --> messagebox(showerror).
    """
    # global status_pop_up
    status_pop_up = Toplevel(rootA)

    # Remove Windows Manager bar
    # status_pop_up.overrideredirect(True)

    status_pop_up.iconbitmap('phouse.ico')
    status_pop_up.title("Status for parked car")
    status_pop_up.geometry("400x350")
    status_pop_up.resizable(width=False, height=False)
    status_pop_up.config(bg="#F5F5F5")

    start_parking_button.config(state='disabled')
    stop_parking_button.config(state='disabled')
    status_parking_button.config(state='disabled')

    # function to activate root menu buttons
    def activate_root_buttons():
        start_parking_button.config(state='normal')
        stop_parking_button.config(state='normal')
        status_parking_button.config(state='normal')

    # Label for the text that asks for users reg num.
    regnum_label = Label(status_pop_up, text="Please enter your registration number", font=("Verdana", 11), fg="black", bg='#F5F5F5')
    regnum_label.pack(pady=20)

    # Entry for reg num.
    # global entry_text_status
    # global entry_regnum_status
    entry_text_status = StringVar()
    entry_regnum_status = Entry(status_pop_up, width=10, borderwidth=4, font=("Verdana", 9), textvariable=entry_text_status)
    entry_regnum_status.pack()

    # Function that limits reg num entry to 6 upper case characters.
    def character_limit(entry_text):
        if len(entry_text.get()) > 0:
            entry_text.set(entry_text.get().upper()[:6])
    entry_text_status.trace("w", lambda *args: character_limit(entry_text_status))

    # Funcion when 'check status'-button is clicked.
    def status_click():
        # Disable 'check status'-button when info about car is shown
        status_button.config(state='disabled')
        # Create a connection to DB
        con = sqlite3.connect('park.db')

        # Create cursor
        cursor = con.cursor()

        # Variable to store inputed reg num
        regnum = entry_text_status.get()

        # Check if regnum has valid format
        if re.match(r"^[A-Za-z]{3}[0-9]{2}[0-9A-Za-z]{1}$", regnum):
            # Get total parked time for a parked_car and store it in variable parked_time
            cursor.execute("SELECT CAST ((JulianDay('now','localtime') - JulianDay(start_time)) * 24 * 60 AS Integer) FROM parked_cars WHERE parked_car=?", (regnum,))
            parked_time = cursor.fetchone()
            # Select the right car by its regnum to check its status
            cursor.execute("SELECT * FROM parked_cars WHERE parked_car=?", (regnum,))
            car_info = cursor.fetchone()
            # If regnum is in db
            if car_info:
                # Variables to store reg num, start/stop time and price
                car_reg = "Registration number: " + str(car_info[0])
                start_time = "Start date and time:" + str(car_info[1])
                stop_time = "Stop date and time: " + str(car_info[2])
                # Show total parking time, if time < 60min show in minutes, if time > 60min show in hours
                if parked_time[0] <= 59:
                    total_time = "Total parking time: " + str(parked_time[0]) + ' minutes'
                elif parked_time[0] >= 60:
                    total_time = "Total parking time: " + str(round(parked_time[0] / 60, 1)) + ' hours'

                # Variable for pricing for a parked car (0-60min FREE)
                if parked_time[0] <= 60:
                    price = "Price: " + str(parked_time[0] * 0) + ' SEK'
                # Price for 61 min onwards ---> 0.25kr/min, REMOVES FIRST FREE HOUR)
                elif parked_time[0] >= 61:
                    price = "Price: " + str((parked_time[0] - 60) * (0.25)) + ' SEK'

                # Labels for the variables above
                car_reg_label = Label(status_pop_up, text=car_reg, bg='#F5F5F5', font=("Verdana", 11))
                car_reg_label.pack()
                start_time_label = Label(status_pop_up, text=start_time, bg='#F5F5F5', font=("Verdana", 11))
                start_time_label.pack()
                stop_time_label = Label(status_pop_up, text=stop_time, bg='#F5F5F5', font=("Verdana", 11))
                stop_time_label.pack()
                total_time_label = Label(status_pop_up, text=total_time, bg='#F5F5F5', font=("Verdana", 11))
                total_time_label.pack()
                price_label = Label(status_pop_up, text=price, bg='#F5F5F5', font=("Verdana", 11))
                price_label.pack()

                # Clear entry box after click on 'check status'
                entry_regnum_status.delete(0, END)
            # If regnum is valid but not in db, show error message.
            elif not car_info:
                messagebox.showerror(title='Car not found', message=f'Car with registration number: {regnum} not found')
                status_pop_up.destroy()
                activate_root_buttons()
        # If regnum is not in valid format, show error message.
        else:
            messagebox.showerror(title='Not valid', message=f'{regnum} is not a valid registration number\nPlease try again.')
            entry_regnum_status.delete(0, END)
            status_pop_up.destroy()
            activate_root_buttons()
        # Commit changes
        con.commit()

    # Create status button for status_pop_up
    status_button = Button(status_pop_up, command=status_click, height=0, width=30, relief="solid", text="Check status", font=('Verdana', 10), fg='#F5F5F5', bg='#3466a5')
    status_button.pack(pady=20)

    # Function to activate root buttons and close status_pop_up page when clicking 'X' on the Windows Manager.
    def on_close():
        start_parking_button.config(state='normal')
        stop_parking_button.config(state='normal')
        status_parking_button.config(state='normal')
        status_pop_up.destroy()
    status_pop_up.protocol("WM_DELETE_WINDOW", on_close)

def stop_parking():
      # Create new window called start_pop_up for stop parking-button
    stop_pop_up = Toplevel(rootA)
    stop_pop_up.iconbitmap('phouse.ico')
    stop_pop_up.title("Stop parking")
    stop_pop_up.geometry("400x350")
    stop_pop_up.resizable(width=False, height=False)
    stop_pop_up.config(bg="#F5F5F5")

    # Disable root menu buttons while inside start_pop_up
    def disable_main_buttons():
        start_parking_button.config(state='disabled')
        stop_parking_button.config(state='disabled')
        status_parking_button.config(state='disabled')
    disable_main_buttons()

    # function to activate root menu buttons
    def activate_root_buttons():
        start_parking_button.config(state='normal')
        stop_parking_button.config(state='normal')
        status_parking_button.config(state='normal')

    # Label with the text that asks for users reg num.
    def create_labels():
        regnum_label = Label(stop_pop_up, text="Please enter your registration number", font=("Verdana", 11), fg="black", bg='#F5F5F5')
        regnum_label.pack(pady=20)
    create_labels()

    # Entry box for user to type in reg num
    entry_text_stop = StringVar()
    entry_regnum_stop = Entry(stop_pop_up, width=10, borderwidth=4, font=("Verdana", 9), textvariable=entry_text_stop)
    entry_regnum_stop.pack()

    # Function that limits reg num entry to 6 upper case characters.
    def character_limit(entry_text):
        if len(entry_text.get()) > 0:
            entry_text.set(entry_text.get().upper()[:6])
    entry_text_stop.trace("w", lambda *args: character_limit(entry_text_stop))

    # Function for when stop button inside stop_pop_up is clicked
    def stop_click():
        # Disable 'stop'-button when info about car is shown
        stop_button.config(state='disabled')

        global TOTAL_PARKING_SPACES
        #date_time = strftime("%m/%d/%Y, %H:%M:%S")

        # Create a connection to DB
        connection = sqlite3.connect('park.db')

        # Create cursor
        cursor = connection.cursor()

        # Enable foreign keys
        # cur.execute("PRAGMA foreign_keys=1")

        # Variable to store inputed reg num
        regnum = entry_text_stop.get()

        # Check if reg num is valid
        if re.match(r"^[A-Za-z]{3}[0-9]{2}[0-9A-Za-z]{1}$", regnum):
            # Check if reg num is in the database, if no -> showerror.
            cursor.execute("SELECT car_id FROM car WHERE car_id=?", (regnum,))
            result = cursor.fetchone()
            print(result)
            print(type(result))
            if result:
                cursor.execute("UPDATE parked_cars SET stop_time=(DATETIME('now','localtime')) where parked_car=?", (regnum,))
                cursor.execute("SELECT CAST ((julianday(stop_time) - julianday(start_time))* 24* 60 AS INTEGER) FROM parked_cars WHERE parked_car = ?", (regnum,))
                # # cursor.execute("SELECT start_time, stop_time FROM parked_cars WHERE parked_car=?", (regnum,))
                # start_stop = cursor.fetchone()
                # print(start_stop)
                parked_time = cursor.fetchone()
                print(type(parked_time))
                delimeter= ','
                parked_time_join=delimeter.join([str(value) for value in parked_time])
                print(parked_time_join)
                update_query="UPDATE parked_cars SET total_time=? where parked_car=?"
                data=(parked_time_join, regnum)
                cursor.execute(update_query, data)

                cursor.execute("SELECT CAST(((total_time)-60) * (0.25) AS INTEGER)from parked_cars WHERE parked_car=?", (regnum,))
                result_total_time=cursor.fetchone()
                print(result_total_time)
                delimeter= ','
                result_total_time_join=delimeter.join([str(value) for value in result_total_time])
                print(result_total_time_join)
                update_query="UPDATE parked_cars SET price=? where parked_car=?"
                data=(result_total_time_join, regnum)
                cursor.execute(update_query, data)
            # If reg num is valid but not in database
            else:
                messagebox.showerror(title='Not registered,', message=f'{regnum} has not started parking!\nPlease try again with a different registration number.')
                stop_pop_up.destroy()
                activate_root_buttons()   
         
            # Select the right car by its regnum to check its parking summary
            def parking_summary():
                cursor.execute("SELECT * FROM parked_cars WHERE parked_car=?", (regnum,))
                car_info = cursor.fetchone()
                #print(car_info)
                # If regnum is in db
                if car_info:
                    # Variables to store reg num, start/stop time and price
                    car_reg = "Registration number: " + str(car_info[0])
                    start_time = "Start date and time:" + str(car_info[1])
                    stop_time = "Stop date and time: " + str(car_info[2])
                    # Show total parking time, if time < 60min show in minutes, if time > 60min show in hours
                    if parked_time[0] <= 59:
                        total_time = "Total parking time: " + str(parked_time[0]) + ' minutes'
                        ######cursor.execute("UPDATE parked_cars SET total_time=?", (total_time,))
                    elif parked_time[0] >= 60:
                        total_time = "Total parking time: " + str(round(parked_time[0] / 60, 1)) + ' hours'

                    # Variable for pricing for a parked car (0-60min FREE)
                    if parked_time[0] <= 60:
                        price = "Price: " + str(parked_time[0] * 0) + ' SEK'
                    # Price for 61 min onwards ---> 0.25kr/min, REMOVES FIRST FREE HOUR)
                    elif parked_time[0] >= 61:
                        price = "Price: " + str((parked_time[0] - 60) * (0.25)) + ' SEK'

                    # Labels for the variables above
                    car_reg_label = Label(stop_pop_up, text=car_reg, bg='#F5F5F5', font=("Verdana", 11))
                    car_reg_label.pack()
                    start_time_label = Label(stop_pop_up, text=start_time, bg='#F5F5F5', font=("Verdana", 11))
                    start_time_label.pack()
                    stop_time_label = Label(stop_pop_up, text=stop_time, bg='#F5F5F5', font=("Verdana", 11))
                    stop_time_label.pack()
                    total_time_label = Label(stop_pop_up, text=total_time, bg='#F5F5F5', font=("Verdana", 11))
                    total_time_label.pack()
                    price_label = Label(stop_pop_up, text=price, bg='#F5F5F5', font=("Verdana", 11))
                    price_label.pack()

                    # Clear entry box after click on 'stop parking'
                    entry_regnum_stop.delete(0, END)
                # If regnum is valid but not in db, show error message.
                # elif not car_info:
                #     messagebox.showerror(title='Car not found', message=f'Car with registration number: {regnum} not found')
                #     stop_pop_up.destroy()
                #     activate_root_buttons()

            parking_summary()
        # If regnum is not in valid format, show error message.
        else:
            messagebox.showerror(title='Not valid', message=f'{regnum} is not a valid registration number\nPlease try again.')
            entry_regnum_stop.delete(0, END)
            stop_pop_up.destroy()
            activate_root_buttons()


       
        # Commit changes
        connection.commit()
        connection.close()

    # Create stop button for stop_pop_up
    stop_button = Button(stop_pop_up, command=stop_click, height=0, width=30, relief="solid", text="Stop parking", font=('Verdana', 10), fg='#F5F5F5', bg='#2E8B57')
    stop_button.pack(pady=20)

 # Label with the text that asks for users mailadress.
    def mail_labels():
        mail_label = Label(stop_pop_up, text="Please enter your emailadress", font=("Verdana", 11), fg="black", bg='#F5F5F5')
        mail_label.pack(pady=20)
        

        # Entry box for user to type in mailaddress
        entry_mail = StringVar()
        entry_mail = Entry(stop_pop_up, width=10, borderwidth=4, font=("Verdana", 9), textvariable=entry_text_stop)
        entry_mail.pack()

    # Clear entry box after click on 'email'
        entry_mail.delete(0, END)   
        mail_labels()

    # Activate root buttons and close stop_pop_up page when clicking 'X' on Windows Manager
    def on_close():
        start_parking_button.config(state='normal')
        stop_parking_button.config(state='normal')
        status_parking_button.config(state='normal')
        stop_pop_up.destroy()

    stop_pop_up.protocol("WM_DELETE_WINDOW", on_close)


# ###################################################################
# Create picture for header
park_image = Image.open("phouse.png")
# resize picture to fit for the window
resized = park_image.resize((190, 140), Image.ANTIALIAS)
new_image = ImageTk.PhotoImage(resized)
# Create label for picture and place it on the grid
lab = Label(rootA, image=new_image, borderwidth=0)
lab.grid(row=0, column=0, sticky='n')
# #######################################################################
# Create main menu (root) buttons and their location on the grid
see_prices_button = Button(rootA, command=prices, height=1, width=70, relief="solid", text="View price list", font=('Verdana', 10), fg='#F5F5F5', bg='#36454F')
see_prices_button.grid(padx=30, pady=5, row='4', column='0', sticky='w')

start_parking_button = Button(rootA, command=start_parking, height=2, width=20, relief="solid", text="Start parking", font=('Verdana', 10), fg='#F5F5F5', bg='#2E8B57')
start_parking_button.grid(padx=30, pady=15, row='5', column='0', sticky='w')

status_parking_button = Button(rootA, command=car_status, height=2, width=22, relief="solid", text="See status for parked car", font=('Verdana', 10), fg='#F5F5F5', bg='#3466a5')
status_parking_button.grid(padx=30, pady=15, row='5', column='0', sticky='n')

stop_parking_button = Button(rootA, command=stop_parking, height=2, width=20, relief="solid", text="Stop parking", font=('Verdana', 10), fg='#F5F5F5', bg='#8f1d21')
stop_parking_button.grid(padx=30, pady=15, row='5', column='0', sticky='e')

# Create black line below logo
c = Canvas(rootA, height=22, width=620, bg="black")
c.grid(row=1, column=0)

# Create labels
welcome_label = Label(rootA, text="Welcome to YourPark!\n\nPlease choose from the options below..", font=('Verdana', 10), bg='#F5F5F5', fg="black")
welcome_label.grid(row=3, column=0, sticky='n', padx=10, pady=10)
time_label = Label(rootA)
time_label.grid(row=1, column=0, sticky='w')
date_label = Label(rootA)
date_label.grid(row=1, column=0, sticky='e', padx=13)
park_space_label = Label(rootA, text='Available spots: ' + str(TOTAL_PARKING_SPACES), font=('Verdana', 10), fg="#FFBF00", bg='black')
park_space_label.grid(row=1, column=0, sticky='')

# Call time and date function for root menu
current_time_date()

# Create a connection to DB
conn = sqlite3.connect('park.db')

# Create cursor
cur = conn.cursor()

# Update total parking spaces depending on amount of parked cars stored i the db.
cur.execute("SELECT COUNT (*) FROM parked_cars")
parked_cars_amount = cur.fetchall()
TOTAL_PARKING_SPACES = TOTAL_PARKING_SPACES - parked_cars_amount[0][0]
park_space_label.config(text='Available spots: ' + str(TOTAL_PARKING_SPACES))

# Enable foreign keys
cur.execute("PRAGMA foreign_keys=1")


# SQL COMMANDS: Create the tables for database
def create_tables():
    """This function is used to create the tables for db"""
    # Driver table

    cur.execute("""CREATE TABLE IF NOT EXISTS driver (
        email TEXT PRIMARY KEY NOT NULL
            )""")

    # Car table
    cur.execute("""CREATE TABLE IF NOT EXISTS car (
        car_id TEXT(6) PRIMARY KEY NOT NULL,
        email TEXT,
        FOREIGN KEY (email) REFERENCES driver(email)
            )""")

    # Parked cars table
    cur.execute("""CREATE TABLE IF NOT EXISTS parked_cars (
        parked_car TEXT(6) UNIQUE NOT NULL,
        start_time timestamp DATETIME DEFAULT (datetime('now','localtime')),
        stop_time DATETIME DEFAULT 'ACTIVE',
        total_time INT,
        price INT,
        FOREIGN KEY (parked_car) REFERENCES car (car_id)
            )""")

# Defination to delete row after stop of parking
# def delete_task():
#     """
#     Delete a task by task id
#     :param conn:  Connection to the SQLite database
#     :param id: id of the task
#     :return:
#     """
#     sql = 'DELETE FROM parked_cars WHERE parked_car=?'
#     cur = conn.cursor()
#     cur.execute(sql, (regnum,))
#     conn.commit()
#     delete_task()

# Call the create tables function
# create_tables()

# Commit changes
conn.commit()

# Close connection
conn.close()

# Run tkinter window
rootA.mainloop()
