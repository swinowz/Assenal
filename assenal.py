import signal
import sys
import os
import json
from rich.console import Console
from rich.text import Text
from rich.layout import Layout
from rich import print
from rich.prompt import Prompt
from rich.live import Live
from rich.table import Table
from simple_term_menu import TerminalMenu
import subprocess

def signal_handler(sig, frame):
    print('Interrupted')
    sys.exit(0)

def search():
    usersearch = (Prompt.ask("[red]Search")).lower()
    finds = []

    with open(DB_PATH, 'r') as db_file:            
        db_data = json.load(db_file)
        tools = [tool for tool in db_data['tools']]

    table = Table()
    table.add_column("Title")
    table.add_column("Description")
    table.add_column("Command")
    with Live(table, refresh_per_second=4):
        for tool in tools:
            if usersearch == "*" or usersearch in tool['title'] or usersearch in tool['object']['command'] or usersearch in tool['object']['description']:
                finds.append(tool['title'])
                table.add_row(f"[green]{tool['title']}", f"{tool['object']['description']}", f"{tool['object']['command']}")

    options = finds
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    choice = options[menu_entry_index]
    for tool in tools:
        if tool['title'] == choice:
            command = tool["object"]["command"]
            console.print(tool['object']['args'])
            for arg in tool['object']['args']:
                value = Prompt.ask(f"{arg} = ")
                command = command.replace(f"${arg}", value)

            # Execute the command in the terminal
            try:
                subprocess.run(command, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Command failed with error: {e}")

def mainMenu(menutext="Assenal", clearscreen=True):
    if clearscreen:
        os.system('clear')
    house_art = """

__
 /  \\
/____\\
|    ||
|_[]_||

    """

    console.print(house_art, style="red", justify="center")

    text = Text("\n" + menutext)
    text.stylize("bold")
    text.stylize("size 40")
    console.print(text, justify="center")
    layout = Layout()
    layout.split_column(
        Layout(name="search"),
        Layout(name="results")
    )
    layout["search"].size = 10
    
def main():
    search_completed = False
    mainMenu(clearscreen=True)
    while not search_completed:
        search() 

if __name__ == "__main__":
    DB_PATH = "db.json"

    signal.signal(signal.SIGINT, signal_handler)
    console = Console()
    main()
