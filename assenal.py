import signal
import sys
import os
import json
from rich.console import Console
from rich.text import Text
from rich import print
from rich.prompt import Prompt
from rich.live import Live
from rich.table import Table
from simple_term_menu import TerminalMenu
import subprocess
import pyperclip
from random import *
import time

def signal_handler(sig, frame):
    print('Interrupted')
    sys.exit(0)

def json_write(new_command, file='db.json'):
    with open(file, 'r+') as f:
        data = json.load(f)
        data["tools"].append(new_command)
        f.seek(0)
        json.dump(data, f, indent=4)

def add_custom_command():
    console.print("Adding custom command")
    custom_name = (Prompt.ask("[green]Command title")).lower()
    custom_tags = (Prompt.ask("[green]Command tags (ex : tag1 tag2 tag3)")).lower()
    custom_description = (Prompt.ask("[green]Command description")).lower()
    custom_command = (Prompt.ask("[green]Full command, add $ before args ( ex : ping $ip)")).lower()
    custom_args = (Prompt.ask("[green]All args, in one line like tags (ex: ip wordlist file pass user)")).lower()
    new_command = {
        "title": custom_name,
        "object": {
            "tags": custom_tags,
            "description": custom_description,
            "command": custom_command,
            "args": custom_args.split(),
            "defaults": {}
        }
    }
    json_write(new_command)


def search():
    usersearch = (Prompt.ask("[red]Search")).lower()
    finds = []
    options = []

    if usersearch == "":
        console.print("[red]Empty search, going back to search")
        time.sleep(.5)
        main()

    if usersearch == "/add":
        add_custom_command()
        main()

    if usersearch == "/q" or usersearch == "/quit":
        exit()

    with open(DB_PATH, 'r') as db_file:            
        db_data = json.load(db_file)
        tools = [tool for tool in db_data['tools']]

    table = Table()
    table.add_column("Title")
    table.add_column("Description")
    table.add_column("Command")

    with Live(table, refresh_per_second=4):
        for tool in tools:
            if (usersearch == "*" or usersearch in tool['title'].lower() or
               usersearch in tool['object']['command'].lower() or 
               usersearch in tool['object']['description'].lower() or
               usersearch in tool['object']['tags'].lower()):
                finds.append(tool['title'])
                table.add_row(f"[green]{tool['title']}", f"{tool['object']['description']}", f"{tool['object']['command']}")
###############################
    options = finds
    #console.log(len(finds))
    if len(finds) == 0:
        console.print("[red] No results found, going back to search")
        time.sleep(.5)
        exit()
###############################

    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    choice = options[menu_entry_index]
    for tool in tools:
        if tool['title'] == choice:
            command = tool["object"]["command"]
            for arg in tool['object']['args']:
                try:
                    defaultval =  tool['object']['defaults'][arg]
                except KeyError as e:
                    defaultval = None
                value = Prompt.ask(f"{arg}", default=defaultval)
                if (value == None) or (value == " "):
                    console.print("[red]You entereda a blank value, going back to search...")
                    time.sleep(2)
                    main()
                else:
                    command = command.replace(f"${arg}", value)
            try:
                console.print(f"Here's your command: [bold yellow]{command}")
                check = (Prompt.ask("[green]Run (R) | [blue] Copy (C) | [red] Quit (Q)")).lower()
                match check[0]:
                    case "r":
                        subprocess.run(command, shell=True, check=True)
                        exit(0)
                    case "c":
                        pyperclip.copy(command)
                        exit(0)
                    case "q":
                        exit(0)
                
            except subprocess.CalledProcessError as e:
                print(f"Command failed with error: {e}")


def artGen():
    files = os.listdir("./arts")
    with open(f"./arts/{randint(1, len(files))}", 'r') as f:
        return f.read()

def mainMenu(menutext="Assenal", clearscreen=True):
    if clearscreen:
        os.system('clear')
    house_art = artGen()

    #console.print(house_art, style="cyan", justify="center")

    text = Text("\n" + menutext)
    text.stylize("bold")
    text.stylize("size 40")
    console.print(text, justify="center")
        
def main():
    search_completed = False
    mainMenu(clearscreen=True)
    search() 

if __name__ == "__main__":
    DB_PATH = "db.json"

    signal.signal(signal.SIGINT, signal_handler)
    console = Console()
    main()
