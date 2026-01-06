# TheMeal API Python Client with TKinter GUI

from tkinter import *
import requests, os
from io import BytesIO
from PIL import Image, ImageTk
import customtkinter as CTK

# [VARIABLES]
bgcolor = "#2e2e2e"
buttoncolor = "#CB9E0C"

# [TKINTER WINDOW SETUP]
root = Tk()
root.geometry("1200x600")
root.title("MealDB Python API")
root.configure(bg=bgcolor)

# [CLASSES]

class MealDBClient: # Client-side Data Management.
    baseurl = "https://www.themealdb.com/api/json/v1/1/"

    # Search Methods
    def searchName(self, name): # Searches meal by name.
        url = f"{self.baseurl}search.php?s={name}" # Modifies the url
        return requests.get(url).json() # Returns the data as json.
    
    def searchID(self, id): # Searches meal by ID.
        url = f"{self.baseurl}lookup.php?i={id}"
        return requests.get(url).json() 

    # Filter Methods
    def filterCategory(self, category): # Searches meals by category.
        url = f"{self.baseurl}filter.php?c={category}"
        return requests.get(url).json()

    def filterArea(self, area): # Searches meals by area.
        url = f"{self.baseurl}filter.php?a={area}"
        return requests.get(url).json()

    # Lists Methods
    def categoryList(self): # Displays categories from the list (No Images)
        url = f"{self.baseurl}list.php?c=list"
        return requests.get(url).json()
    
    def AreaList(self): # Displays areas within a dictionaries values that stores the list. (No Images)
        url = f"{self.baseurl}list.php?a=list"
        return requests.get(url).json()
    
    def IngredientsList(self): # Displays Ingredients (Image, Type, ID, Name, Description)
        url = f"{self.baseurl}list.php?i=list"
        return requests.get(url).json()

    def FirstLetterList(self, letter): # Displays a list of meals by first letter. (Full data)
        url = f"{self.baseurl}search.php?f={letter}"
        return requests.get(url).json()
    
    # Bonus Randomized Methods [Full Data] (ID, Name, Alternate, Category, Area, Instructions, Thumbnail, Tags, Youtube, Ingredients(1:20), Measure(1:20))
    def randomMeal(self):
        url = f"{self.baseurl}random.php"
        return requests.get(url).json()
 
class MealCard(): # Meal Object Blueprint
    
    def __init__(self, reference): # Class Attributes 

        # Data classes that contain the meal's data.
        self.id: int
        self.name: str
        self.category: str
        self.area: str
        self.instructions: str
        self.mealimg: str
        self.tags: str
        self.youtube: str
        self.ingr1: str
        self.ingr2: str
        self.ingr3: str
        self.meas1: str
        self.meas2: str
        self.meas3: str
        self.source: str
        
        # Meal Card Elements
        self.frame = Frame(reference, bg="#343434", border=2, pady=15, padx=15) # This frame holds each meal option.
        response = requests.get(self.mealimg) # This downloads the image into bytes via link.
        img = ImageTk.PhotoImage(Image.open(BytesIO(response.content)).resize((250,250))) # BytesIO turns the json data into a file-like object.

        label = Label( # Stores the image and text in a label.
                self.frame, image = img, compound="top", # Compound tells the position of the image next to the text.
                text=f"{self.name}", font=('Helvetica', 12)
            )

    def storemealdata(self, meal_data): # Stores meal data into Meal Object.
        self.id = int(meal_data['meals'][0]['idMeal'])
        self.name = meal_data['meals'][0]['strMeal']
        self.category = meal_data['meals'][0]['strCategory']
        self.area = meal_data['meals'][0]['strArea']
        self.instructions = meal_data['meals'][0]['strInstructions']
        self.mealimg = meal_data['meals'][0]['strMealThumb']
        self.tags = meal_data['meals'][0]['strTags']
        self.youtube = meal_data['meals'][0]['strYoutube']
        self.ingr1 = str(meal_data['meals'][0]['strIngredient1'])
        self.ingr2 = str(meal_data['meals'][0]['strIngredient2'])
        self.ingr3 = str(meal_data['meals'][0]['strIngredient3'])
        self.meas1 = str(meal_data['meals'][0]['strMeasure1'])
        self.meas2 = str(meal_data['meals'][0]['strMeasure2'])
        self.meas3 = str(meal_data['meals'][0]['strMeasure3'])
        self.source = meal_data['meals'][0]['strSource']

    def displaymealdata(self): # Displays meal data in the console.
        
        # !! Reconstruct this into TkinterGUI.
        print(f"ID: {self.id}")
        print(f"Name: {self.name}")
        print(f"Category: {self.category}")
        print(f"Area: {self.area}")
        print(f"Instructions: {self.instructions}")
        print(f"Meal Image: {self.mealimg}")
        print(f"Tags: {self.tags}")
        print(f"YouTube: {self.youtube}")
        print(f"Ingredient 1: {self.ingr1}")
        print(f"Ingredient 2: {self.ingr2}")
        print(f"Ingredient 3: {self.ingr3}")
        print(f"Measure 1: {self.meas1}")
        print(f"Measure 2: {self.meas2}")
        print(f"Measure 3: {self.meas3}")
        print(f"Source: {self.source}")

class TkinterGUI: # TKinter GUI Blueprint
    def __init__(self, root): 

        # For displaying 10 random meals.
        self.cards = []
        self.images = []
        self.imagecontainers = []

        self.root = root # Connects the GUI's Root to the Class

        self.title = CTK.CTkLabel(self.frame, text="TheMeal Python API", font=('Arial', 24, "bold"), fg_color=bgcolor, text_color="white") # Title

        # Frames
        self.frame = Frame(root, bg=bgcolor) # Main Frame
        self.frame2 = Frame(self.frame) # Frame that contains the search bar
        self.frame3 = CTK.CTkScrollableFrame(self.frame, orientation="horizontal", width=1000, height=350) # Frame that contains the content.

        # For Search Bar
        self.entry = CTK.CTkEntry(self.frame2, placeholder_text='Search', corner_radius=0, width=800, height=28, fg_color="#FFFFFF", text_color="#000000", font=('Arial', 12)) # Entry Bar
        self.options = CTK.CTkOptionMenu(self.frame2, values=['ID', 'Name'], corner_radius=0, fg_color=buttoncolor, button_color=buttoncolor, button_hover_color=buttoncolor, text_color="white", font=('Arial', 12, "bold")) # Dropdown Button   

    def getmealrandom(self): # Gets 10 random meals from the API.
        for i in range(10): 
            # Set Up
            optionframe = Frame(self.frame3, bg="#343434", border=2, pady=15, padx=15) # This frame holds each meal option.
            mealimgurl = database.randomMeal()['meals'][0]['strMealThumb'] # Stores the link in a variable
            mealname = database.randomMeal()['meals'][0]['strMeal'] # Stores the meal name in a variable.
            response = requests.get(mealimgurl) # This downloads the image into bytes via link.
            img = ImageTk.PhotoImage(Image.open(BytesIO(response.content)).resize((250,250))) # BytesIO turns the json data into a file-like object.
            
            label = Label( # Compound tells the position of the image next to the text.
                optionframe, image = img, compound="top", 
                text=f"{mealname}", font=('Helvetica', 12)
            ) 
            label.pack()

            # Appending references
            self.imagecontainers.append(label)
            self.images.append(img)
            self.cards.append(optionframe)

    def displaymealrandom(self): # Displays the 10 random meals.
        for i in range(10):
            self.cards[i].pack(side="left") # Packs the cards contents (including frames and labels)
            
            # Binds the function to both the frame and image to make sure it is clickable.
            self.imagecontainers[i].bind("<Button-1>", openmeal) 
            self.cards[i].bind("<Button-1>", openmeal) 
    
    def searchmeal(self): # Searches meal based on user input.
        pass

    def clearframe(): # Clears the content frame.
        pass

class TheMealApplication(): # Main Application Blueprint
    def __init__(self):
        pass

####################################

# [FUNCTIONS]

def openmeal(event):
    print("Button is clicked!")

####################################

# [SETUP]

# Instantiations

# Main Objects
database = MealDBClient() # Instantiates the API class
GUI = TkinterGUI(root) # Instantiates the GUI class.

mealdata = MealCard() # Instantiates the Meal Object class.

#################

# [Packing System (!! Comes In Cascading Order !!)]

# Main Frame
GUI.frame.pack(side="top", anchor="center") # Packs the frame in the GUI
GUI.title.pack(pady=15, side="top") # Title in the GUI is packed.

GUI.frame2.pack(pady=15) # Packs the second frame holding the search bar.

# Search Items
GUI.entry.pack(side="left") # Entry in the GUI is packed.
GUI.options.pack(side="left") # Optionbox in the GUI is packed.

# Content Frame
GUI.frame3.pack(padx=15) # Packs the third frame holding the content.

#################
# [SYSTEM]
#################

# Testing Meal Object

mealdata.storemealdata(database.randomMeal()) # Stores random meal data into Meal Object.
mealdata.displaymealdata() # Displays meal data in the console.

#################

# Methods Called For Displaying Meals
# GUI.getmealrandom()
# GUI.displaymealrandom()

#################
# root.resizable(False,False) # Keeps the GUI from resizing. (fixed resolution)
# root.mainloop() # Runs the tkinter GUI.

####################################