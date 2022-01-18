import sqlite3
import json
from models import Customer

CUSTOMERS = [
    {
    "id": 1,
    "name": "Ryan Tanay",
    "address": "123 Main St,",
    "email": "ryan@email.com",
    "password": "DogLover"
    },
    {
    "id": 2,
    "name": "Emma Beaton",
    "address": "345 Alpine St",
    "email": "emma@email.com",
    "password": "DogWalker"
    },
    {
    "id": 3,
    "name": "Dani Adkins",
    "address": "567 Center Ave",
    "email": "dani@email.com",
    "password": "DanisDogs"
    },
    {
    "id": 4,
    "name": "Adam Oswalt",
    "address": "789 Harrison Blvd",
    "email": "adam@email.com",
    "password": "FetchingDogs"
    },
    {
    "id": 5,
    "name": "Fletcher Bangs",
    "address": "398 Outer Cir",
    "email": "fletcher@email.com",
    "password": "DogScratchies"
    },
    {
    "id": 6,
    "name": "Angela Lee",
    "address": "915 Seattle Way",
    "email": "angela@email.com",
    "password": "DogKisses"
    },
]

def get_all_customers():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            c.id,
            c.name,
            c.address,
            c.email,
            c.password
        FROM customer c
        """)

        # Initialize an empty list to hold all animal representations
        customers = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            customer = Customer(row['id'], row['name'], row['address'], row['email'], row['password'])

            customers.append(customer.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(customers)

def get_single_customer(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            c.id,
            c.name,
            c.address,
            c.email,
            c.password
        FROM customer c
        WHERE c.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        customer = Customer(data['id'], data['name'], data['address'], data['email'], data['password'])

        return json.dumps(customer.__dict__)
    
def get_customers_by_email(email):

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            c.id,
            c.name,
            c.address,
            c.email,
            c.password
        from Customer c
        WHERE c.email = ?
        """, ( email, ))

        customers = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            customer = Customer(row['id'], row['name'], row['address'], row['email'] , row['password'])
            customers.append(customer.__dict__)

    return json.dumps(customers)

def create_customer(customer):
    max_id = CUSTOMERS[-1]["id"]
    
    new_id = max_id + 1
    
    customer["id"] = new_id
    
    CUSTOMERS.append(customer)
    
    return customer

def delete_customer(id):

    customer_index = -1

    for index, customer in enumerate(CUSTOMERS):
        if customer["id"] == id:
            customer_index = index

    if customer_index >= 0:
        CUSTOMERS.pop(customer_index)
        
def update_customer(id, new_customer):

    for index, customer in enumerate(CUSTOMERS):
        if customer["id"] == id:
            CUSTOMERS[index] = new_customer
            break