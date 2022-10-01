from getpass import getuser
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


# Answer group constants for input validation.
# Made global because several functions need to know this. 
EXIT_ANSWERS = ["e", "quit", "exit", "leave", "close"]
DOC_FILEDS = ['Purchased', 'Gilded', 'Custom Pips', 'Type']
NO_ANSWERS = ["n", "no", "f", "false", "incorrect"]
YES_ANSWERS = ["y", "yes", "t", "true", "correct"]
SIMPLE_ANSWERS = ["s", "simple", "small", "short"]
DETAILED_ANSWERS = ["d", "detailed", "descriptive"]

# Connect to the database using Application credentials
def connect():
    # Get credential from json
    cred = credentials.Certificate('cardcollect-bbefd-a23e50827e56.json')
    
    # Initialize app connection
    app = firebase_admin.initialize_app(cred)
    
    print("Connect")
    db = firestore.client()
    print("Connected to Firestore Database")
    return db

# Determines if user text input is a confirmation or negation
def isYes(input):
    if input not in NO_ANSWERS and input not in YES_ANSWERS:
        print("Response is not recognizable as yes or no, defaulting to no.")
        return False
    else:
        return input in YES_ANSWERS

# For testing, adds a default deck.
def addDefault(db):
    doc_ref = db.collection(u'decks').document(u'default')
    doc_ref.set({
        u'Name': u'default',
    })

# Adds a simple deck to the collection. Just a name and date.
def addSimpleDeck(db):
    # Get a name for it
    name = input("What is the name of this deck >: ")

    # Create a new doc by attempting to access it by name
    doc_ref = db.collection(u'decks').document(name)

    # Set the data
    doc_ref.set({
        u'Name':name,
        u'Created':datetime.datetime.now(),
        u'Updated':datetime.datetime.now(),
        u'Type':u'Simple'
    })
    print("Deck Added successfully.")

# Adds a detailed deck to the collection, includes name, purchase date, if the deck is gilded, and if it has custom pips
def addDetailedDeck(db):
    # Get all the required data
    name = input("What is the name of this deck >: ")
    dateInput = input("When was it purchased (mm/dd/yy) >: ")
    # Try to cast to datetime
    try:
        date = datetime.datetime.strptime(dateInput, f'%m/%d/%y')
    except:
        # Bad date string, replacing with current datetime
        date = datetime.datetime.now()
    gilded = isYes(input("Is it gilded?: "))
    customPips = isYes(input("Does it have custom pip icons >: "))

    # Create the new document by attempting to access it.
    doc_ref = db.collection(u'decks').document(name)

    # Set all the data
    doc_ref.set({
        u'Name':name,
        u'Created':datetime.datetime.now(),
        u'Purchased': date,
        u'Gilded': gilded,
        u'Custom Pips': customPips,
        u'Type':u'Detailed',
        u'Updated':datetime.datetime.now()
    })
    print("Deck added successfully.")

# Menu for chosing which type of deck to add.
def addMenu(db):
    choice = input("Would you like to add a simple or detailed entry? >:")

    while choice.lower() not in SIMPLE_ANSWERS and choice not in DETAILED_ANSWERS:
        # Bad choice
        choice = input("unknown answer, please choose s or d")
    if choice in SIMPLE_ANSWERS:
        addSimpleDeck(db)
    elif choice in DETAILED_ANSWERS:
        addDetailedDeck(db)

# Displays all decks in the collection
def getDecks(db):
    # Get the deccks
    decks_ref = db.collection(u'decks')
    docs = decks_ref.stream()

    for doc in docs:
        displayDeck(doc.to_dict())

# Displays all simple decks in the collection
def getSimpleDecks(db):
    # Attempt to get the deck
    docs = db.collection(u'decks').where(u'Type', u'==', u'Simple').stream()
    for doc in docs:
        displayDeck(doc.to_dict())

# Displays all detailed decks in the collection
def getDetailedDecks(db):
    # Attempt to get the deck
    docs = db.collection(u'decks').where(u'Type', u'==', u'Detailed').stream()
    for doc in docs:
        displayDeck(doc.to_dict())

# Searches for a specific deck by name and displays it
def search(db):
    name = input("What do you want to search for? >:")

    # Attempt to get the deck
    doc = db.collection(u'decks').document(name).get()
    if doc.exists:
        displayDeck(doc.to_dict())
    else:
        print("No results found. Remember name must be exact")

# Menu for selecting search options.
def queryMenu(db):

    # Unique, query only answers are kept here instead of global
    keyword = ["n", "k", "keyword", "name"]
    choice = input("Would you like all simple, all detailed, or to search by name? >:").lower()

    if choice in SIMPLE_ANSWERS:
        # Display all simple decks
        getSimpleDecks(db)
    elif choice in DETAILED_ANSWERS:
        # Display all detailed decks
        getDetailedDecks(db)
    elif choice in keyword:
        # Start a search
        search(db)
    else:
        print("Choice not recognized, returning to start.")

# Menu for selecting which decks to get from database
def getMenu(db):

    # Unique, search only answers are kept here instead of global.
    all = ["a", "all", "every", ""]
    search = ["s", "query", "specific", "search", " "]
    choice = input("Would you like to get all decks, or search for specific ones? >:")

    if choice not in all and choice not in search:
        # Bad choice
        print("Choice not recognized, returning to start")
    elif choice in search:
        # Search for specific decks
        queryMenu(db)
    elif choice in all:
        # Display all decks
        getDecks(db)

# Asks for a deck, if it exists asks for confirmation, then deletes deck
def delete(db):
    name = input("What is the name of the deck to delete? >:")
    print(name)

    # Try to get the document
    doc_ref = db.collection(u'decks').document(name)
    doc = doc_ref.get()

    # Verify existance
    if doc.exists:
        print("\n")
        displayDeck(doc.to_dict())

        # Ask for confirmation
        confirm = input("*WARNING*\nAre you sure you wish to delete this deck? >:")
        if isYes(confirm):
            doc_ref.delete()
            print("Deck Deleted Successfully.")
    else:
        print(u'No such deck exists.')

# Menu for selecting which deck and fields to update
def updateMenu(db):
    name = input("What is the name of the deck to update? >:")

    # Try to get the document
    doc_ref = db.collection(u'decks').document(name)
    doc = doc_ref.get()

    # Verify existance
    if doc.exists:
        answer = ""
        # Keep letting user update until they decide to leave.
        while answer not in EXIT_ANSWERS:
            # Display options
            print("Possible fields: ")
            i = 1
            for choice in DOC_FILEDS:
                print(f"{i}: {choice}")
                i += 1

            answer = input("What would you like to update? >: ")
            
            # Allow user to chose based on index number or full field name
            if answer.isnumeric():
                answer = int(answer) - 1
                if answer < len(DOC_FILEDS):
                    # Update the field
                    update(doc_ref, DOC_FILEDS[answer])
                else:
                    # They gave us a number that does not correspond to any field value.
                    print("Field index invalid, please select a valid field.")
            elif answer.lower() in DOC_FILEDS:
                # Update the field.
                update(answer)             
    else:
        # Name was incorrect.
        print(u'No such deck exists.')

# Input validation and update calls for updating a deck.
def update(doc_ref, field):
    answer = input(f"What would you like to change the {field} field to? >: ")
    # Unique case, purchased is datetime.
    if field == "Purchased":
        try:
            # Try to create a datetime from string input.
            answer = datetime.datetime.strptime(answer, f'%m/%d/%y')
        except:
            # They messed up the date, but we'll just add it as a datetime because firebase is not type locked.
            pass
    try:
        # Attempt to update the document.
        doc_ref.update({
            field:answer,
            u'Updated':datetime.datetime.now()
        })

        # If it is a simple document, upgrade it to detailed.
        if doc_ref.get().to_dict()['Type'].lower() == "simple":
            doc_ref.update({
                u'Type': 'Detailed'
            })
        print("Document updated successfully")
    except:
        # Firebase couldn't cast the datetime or bools and threw an error.
        print("There was an error updating the document. Please double check your data to ensure it is valid.")

# Displays a dictionary in a more readable way
def displayDeck(dic):
    print(f"Deck: {dic['Name']}")
    for key in dic:
        if key != "Name":
            print(f"    {key}: {dic[key]}")

# Main menu
def main():
    db = connect()
    answer = ""
    while answer not in EXIT_ANSWERS:
        answer = input(">: ").lower()
        if answer == "get":
            getMenu(db)
        if answer == "add":
            addMenu(db)
        if answer == "remove":
            delete(db)
        if answer == "update":
            updateMenu(db)

# Get the show started.
main()