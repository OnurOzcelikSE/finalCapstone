import sqlite3

# creates a database called ebookstore with a SQLite3 DB
db = sqlite3.connect("ebookstore.db")

# gets a cursor object
cursor = db.cursor()

# checks if the table called "books" exists and if not creates it
cursor.execute("""CREATE TABLE IF NOT EXISTS books
                    (id INTEGER PRIMARY KEY,
                    title TEXT,
                    author TEXT,
                    quantity INTEGER)""")

# book details in the bookstore
id1 = 3001
title1 = "A Tale of Two Cities"
author1 = "Charles Dickens"
quantity1 = 30

id2 = 3002
title2 = "Harry Potter and the Philosopher's Stone"
author2 = "J.K. Rowling"
quantity2 = 40

id3 = 3003
title3 = "The Lion, the Witch and the Wardrobe"
author3 = "C.S. Lewis"
quantity3 = 25

id4 = 3004
title4 = "The Lord of the Rings"
author4 = "J.R.R. Tolkien"
quantity4 = 37

id5 = 3005
title5 = "Alice in Wonderland"
author5 = "Lewis Carroll"
quantity5 = 12

# list of the book details to be able to add multiple at once
bookstore_database = [(id1, title1, author1, quantity1), (id2, title2, author2, quantity2),
                      (id3, title3, author3, quantity3), (id4, title4, author4, quantity4),
                      (id5, title5, author5, quantity5)]

# adds the details to the table
db.executemany("INSERT INTO books VALUES(?,?,?,?)", bookstore_database)


# if clerk wants to add a book to database
def add_new_book():
    # requests the details of the book which user wants to add to the database
    id_new = input("Please enter the ID of the new book: ")
    title_new = input(str("Please enter the Title of the new book: "))
    author_new = input(str("Please enter the Author of the new book: "))
    quantity_new = input("Please enter the Quantity of the new book: ")

    new_book = [(id_new, title_new, author_new, quantity_new)]

    # inserts the details to the table
    db.executemany("INSERT INTO books VALUES(?,?,?,?)", new_book)

    print("\nNew book added to the database successfully!\n")

    # prints out the last added book
    for row in cursor.execute(f"SELECT * FROM books WHERE id = ?", (id_new,)):
        print(row)

    return main()


# updates a book details which has the ID given by the user
def update_book():

    # requests the id number of the book which user wants to update the details
    update = input("Please enter the id of the book that you want to update: ")
    cursor.execute("SELECT * FROM books WHERE id = ?", (update,))

    # to get the book title to print out the result
    found = cursor.fetchone()

    # checks if the selected book is in the list or not
    if found:
        # requests new inputs to update from the clerk
        id_update = input("Please enter the new id:")
        title_update = input("Please enter the new title:")
        author_update = input("Please enter the new author:")
        quantity_update = input("Please enter the new quantity:")

        # executes the new data to the table
        db.execute("UPDATE books SET id = ? WHERE id = ?", (id_update, update))
        db.execute("UPDATE books SET title = ? WHERE id = ?", (title_update, update))
        db.execute("UPDATE books SET author = ? WHERE id = ?", (author_update, update))
        db.execute("UPDATE books SET quantity = ? WHERE id = ?", (quantity_update, update))
        print("Database updated!")

        # prints out the details of the updated book
        for row in cursor.execute(f"SELECT * FROM books WHERE id = {update}"):
            print(row)

    else:
        print("\nWrong ID! Please make sure you you entered the right ID!")

    return main()


# lists all of the books in the bookstore / database
def list_all_books():
    print("\nBooks in the store:")

    for row in cursor.execute("SELECT * FROM books"):
        print(row)

    return main()


# prints out a specific book which has the ID given by the user
def search_book():

    # requests the id number of the book which user wants to prints out the details
    search = input("Please enter the id of the book that you're searching for:")

    cursor.execute("SELECT * FROM books WHERE id = ?", (search,))

    # to get the book title to print out the result
    found = cursor.fetchone()

    # if the book is valid in the database prints out the details
    if found:
        print(found)

    # if that book is not stored in the database
    else:
        print("\nThis book is not valid in the database!")

    return main()


# this function removes a book from the database
def delete_book():

    # requests the id number of the book which user wants to remove from the database
    delete = input("Please enter the id of the book you would like to remove from the database?: ")
    cursor.execute("SELECT title FROM books WHERE id = ?", (delete,))

    # to get the book title for printing out the result
    book_to_delete = cursor.fetchone()

    # the the book with that id is valid in the database
    if book_to_delete:

        # title of the book
        book_title = book_to_delete[0]

        # deletes the data from the database
        cursor.execute("DELETE FROM books WHERE id = ?", (delete,))
        print(f"\n{book_title} is removed from the database successfully!")

    # if the book is not stored
    else:
        print(f"\nThe book with ID number {delete} isn't valid in the database!")

    return main()


# this main menu function provides options for the user to choose the action to take
def main():
    print("\nWelcome to Book Store Manager")

    while True:
        menu = str(input("""
Please enter one of the options below\n
a - add a new book
d - delete a book
l - list all books
u - update a book
s - search a book
q - quit
:""")).lower()

        try:
            if menu == "a":
                add_new_book()
                break

            if menu == "d":
                delete_book()
                break

            if menu == "l":
                list_all_books()
                break

            if menu == "u":
                update_book()
                break

            if menu == "s":
                search_book()
                break

            if menu == "q":
                print("Goodbye!")
                quit()

            else:
                print("Invalid value!\n")
                continue

        # error handling if user enters a wrong type, value, etc
        except TypeError:
            print("You entered a wrong answer!\n")
            continue
        except ValueError:
            print("Please enter a - d - l - u - s  or q!\n")
            continue


main()
