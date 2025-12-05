import psycopg2
import csv
import re

conn = psycopg2.connect(
    host="localhost",
    database="phonebookdb",
    user="postgres",
    password="Fybcf2014"
)
cursor = conn.cursor()


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


# -------------------------------------------------------------
# 1. SEARCH BY PATTERN (NAME OR PHONE)
# -------------------------------------------------------------
def search_by_pattern():
    pattern = input("Enter search pattern: ")

    cursor.execute("""
        SELECT * FROM phonebook
        WHERE first_name ILIKE %s OR phone ILIKE %s
    """, (f"%{pattern}%", f"%{pattern}%"))

    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("No matching users found.")


# -------------------------------------------------------------
# 3. INSERT MANY USERS USING PROCEDURE
#    procedure returns incorrect data
# -------------------------------------------------------------
def insert_many_users_procedure():

    n = int(input("How many users to insert? "))

    names = []
    phones = []

    for i in range(n):
        names.append(input(f"Name {i+1}: ").strip())
        phones.append(input(f"Phone {i+1}: ").strip())

    invalid = []

    # Phone regex: allows +, digits, -, length 5–20
    phone_re = re.compile(r'^[+]?[0-9\-]{5,20}$')

    for name, phone in zip(names, phones):

        # Validate phone number
        if not phone_re.match(phone):
            invalid.append(f"{name}:{phone}")
            continue

        try:
            # Try INSERT first
            cursor.execute("""
                INSERT INTO phonebook(first_name, phone)
                VALUES (%s, %s)
                ON CONFLICT (phone)
                DO UPDATE SET first_name = EXCLUDED.first_name;
            """, (name, phone))

        except psycopg2.Error as e:
            print(f"Database error for {name}:{phone} -> {e}")
            invalid.append(f"{name}:{phone}")

    conn.commit()

    if invalid:
        print("\nInvalid or failed entries:")
        for item in invalid:
            print(" -", item)
    else:
        print("All users inserted/updated successfully.")


# -------------------------------------------------------------
# 4. PAGINATION USING FUNCTION
# -------------------------------------------------------------
def pagination():
    limit = int(input("Enter limit (how many rows to return): "))
    offset = int(input("Enter offset (how many rows to skip): "))

    query = "SELECT * FROM phonebook LIMIT %s OFFSET %s"

    cursor.execute(query, (limit, offset))
    rows = cursor.fetchall()

    for row in rows:
        print(row)
        

# -------------------------------------------------------------
# ORIGINAL FUNCTIONS BELOW
# -------------------------------------------------------------
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


def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    cursor.execute(
        "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)",
        (name, phone)
    )
    conn.commit()
    print("User added.")


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


def delete_user():
    identifier = input("Enter username or phone to delete: ")
    cursor.execute(
        "DELETE FROM phonebook WHERE first_name = %s OR phone = %s",
        (identifier, identifier)
    )
    conn.commit()
    print("User deleted.")


# -------------------------------------------------------------
# ADDING NEW FEATURES INTO MENU
# -------------------------------------------------------------
def menu():
    create_table()

    while True:
        print("""
PHONEBOOK MENU
1) Insert from CSV
2) Insert from console
3) Update user
4) Search
5) Delete user
6) Exit
7) Search by pattern
9) Insert many users
10) Pagination query
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

        elif option == "7":
            search_by_pattern()

        elif option == "9":
            insert_many_users_procedure()

        elif option == "10":
            pagination()

        else:
            print("Invalid option.")


menu()
cursor.close()
conn.close()
#python phonebook_rebuild.py