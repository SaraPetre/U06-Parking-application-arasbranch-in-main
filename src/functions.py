import sqlite3
import smtplib
import requests
import pandas as pd
from pyfiglet import Figlet
from tabulate import tabulate

def mailhog():
    """
    This funktion sends an email with the recipie inforamtion about 
    """
    f_f = Figlet(font='slant')
    print(f_f.renderText('Parking receipt!'))
    url_figlet = (f_f.renderText("Parking receipt!"))
    # create database object to connect
    # the database db_coins.db
    conn = sqlite3.connect("park.db", isolation_level=None, detect_types=sqlite3.PARSE_COLNAMES)
    db_df = pd.read_sql_query("SELECT * FROM parked_cars", conn)
    # db_df = pd.read_sql_query("SELECT name 'Name', symbol 'Symbol',price_usd 'Price(USD)', change_1h_percent '1h %', change_24h_percent '24h %', change_7d_percent '7 day %',last_updated 'Last update' FROM coins", conn)
    df_create_table = pd.DataFrame(db_df)

    to_addr_input=input("Enter your email")
    to_addr=to_addr_input
    def pdtabulate(df_d):
        return tabulate(df_d, headers='keys', tablefmt='rst', showindex=False)
    url = pdtabulate(df_create_table)
    print(pdtabulate(df_create_table))

 
    from_addr = "reciept@park.yes"
    to_addr = "test@to.to"
    subject = "Reciept summary!"

    msg = f"From: {from_addr}\r\nSubject: {subject}\r\nTo: {to_addr}\r\n\r\n This is a message from MailHog.py. \n Find down below the daily prices for the top10 crypto coins! \n\n {url_figlet}\n\n{url}."
    server = smtplib.SMTP("localhost:1025")
    server.sendmail(from_addr, to_addr, msg)
mailhog()

print("\n\nThe reciept have been sent! \n\nCheck out the MailHog mail!! You can click and follow the down below link to open the mail in your browser.\n")
print("http://localhost:8025/")
input("\nPress enter to continue to main menu!")