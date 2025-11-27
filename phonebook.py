import psycopg2
import csv

# ---------------------------------------------------------
# CONNECT TO POSTGRESQL (CHANGE THESE VALUES)
# ---------------------------------------------------------
conn = psycopg2.connect(
    host="localhost",
    database="phonebookdb",   # your database name
    user="postgres",          # your username
    password="Fybcf2014"  # your password
)
cursor = conn.cursor()


# ---------------------------------------------------------
# 1) CREATE TABLE
# ---------------------------------------------------------
def create_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            phone VARCHAR(20) UNIQUE NOT NULL
        );
    """)
    conn.commit()
    print("Table 'phonebook' created (or already exists).")


# ---------------------------------------------------------
# 2.1) INSERT USERS FROM CSV
# CSV format example:
# John,+77770001122
# ---------------------------------------------------------
def insert_from_csv(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                name, phone = row
                try:
                    cursor.execute(
                        "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)",
                        (name, phone)
                    )
                except psycopg2.Error as e:
                    print(f"Error inserting {name}: {e}")
        conn.commit()
        print("CSV data inserted successfully.")
    except FileNotFoundError:
        print("CSV file not found!")


# ---------------------------------------------------------
# 2.2) INSERT USER FROM CONSOLE
# ---------------------------------------------------------
def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    cursor.execute(
        "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)",
        (name, phone)
    )
    conn.commit()
    print("User added.")


# ---------------------------------------------------------
# 3) UPDATE USER DATA
# ---------------------------------------------------------
def update_user():
    identifier = input("Enter username or phone to update: ")

    new_name = input("New name (press Enter to skip): ")
    new_phone = input("New phone (press Enter to skip): ")

    if new_name:
        cursor.execute(
            "UPDATE phonebook SET first_name = %s WHERE first_name = %s OR phone = %s",
            (new_name, identifier, identifier)
        )
    if new_phone:
        cursor.execute(
            "UPDATE phonebook SET phone = %s WHERE first_name = %s OR phone = %s",
            (new_phone, identifier, identifier)
        )

    conn.commit()
    print("User updated.")


# ---------------------------------------------------------
# 4) SEARCH / QUERY USERS
# ---------------------------------------------------------
def search():
    print("""
Search by:
1) Name
2) Phone
3) All users
""")
    choice = input("Choose: ")

    if choice == "1":
        name = input("Enter name: ")
        cursor.execute("SELECT * FROM phonebook WHERE first_name ILIKE %s", (f"%{name}%",))
    elif choice == "2":
        phone = input("Enter phone: ")
        cursor.execute("SELECT * FROM phonebook WHERE phone = %s", (phone,))
    else:
        cursor.execute("SELECT * FROM phonebook")

    rows = cursor.fetchall()
    for r in rows:
        print(r)


# ---------------------------------------------------------
# 5) DELETE USER
# ---------------------------------------------------------
def delete_user():
    identifier = input("Enter username or phone to delete: ")
    cursor.execute(
        "DELETE FROM phonebook WHERE first_name = %s OR phone = %s",
        (identifier, identifier)
    )
    conn.commit()
    print("User deleted.")


# ---------------------------------------------------------
# MAIN MENU
# ---------------------------------------------------------
def menu():
    create_table()   # ← TABLE CREATES AUTOMATICALLY HERE

    while True:
        print("""
PHONEBOOK MENU
1) Insert from CSV
2) Insert from console
3) Update user
4) Search
5) Delete user
6) Exit
""")

        option = input("Choose option: ")

        if option == "1":
            filename = input("Enter CSV filename: ")
            insert_from_csv(filename)

        elif option == "2":
            insert_from_console()

        elif option == "3":
            update_user()

        elif option == "4":
            search()

        elif option == "5":
            delete_user()

        elif option == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")


# ---------------------------------------------------------
# RUN PROGRAM
# ---------------------------------------------------------
menu()
cursor.close()
conn.close()
