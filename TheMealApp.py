# [ TheMealApp Python Client with customtkinter. ]

#--------------[ MODULES ]--------------#

import webbrowser as wb # Module needed to access the web.
import customtkinter as ctk # Main GUI Library
import requests # For API Requests
import threading # For Multithreading
from PIL import Image # For Image opening and image objects.
from io import BytesIO # Turns raw bytes into a readable file.

#--------------[ VARIABLES ]--------------#

maincolor =  "#2e2e2e"
darkcolor = "#202020"
accentcolor = "#CB9E0C"
darkaccent = "#7B5000"
h1 = ('Inter', 24, "bold")
large = ('Inter', 20)
bold = ('Inter', 15, "bold")
p = ('Inter', 15)
imagesmall = (200,200)
imagelarge = (400,400)

#############################################

#--------------[ OUTSIDE FUNCTIONS ]--------------#

def clearwidgets(): # Function to clear all widgets in both display frames.
    for widget in GUI.display1.winfo_children(): 
        widget.destroy()

    for widget in GUI.display2.winfo_children():
        widget.destroy()

def cleardisplay2(): # Function that specifically clears widgets in display2 frame.
    for widget in GUI.display2.winfo_children():
        widget.destroy()

#--------------[ CLASSES ]--------------#

class ErrorDisplay(): # Responsible for informing user their error for searchGUI.
    
    def apifailure(self, error): # Method that displays the API error.
        self.label = ctk.CTkLabel(GUI.display1, text="", font=p) # Label is constructed.
        self.label.configure(text=f"[!]: API failed. Error: {error}")
        self.label.grid(row=2, column=0, sticky="nsew", pady=50)

    def noitemsfound(self): # Method that displays 'No Items Found.'
        self.label = ctk.CTkLabel(GUI.display1, text="", font=p) # Label is constructed.
        self.label.configure(text="[!]: No Items Found :C")
        self.label.grid(row=2, column=0, sticky="nsew", pady=50)

    def invalidinput(self): # Method that displays 'Invalid input.'
        self.label = ctk.CTkLabel(GUI.display1, text="", font=p) # Label is constructed.
        self.label.configure(text="[!]: Invalid input")
        self.label.grid(row=2, column=0, sticky="nsew", pady=50)

    def insufficientinput(self): # Method that displays 'Insufficient Input.'
        self.label = ctk.CTkLabel(GUI.display1, text="", font=p) # Label is constructed.
        self.label.configure(text="[!]: Insufficient ID Input.")
        self.label.grid(row=2, column=0, sticky="nsew", pady=50)

    def emptyinput(self): # Method that displays 'Empty Input.'
        self.label = ctk.CTkLabel(GUI.display1, text="", font=p) # Label is constructed.
        self.label.configure(text="[!]: Empty Input. Please try again.")
        self.label.grid(row=2, column=0, sticky="nsew", pady=50)

##################################

class MealDBClient(): # Responsible for acquiring API data.
    baseurl = "https://www.themealdb.com/api/json/v1/1/" # Base URL for API requests.

    # [SEARCH METHODS ]
    
    def searchName(self,name): # Searches meal by name.
        url = f"{self.baseurl}search.php?s={name}" # Modifies the url
        response = None # Response is initially none prepared for the exception handling if API is not functioning.

        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            return data # Returns the data now as json.
        except Exception:
            status = response.status_code if response else None # If there is response, it returns the status code, otherwise it returns None.
            SYS.apifailure(status) # Displays the error.
            return None
    
    def searchFirstLetter(self, letter): # Searches meal by first letter.
        url = f"{self.baseurl}search.php?f={letter}"
        response = None

        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            return data # Returns the data now as json.
        except Exception:
            status = response.status_code if response else None # If there is response, it returns the status code, otherwise it returns None.
            SYS.apifailure(status)
            return None

    def searchID(self,id): # Searches meal by ID.
        url = f"{self.baseurl}lookup.php?i={id}"
        response = None

        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            return data # Returns the data now as json.
        except Exception:
            status = response.status_code if response else None # If there is response, it returns the status code, otherwise it returns None.
            SYS.apifailure(status)
            return None
    
##################################

class Meal(): # Represents a Meal object.
    def __init__(self, data): # The class takes in the data needed. 
        
        # [VARIABLES]
        self.ingredients = [] # Ingredients List

        # [ASSIGNING DATA]
        self.name = data.get('strMeal') # Gets the meal title from the json.
        self.id = data.get('idMeal') # Gets the meal ID from the json.
        self.category = data.get('strCategory') # Gets the meal category from the json.
        self.area = data.get('strArea') # Gets the meal area from the json.
        self.instructions = data.get('strInstructions') # Gets the meal instructions from the json.
        self.thumbnail = data.get('strMealThumb') # Gets the meal thumbnail URL from the json.
        self.tags = data.get('strTags') # Gets the meal tags from the json.
        self.youtube = data.get('strYoutube') # Gets the meal YouTube link from the json.

        for n in range(1,21): # Goes through from 1-20 to get all the ingredients and tags.
            # ".get()" is used to avoid errors.
            self.ing = data.get(f"strIngredient{n}")
            self.meas = data.get(f"strMeasure{n}")

            if self.ing and self.ing.strip() != "": # If ingredient is not empty.
                self.ingredients.append(f"{self.ing} - {self.meas}") # Ingredients are then appended along with its measurement.
        
        if data.get(f"strSource") == "":  # Gets the meal source link from the json.
            self.source = "Null"
        else:
            self.source = data.get(f"strSource") 

        self.imgsource = data.get(f"strImageSource") # Gets the image source from the json.
        self.cc = data.get('strCreativeCommonsConfirmed') # Gets the meal creative commons link from the json.
        self.datemodified = data.get('strDateModified') # Gets the meal date modified from the json.

##################################

class contentGUI(): # Handles the display frame GUI elements and function.
    def __init__(self, meal, parent, iteration=0): # Initializes the display GUI class.
       
       # [VARIABLES]
       placeholder = Image.new('RGB', (250, 250), color = 'gray') # Creates a placeholder gray image if the request fails.

       self.textsplit = meal.instructions.replace('\r\n', ' ').replace('\n', ' ') # Replaces new lines with spaces.
       self.text = self.textsplit if len(self.textsplit) < 300 else self.textsplit[:300] + "..."  # Limits the text to 500 characters using short-term if-else condition
       self.tkimg = "" # Empty variable used later.
       self.listofingredients = "" # Empty variable used later.

       # [FRAMES]
       self.card = ctk.CTkFrame(parent, fg_color=maincolor, corner_radius=10) # Card Frame
       self.description = ctk.CTkFrame(self.card, fg_color=maincolor, corner_radius=10) # Description Frame
       self.h1frame = ctk.CTkFrame(self.description, fg_color=maincolor, corner_radius=10) # H1 Frame
       self.info = ctk.CTkFrame(self.description, fg_color=maincolor, corner_radius=10) # Info Frame

       # [WIDGETS & ELEMENTS]
       self.img = ctk.CTkImage(placeholder, size=imagesmall) # The image is then converted and stored
       self.label = ctk.CTkLabel(self.card, image=self.img, text="") # Label to hold the image.
       self.title = ctk.CTkLabel(self.h1frame, text=meal.name, text_color="white", font=h1, wraplength=400, justify="left") # Label to hold the description text.
       self.id = ctk.CTkLabel(self.info, text=f"ID: {meal.id}", text_color="white", font=bold) # Label to hold the meal ID.
       self.category = ctk.CTkLabel(self.info, text=f"Category: {meal.category}", text_color="white", font=p) # Label to hold the meal category.
       self.instructions_text = ctk.CTkLabel(self.info, text=self.text, text_color="white", font=p, wraplength=400, justify="left") # Label to hold the meal instructions.

       # [GRID LAYOUT]

       # Frames
       self.card.grid(row=iteration, column=0, columnspan=3, padx=20, pady=20, sticky="nsew") # Grids the card based on the iteration number.
       self.h1frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
       self.description.grid(row=0, column=1, columnspan=2, padx=20, pady=20, sticky="nsew")
       self.info.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

       # Widgets & Elements
       self.label.grid(row=0, column=0, padx=10, pady=10) 
       self.title.grid(row=1, column=0, sticky="w")
       self.id.grid(row=0, column=0, sticky="w")
       self.category.grid(row=0, column=2, sticky="w")
       self.instructions_text.grid(row=1, column=0, columnspan=3, sticky="w")

       # [GRID CONFIGURATION]
       self.card.grid_columnconfigure(1, weight=2)
       self.description.grid_rowconfigure(0, pad=0)
       self.info.grid_columnconfigure(0, pad=25)
       self.info.grid_rowconfigure(0, pad=10)

       # [FRAME BINDINGS]
       self.card.bind("<Button-1>", lambda event: self.viewmealdata(meal, event)) # Binds the card frame to view meal data function.

       # [FUNCTION CALLS]
       self.load_image_async(meal.thumbnail, self.update_image) # Starts the threading process for the content's images.

    # [!] : [ VIEWING DATA METHOD ]
    def viewmealdata(self, meal, event=None): # Function to view meal data in the console.
        
        cleardisplay2()

        # [IMAGE HANDLING]

        try: # Attempts to construct the acquired image.
            self.tkimg = ctk.CTkImage(self.img, size=imagelarge)
        except: # If there are exceptions, creates an colored image as placeholder.
            self.tkimg = ctk.CTkImage(Image.new('RGB', (500, 500), color = 'gray'), size=imagelarge)

        # [WIDGETS & ELEMENTS]

        for i in meal.ingredients: # For every ingredient in the meal data.
            if len(meal.ingredients) > 1: # If the amount of meals are more than one.
                line = f" {i}\n" # Stores the line with the comma. (sugggesting more than one ingredients)
            else:
                line = f" {i}\n" # Stores the line without the comma.

            self.listofingredients += line # Adds it to display the list

        # [VIEW MEAL DATA GUI]
        label = ctk.CTkLabel(GUI.display2, image=self.tkimg, text="")
        src = ctk.CTkLabel(GUI.display2, text=meal.source, wraplength=350)
        youtube = ctk.CTkButton(GUI.display2, height=35, text="Watch Tutorial", fg_color=accentcolor, font=bold, command=lambda: self.openyoutube(meal), hover_color=darkaccent)
        title = ctk.CTkLabel(GUI.display2, text=f"Meal Name: {meal.name}", font=large, wraplength=350)
        id = ctk.CTkLabel(GUI.display2, text=f"ID: {meal.id}", font=large, wraplength=350)
        category = ctk.CTkLabel(GUI.display2, text=f"Category: {meal.category}", font=large, wraplength=350)
        area = ctk.CTkLabel(GUI.display2, text=f"Area: {meal.area}", font=large, wraplength=350)
        ingredients = ctk.CTkLabel(GUI.display2, text="Ingredients:", font=large, wraplength=350)
        listofing = ctk.CTkLabel(GUI.display2, text=f"{self.listofingredients}", font=p, text_color=accentcolor, wraplength= 350, justify="left")
        tags = ctk.CTkLabel(GUI.display2, text=f"Tags: {meal.tags}", font=large, wraplength=350)
        imgsource = ctk.CTkLabel(GUI.display2, text=f"Image Source: {meal.imgsource}", font=large, wraplength=350)
        instructions = ctk.CTkLabel(GUI.display2, text="Instructions: ", font=large, wraplength=350)
        steps = ctk.CTkLabel(GUI.display2, text=f"{meal.instructions}", font=p, text_color=accentcolor, wraplength=350, justify="left")
        creativecommons = ctk.CTkLabel(GUI.display2, text=f"Creative Commons: {meal.cc}", font=large, wraplength=350)
        datemod = ctk.CTkLabel(GUI.display2, text=f"Date Modified: {meal.datemodified}", font=large, wraplength=350)
            
        # [GRID: WIDGETS & ELEMENTS]
        label.grid(row=0, column=0, sticky="nsew", pady=(0,5))
        src.grid(row=1, column=0)
        youtube.grid(row=2, column=0, sticky="ew", pady=5)
        title.grid(row=3, column=0, pady=(15,0), sticky="w")
        id.grid(row=4, column=0, sticky="w")
        category.grid(row=5, column=0, sticky="w")
        area.grid(row=6, column=0, sticky="w")
        ingredients.grid (row=7, column=0, sticky="w")
        listofing.grid(row=8, column=0, sticky="w")
        tags.grid(row=9, column=0, sticky="w")
        imgsource.grid(row=10, column=0, sticky="w")
        instructions.grid(row=11, column=0, sticky="w")
        steps.grid(row=12, column=0, sticky="w", pady=15)
        creativecommons.grid(row=13, column=0, sticky="w")
        datemod.grid(row=14, column=0, sticky="w")

    # [!] : [ METHODS FOR YOUTUBE LINKS ]
    def openyoutube(self, meal):
        wb.open_new_tab(meal.youtube) # Using webbrowser module, it opens the tab based on the meal's web link provided.

    # [!] : [ THREADING FUNCTIONS ] : NEEDED FOR FASTER RESPONSES!!
    def load_image_async(self, url, callback): # Function responsible for loading the image async. 

        def worker(): # A worker thread to handle the image loading.
            try: 
                response = requests.get(url) # The nested worker method  tries to get the image based on the provided url.
                self.img = Image.open(BytesIO(response.content)) # This opens the image from the URL into a readable file.
            except: 
                self.img = Image.new('RGB', (250, 250), 'gray') # Placeholder stays gray if loading fails.

            GUI.after(0, lambda: callback(self.img)) # Calls the callback on the main thread.

        threading.Thread(target=worker, daemon=True).start() # Starts the worker thread.
        
    def update_image(self, img): # Method that updates the image in the label once loaded.
        tk_img = ctk.CTkImage(img, size=imagesmall) # After BytesIO makes the file readable for PIL, PIL is used to display the image.
        self.label.configure(image=tk_img) # Image is replaced from its placeholder to its actual.
        self.label.image = tk_img 

##################################

class searchGUI(): # Handles the search frame GUI and function.
    def __init__(self, parent): # Initializes the search GUI class.

        # [VARIABLES]
        self.options = ['Name', 'ID'] # List of options for your search.

        # [WIDGETS & ELEMENTS]
        self.label = ctk.CTkLabel(parent, text="TheMeal Python API", text_color="white", font=h1, fg_color=maincolor)
        self.entry = ctk.CTkEntry(parent, placeholder_text="Search", corner_radius=0, fg_color="white", text_color="black", font=p)
        self.options = ctk.CTkOptionMenu( parent, corner_radius=0, fg_color=accentcolor, button_color=accentcolor, button_hover_color=accentcolor, values=self.options,text_color="white", font=bold)

        # [GRID LAYOUT]
        self.label.grid(row=0, column=0, sticky="w")
        self.entry.grid(row=0, column=1, columnspan=3, sticky="ew")
        self.options.grid(row=0, column=6, sticky="e")

        # [ELEMENT BINDINGS]
        self.entry.bind("<Return>", self.searchfunction) # If Enter is pressed, call the search function.

    def searchfunction(self, event=None): # Function that handles the search logic.
        
        search = self.entry.get() # Gets the text from the entry widget.
        
        if search == "": # If search is empty.
            clearwidgets() # Cleans up the current widgets in the both displays.
            SYS.emptyinput() # Informs the user of their error that the input is empty.
            return # 'Return' ends the method.
        
        else:
            if self.options.get() == 'Name': # If the option selected is "Name"

                if len(search) == 1: # If the search is only 1 letter, use first letter search.
                    clearwidgets() # Clean both displays.
                    data = API.searchFirstLetter(search) # API is used for search and its result is stored as 'data.'

                elif len(search) > 1: # If the search is more than 1 letter, use name search.
                    clearwidgets() # Clean both displays.
                    data = API.searchName(search) # API is used for search and its result is stored as 'data.'

                meals = data['meals'] # Stores the meals within the data in its own variable.

                if meals is None: # If no meals are found, inform and exit.
                    clearwidgets() # Clean both displays.
                    SYS.noitemsfound() # Informs the user that no items were found.
                    return # Ends the method.

                self.loadcards(meals) # If there is a meal, calls the "loadcards" function to display the meals.
                    
            if self.options.get() == 'ID': # If the option selected is "ID"
                
                if search.isdigit() == False: # Checks if the ID input was a string input.
                    clearwidgets() # Clean both displays.
                    SYS.invalidinput() # Informs the user of their error.
                    return # Ends the method.

                if len(search) < 5: # If the numbers are under 5 digits
                    clearwidgets() # Clean both displays.
                    SYS.insufficientinput() # Informs the user of their error.
                    return # Ends the method.

                else: # If numbers are exactly 5 digits.
                    clearwidgets() # Clean both displays. 
                    data = API.searchID(search) # API is used for search.

                meals = data['meals'] # Data's meals are stored in its own variable.

                if meals is None: # If no meals are found, inform and exit.
                    clearwidgets() # Clean both displays.
                    SYS.noitemsfound() # Inform user of the result.
                    return # Ends the method.
                
                self.loadcards(meals) # If there is a meal, calls the "loadcards" function to display the meals.

    # Media Handling
    def loadcards(self, meals, index=0): # Loads meal cards into the content frame.
        
        # A more unsual for-loop is made to give the system time to load than to overwhelm it.
        if index >= len(meals): # Base case: if index exceeds meals length, closes the function.
            return
        
        mealdata = meals[index] # Gets the meal data at the current index.
        meal = Meal(mealdata) # Creates its Meal object.
        contentGUI(meal, GUI.display1, index) # Creates its content GUI object while storing its meal data and its root for GUI display.

        GUI.after(10, lambda: self.loadcards(meals, index + 1)) # Calls the function again after 10 milliseconds for the next meal.
           
##################################

class MainAppGUI(ctk.CTk): # Handles the main GUI elements.
    def __init__(self): # Initializes the GUI class
        super().__init__() # Redefines the __init__ from its parent class "ctk.CTK".

        # [WINDOW CUSTOMIZATION]
        self.geometry("1200x600") # Window Size
        self.title("TheMealApp") # Window Title
        self.configure(fg_color=maincolor) # Window Background Color
        
        # [FRAMES]
        self.header = ctk.CTkFrame(self, fg_color=maincolor) # Header Frame
        self.content = ctk.CTkFrame(self, fg_color=darkcolor) # Content Frame
        self.display1 = ctk.CTkScrollableFrame(self.content, fg_color=darkcolor, corner_radius=0) # Display Frame 1
        self.display2 = ctk.CTkScrollableFrame(self.content, fg_color=darkcolor, corner_radius=0) # Display Frame 2

        # [GRID LAYOUT]
        self.header.grid(row=0, column=0, padx=20, sticky="ew") 
        self.content.grid(row=1, column=0, sticky="nsew")
        self.display1.grid(row=0, column=0, sticky="nsew")
        self.display2.grid(row=0, column=1, sticky="nsew", pady=25, padx=15)

        # [!] : [GRID CONFIGURATION]

        # [ROOT GRID CONFIGURATION]
        self.grid_rowconfigure(0, weight=1) 
        self.grid_rowconfigure(1, weight=10) # Content row expands more.
        self.grid_columnconfigure(0, weight=1)

        # [HEADER CONFIGURATION]
        self.header.grid_columnconfigure(0, weight=1)
        self.header.grid_columnconfigure(1, weight=5) # The center of header expands more.
        self.header.grid_columnconfigure(2, weight=1)

        # [CONTENT CONFIGURATION]
        self.content.grid_rowconfigure(0, weight=1) 
        self.content.grid_columnconfigure(0, weight=2) # Column 0 expands twice as much as column 1.
        self.content.grid_columnconfigure(1, weight=1)

        # [DISPLAY1 CONFIGURATION]
        self.display1.grid_columnconfigure(0, weight=1)

        # [DISPLAY2 CONFIGURATION]
        self.display2.configure(width=200) # Sets its fixed width
        self.display2.grid_columnconfigure(0, weight=2)

        #####################################

        # [!] : [INSTANTIATING ELEMENTS]
        
        self.searchbar = searchGUI(self.header) # Instantiates the search GUI class.

    def welcome(self): # Method that welcomes the user to the application.
            clearwidgets() # Clears the widgets as usual.
            self.label = ctk.CTkLabel(self.display1, text="Welcome to TheMeal Application! Please type the meal you desired.", wraplength=350, font=p)
            self.label.grid(row=2, column=0, sticky="nsew", pady=100)

##################################

#--------------[ SYSTEM LOGIC ]--------------#

API = MealDBClient() # Instantiates the MealDBClient class
GUI = MainAppGUI() # Instantiates the MainAppGUI class.
SYS = ErrorDisplay() # Instantiates the ErrorDisplay class.
GUI.welcome() # Welcomes the user before the application runs.
GUI.mainloop() # Runs the application.

##################################


