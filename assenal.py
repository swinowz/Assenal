import signal
import sys
import os;
import json
import readline
import difflib
from rich.console import Console
from rich.text import Text
from rich.layout import Layout
from rich import print
from rich.prompt import Prompt

def signal_handler(sig, frame):
    os.system('clear')
    print('Interrupted')
    os.system('clear')
    sys.exit(0)

def search():
    # Recherche ici
    usersearch = Prompt.ask("Search:", default="nmap")

    with open(DB_PATH, 'r') as db_file:
        db_data = json.load(db_file)
        tools = [tool["title"] for tool in db_data['tools']]
        print(tools)

def mainMenu(menutext="Assenal", clearscreen=True):
    if clearscreen:
        os.system('clear')
    house_art = """
__
 /  \\
/____\\
|    |
|_[]_|
    """

    console.print(house_art, style="red", justify="center")

    text = Text("\n" + menutext)
    text.stylize("bold")
    text.stylize("size 40")
    console.print(text, justify="center")
    layout = Layout()
    layout.split_column(
        Layout(name="Search"),
        Layout(name="Results")
    )

def main():
    mainMenu(clearscreen=False)
    search() 

if __name__ == "__main__":
    # CONST
    DB_PATH = "db.json"

    signal.signal(signal.SIGINT, signal_handler)
    console = Console()
    main()
