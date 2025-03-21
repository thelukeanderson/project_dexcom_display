#!/usr/bin/env python3

import tkinter as tk
from datetime import datetime
import time
from pydexcom import Dexcom
from login_helper import get_user_credentials
import argparse
import math

class DexcomGlucoseDisplay:
    def __init__(self, master):
        self.master = master
        self.master.title("Dexcom Display")

        # Set up grid layout
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_columnconfigure(2, weight=1)

        # Create a label to display the dexcom last glucose reading
        self.last_reading_label = tk.Label(self.master, fg="green", bg="black", text="---", font=("Helvetica", 36))
        self.last_reading_label.grid(row=1, column=0, pady=(20, 10), columnspan=2)
        
        # Create a label to display the reading time
        self.show_reading_time_label = tk.Label(self.master, fg="green", bg="black", text="---", font=("Helvetica", 36))
        self.show_reading_time_label.grid(row=2, column=0, pady=(20, 10))
        
        # Create a label to display the current time
        self.show_current_time_label = tk.Label(self.master, fg="green", bg="black", text="---", font=("Helvetica", 36))
        self.show_current_time_label.grid(row=2, column=1, pady=(20, 10))
        
        # Create a label to display the reading time
        self.last_1_hour_label = tk.Label(self.master, fg="green", bg="black", text="---", font=("Helvetica", 36))
        self.last_1_hour_label.grid(row=0, column=0, pady=(20, 10))
        
        # Create a label to display the current time
        self.last_24_hour_label = tk.Label(self.master, fg="green", bg="black", text="---", font=("Helvetica", 36))
        self.last_24_hour_label.grid(row=0, column=1, pady=(20, 10))

        # Bind window resize event to adjust font size
        self.master.bind("<Configure>", self.adjust_font_size)

    def adjust_font_size(self, event):
        width = self.master.winfo_width()
        reading_font_size = max(int(width / 5), 12)  
        time_font_size = max(int(width / 25), 12)  
        average_reading_font_size = max(int(width / 10), 12)  
        self.last_reading_label.config(font=("Helvetica", reading_font_size))
        self.show_reading_time_label.config(font=("Helvetica", time_font_size))
        self.show_current_time_label.config(font=("Helvetica", time_font_size))
        self.last_1_hour_label.config(font=("Helvetica", average_reading_font_size))
        self.last_24_hour_label.config(font=("Helvetica", average_reading_font_size))


def calculate_average(dexcom, minutes):
    readings_list = dexcom.get_glucose_readings(minutes)
    sum_of_sugars = 0.0
    for reading in readings_list:
        sum_of_sugars += float(reading.value)
    return sum_of_sugars/len(readings_list)

def update_label(glucose_label, reading_time_label, current_time_label, last_24_label, last_1_label, user_str, password_str):
    # Call the API
    dexcom = Dexcom(user_str, password_str) 

    # Get the last available glucose reading
    glucose_reading = dexcom.get_latest_glucose_reading()

    # Update the Glucose Label
    glucose_label.configure(text=f"{glucose_reading.value} {glucose_reading.trend_arrow}")

    # Update the Glucose Reading Time
    glucose_time_str = time.strftime("%H:%M", glucose_reading.datetime.timetuple())
    reading_time_label.configure(text=f"As of: {glucose_time_str}")

    # Update the Current Time
    current_time = datetime.now().strftime("%H:%M")
    current_time_label.configure(text=f"Current Time: {current_time}")

    # Update the last 24 hour label
    last_24_hour_average_glucose = calculate_average(dexcom, 1440)
    last_24_label.configure(text=f"24h:{math.floor(last_24_hour_average_glucose)}")
    
    # Update the last 1 hour label
    last_1_hour_average_glucose = calculate_average(dexcom, 60)
    last_1_label.configure(text=f"1h:{math.floor(last_1_hour_average_glucose)}")

    # Do an update every minute
    glucose_label.after(60000, update_label, glucose_label, reading_time_label, current_time_label, last_24_label, last_1_label, user_str, password_str)


def main(user_name, password):

    # Run the thing
    root = tk.Tk()
    root.configure(background='black')
    app = DexcomGlucoseDisplay(root)
    update_label(app.last_reading_label, app.show_reading_time_label, app.show_current_time_label, app.last_24_hour_label, app.last_1_hour_label, user_name, password)
    root.mainloop()



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Opens a display showing a users dexcom reading and trend. If --user and --password aren't given it will prompt with a GUI")
    parser.add_argument('-u', '--user', required=False, help='dexcom username')
    parser.add_argument('-p', '--password', required=False, help='dexcom password')

    args = parser.parse_args()

    if not args.user or not args.password:
        # Get the user credentials
        user_name, password = get_user_credentials()

    else:
        user_name = args.user
        password = args.password

    main(user_name, password)
