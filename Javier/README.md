# Abomination (temporary name)

### Program to scrape information from the internet while the user chats with ChatGPT.

Utilizes multiprocessing to run two codes in parallel:
 - A visual interface for chatting with ChatGPT.
 - Scraping information from the internet and saving it in a database.


## How to run
 Run App.py:
    This code contains the visual interface and starts the scraping process.

### Visual interface
 A start window allows users to select who they want to chat with (e.g., 'Football Player', 'Football Fan', 'Football Hater', etc.). More roles can be added.
 It also provides the option to enter a user's name.
 
 
 The start button opens a second window where the chat takes place.

  -gpt.py: Code for chatting with ChatGPT. 

 * code GUI.py was the first version of the interface and is now outdated.

### Scraping
 Run the secondary_file.py.  Run the secondary_file.py. This file call the codes that are scrapping information:

  - Tables_are_fun.py: Drops and recreates tables in the database. Contains one view to meet one of the requirement.
                       This script includes functions for inserting and selecting information from the database, which are called by other scripts.
  
  - fifa_rack.py: Scrapes information about countries and their FIFA ranking. [fields: nationality, rank, points]
  
  - player.py:   - player.py: code to scrapp information about players. [name, age, team,  nationality, json_positions]

  - google.py: Scrapes information about the players teams (save it on the Database) based on the player's team. [fields: team, manager, stadium, location, founded year, leagues]

