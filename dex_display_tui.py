#!/usr/bin/env python3

from datetime import datetime
import time
from pydexcom import Dexcom
from login_helper import get_user_credentials
import argparse

from textual.app import App, ComposeResult
from textual.widgets import Digits
user_str = str()
password_str = str()

class DexcomTui(App):
    CSS = """
    Screen { align: center middle; }
    Digits { width: auto; }
    """

    def compose(self) -> ComposeResult:
        yield Digits("")

    def on_ready(self) -> None:
        self.update_dex()
        self.set_interval(1, self.update_dex)

    def update_dex(self) -> None:

        global user_str
        global password_str

        # Call the API
        dexcom = Dexcom(user_str, password_str) 
        
        # Get the last available glucose reading
        glucose_reading = dexcom.get_latest_glucose_reading()

        # Change the display
        self.query_one(Digits).update(str(glucose_reading))

def update_label(glucose_label, reading_time_label, current_time_label, user_str, password_str):

    # Update the Glucose Label
    glucose_label.configure(text=f"{glucose_reading.value} {glucose_reading.trend_arrow}")

    # Update the Glucose Reading Time
    glucose_time_str = time.strftime("%H:%M", glucose_reading.datetime.timetuple())
    reading_time_label.configure(text=f"As of: {glucose_time_str}")

    # Update the Current Time
    current_time = datetime.now().strftime("%H:%M")
    current_time_label.configure(text=f"Current Time: {current_time}")

    # Do an update every minute
    glucose_label.after(60000, update_label, glucose_label, reading_time_label, current_time_label, user_str, password_str)


def main(user_name, password):
    global user_str
    global password_str

    user_str = user_name
    password_str = password

    # Run the thing
    app = DexcomTui()
    app.run()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Opens a display showing a users dexcom reading and trend. If --user and --password aren't given it will prompt with a GUI")
    parser.add_argument('-u', '--user', required=True, help='dexcom username')
    parser.add_argument('-p', '--password', required=True, help='dexcom password')

    args = parser.parse_args()

    user_name = args.user
    password = args.password

    main(user_name, password)
