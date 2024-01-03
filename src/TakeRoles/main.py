import datetime
import mariadb
import discord


""" 
Redeem_date beim Einlösung. Ab dann 1 Monat bis die Rolle automatisch weggenommen wird. 

Der Bot muss die Daten von dem Redeem_date lesen und dann die Rolle wegnehmen. 

fetchall(REDEEMED_AT) dates und wenn eine REDEEMED_AT date mit now() übereinstimmt dann nimm rolle weg.

"""


class DateHandler:
    def __init__(self, con):
        self.con = mariadb.connect(
        user="ole",
        password="QrsoL82",
        host="192.168.10.183",
        port=3306,
        database="BunnyDB",
        
        cur = con.cursor()    
    )


    def read_date(self):
        # Read the date from the database
        cursor = self.con.cursor()
        cursor.execute("SELECT REDEEMED_AT FROM CodeRedeemLogs")
        date = cursor.fetchone()[0]

        return date

    def perform_task(self, date):
        # Do something with the date
        print(f"Processing date:", {date})

        discord.Guild.fetch_members()
        

    def run(self):
        # Read the date from the database
        date = self.read_date()

        # Parse the date into a datetime object
        parsed_date = datetime.datetime.strptime(date, '%Y-%m-%d')

        # Do something with the date
        self.perform_task(parsed_date)
