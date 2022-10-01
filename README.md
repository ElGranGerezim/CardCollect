# Overview

Simple python command line to connect to my personal Google Firestore database. Connects automatically on start and allows for
adding/updating/removing/querying of data. Database is modeled to represent a collection of playing card decks, and the programs
add/update functions reflect this, asking for data about the deck to add.

Created to allow me to learn about interfacing with cloud databases, as well as to give me a way to keep track of my collection.

[Demo Video](https://youtu.be/XLtt7H8rarY)

# Cloud Database

Database is a free Google Firestore project. Firestore is a NoSQL database platform provided by Google as part of their Firebase app environment.

The database itself has one collection, called Decks, with a document for each deck. Documents come in two types:
* Simple
  * These documents contain only a name and a creation time.
* Detailed
  * These documents contain more stats on the deck, including up to
    * Purchase date
    * Whether it is gilded
    * If the deck has customm pips
  * Additionally, all detailed decks track the last time they were updated.


# Development Environment

Created in Visual Studio Code
Programmed in Python including Google's provided Firebase Admin SDK and Firebase modules. 

# Useful Websites

* [Google Firebase Quickstart Guide](https://firebase.google.com/docs/firestore/quickstart)

# Future Work

* Create a GUI
* Link with Firestore Storage to allow for storing/retreiving images of the decks as well
  * After this, refactor the database so each deck includes a collection of cards, each with a picture.
* Create a reader version that allows others to only search for and learn about decks, but not edit.