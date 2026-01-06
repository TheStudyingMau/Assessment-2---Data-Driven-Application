# Imports
import random
from tkinter import *
import requests, os

# Variables
bgcolor = "#E0F7FA" # Light cyan background color
api_key = "1"  # Placeholder for API key

# Options
category = "categories.php"

url = f"https://www.themealdb.com/api/json/v1/{api_key}/{category}" # Placeholder for URL
response = requests.get(url) # API Request
database = response.json() # Parse JSON response

# Tkinter Window Setup
root = Tk()
root.geometry("400x300")
root.title("Simple GUI")
root.configure(bg=bgcolor)

script_dir = os.path.dirname(__file__)  # Finds the folder where the code lives.
file_path = os.path.join(script_dir, 'guide.txt') # Locates the file within the folder and stores it in an accessible variable.

# Data Dictionaries
categorydict = {} # Empty dictionary to store categories. 

######################################

# Classes That Handle Data

# class Categ 


data = list(database.values()) # Converts the values to a list and accesses the first item.
for i in range(len(data[0])): # Loops through each item in the list.
    categorydict[data[0][i]['strCategory']] = data[0][i]

with open (file_path, 'w', encoding="utf-8") as file_handler: # Opens the file through "with open" and assigns it as "file_handler."
    for key, values in categorydict.items(): # Loops through each item in the dictionary.
        file_handler.write(f"{key}:{values}\n") # Writes each item to the file followed by a newline character.

######################################

# System Logic

 