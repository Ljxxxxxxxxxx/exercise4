import sqlite3
import sys

conn = sqlite3.connect('library.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Books (
    BookID INTEGER PRIMARY KEY,
    Title TEXT,
    Author TEXT,
    ISBN TEXT,
    Status TEXT
)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Users (
    UserID INTEGER PRIMARY KEY,
    Name TEXT,
    Email TEXT
)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Reservations (
    ReservationID INTEGER PRIMARY KEY,
    BookID INTEGER,
    UserID INTEGER,
    ReservationDate TEXT
)''')

conn.commit()

def main():
    print('Welcome to the library management system!')

    while True:
        choice = input('Enter your choice (1-7): ')

        if choice == '1':
            add_book()
        elif choice == '2':
            find_book_by_id()
        elif choice == '3':
            find_book_reservation_status()
        elif choice == '4':
            find_all_books()
        elif choice == '5':
            modify_book_details()
        elif choice == '6':
            delete_book()
        elif choice == '7':
            exit()
        else:
            print('Invalid choice!')

def add_book():
    title = input('Enter the book title: ')
    author = input('Enter the book author: ')
    isbn = input('Enter the book ISBN: ')
    status = input('Enter the book status (Available/Reserved): ')

    cur.execute('INSERT INTO Books (Title, Author, ISBN, Status) VALUES (?, ?, ?, ?)', (title, author, isbn, status))
    conn.commit()

    print('Book added successfully!')

def find_book_by_id():
    book_id = input('Enter the book ID: ')

    cur.execute('SELECT * FROM Books WHERE BookID = ?', (book_id,))
    book = cur.fetchone()

    if book is None:
        print('Book does not exist!')
        return

    print('Book details:')
    print('Title:', book[1])
    print('Author:', book[2])
    print('ISBN:', book[3])
    print('Status:', book[4])

    cur.execute('SELECT * FROM Reservations WHERE BookID = ?', (book_id,))
    reservation = cur.fetchone()

    if reservation is not None:
        print('User who has reserved the book:')
        user_id = reservation[2]

        cur.execute('SELECT * FROM Users WHERE UserID = ?', (user_id,))
        user = cur.fetchone()

        print('Name:', user[1])
        print('Email:', user[2])

def find_book_reservation_status():
    input_text = input('Enter the book ID, title, user ID, or reservation ID: ')

    if input_text.startswith('LB'):
        book_id = input_text[2:]
    elif input_text.startswith('LU'):
        user_id = input_text[2:]
    elif input_text.startswith('LR'):
        reservation_id = input_text[2:]
    else:
        book_title = input_text

    if book_id is not None:
        cur.execute('SELECT * FROM Reservations WHERE BookID = ?', (book_id,))
    elif user_id is not None:
        cur.execute('SELECT * FROM Reservations WHERE UserID = ?', (user_id,))
    elif reservation_id is not None:
        cur.execute('SELECT * FROM Reservations WHERE ReservationID = ?', (reservation_id,))
    else:
        cur.execute('SELECT * FROM Books WHERE Title = ?', (book_title,))

    reservation = cur.fetchone()

    if reservation is not None:
        print('Book is reserved!')
        print('User who has reserved the book:')
        user_id = reservation[2]

        cur.execute('SELECT * FROM Users WHERE UserID = ?', (user_id,))
        user = cur.fetchone()

        print('Name:', user[1])
        print('Email:', user[2])
    else:
        print('Book is not reserved!')

def find_all_books():
    cur.execute('SELECT * FROM Books')
    books = cur.fetchall()

    for book in books:
        print('Book details:')
        print('Title:', book[1])
        print('Author:', book[2])
        print('ISBN:', book[3])
        print('Status:', book[4])

def modify_book_details():
    book_id = input('Enter the book ID: ')

    cur.execute('SELECT * FROM Books WHERE BookID = ?', (book_id,))
    book = cur.fetchone()

    if book is None:
        print('Book does not exist!')
        return

    print('Book details:')
    print('Title:', book[1])
    print('Author:', book[2])
    print('ISBN:', book[3])
    print('Status:', book[4])

    title = input('Enter the new title: ')
    author = input('Enter the new author: ')
    isbn = input('Enter the new ISBN: ')
    status = input('Enter the new status: ')

    cur.execute('UPDATE Books SET Title = ?, Author = ?, ISBN = ?, Status = ? WHERE BookID = ?', (title, author, isbn, status, book_id))
    conn.commit()

    print('Book details updated successfully!')

def delete_book():
    book_id = input('Enter the book ID: ')

    cur.execute('SELECT * FROM Books WHERE BookID = ?', (book_id,))
    book = cur.fetchone()

    if book is None:
        print('Book does not exist!')
        return

    print('Book details:')
    print('Title:', book[1])
    print('Author:', book[2])
    print('ISBN:', book[3])
    print('Status:', book[4])

    cur.execute('SELECT * FROM Reservations WHERE BookID = ?', (book_id,))
    reservation = cur.fetchone()

    if reservation is not None:
        print('Book is reserved!')
        
        if input('Do you want to cancel the reservation and delete the book? (y/n): ') == 'y':
            cur.execute('DELETE FROM Reservations WHERE BookID = ?', (book_id,))
            conn.commit()
            print('Reservation cancelled!')

            cur.execute('DELETE FROM Books WHERE BookID = ?', (book_id,))
            conn.commit()
            print('Book deleted successfully!')
        else:
            return

    cur.execute('DELETE FROM Books WHERE BookID = ?', (book_id,))
    conn.commit()

    print('Book deleted successfully!')

def exit():
    print('Thank you for using the library management system!')

    conn.close()

    sys.exit()

if __name__ == '__main__':
    main()
