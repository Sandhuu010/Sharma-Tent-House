from storage import load_data, save_data
from excel_export import export_to_excel

CUSTOMERS_FILE = "data/customers.json"
BOOKINGS_FILE = "data/bookings.json"


def generate_customer_id(customers):

    highest = 0

    for customer in customers:

        try:

            number = int(
                customer["cust_id"]
                .split("_")[1]
            )

            highest = max(
                highest,
                number
            )

        except (
            KeyError,
            ValueError,
            IndexError
        ):
            pass

    return f"CUST_{highest + 1:03d}"

def get_valid_phone():

    while True:

        phone = input(
            "Phone Number: "
        ).strip()

        if not phone:

            print(
                "Phone number cannot be empty."
            )

            continue

        if not phone.isdigit():

            print(
                "Phone number must contain digits only."
            )

            continue

        if len(phone) != 10:

            print(
                "Phone number must be exactly 10 digits."
            )

            continue

        return phone

def search_customers(search_text):

    customers = load_data(
        CUSTOMERS_FILE
    )

    matches = []

    search_text = (
        search_text
        .strip()
        .lower()
    )

    for customer in customers:

        if (

            search_text
            in
            customer["name"]
            .lower()

            or

            search_text
            in
            customer["phone"]

        ):

            matches.append(
                customer
            )

    return matches

def choose_customer(matches):

    if len(matches) == 1:

        return matches[0]

    while True:

        choice = input(
            "Choose customer number: "
        ).strip()

        if choice.isdigit():

            choice = int(choice)

            if (
                1 <= choice <= len(matches)
            ):

                return matches[
                    choice - 1
                ]

        print(
            "Invalid choice."
        )

def add_customer():

    customers = load_data(
        CUSTOMERS_FILE
    )

    while True:

        name = input(
            "Customer Name: "
        ).strip()

        if name:
            break

        print(
            "Customer name cannot be empty."
        )

    phone = get_valid_phone()

    address = input(
        "Address: "
    ).strip()

    if not address:

        print(
            "Address cannot be empty."
        )

        return

    for customer in customers:

        if customer["phone"] == phone:

            print(
                "Customer already exists."
            )

            return

    customer = {

        "cust_id":
            generate_customer_id(
                customers
            ),

        "name":
            name,

        "phone":
            phone,

        "address":
            address
    }

    customers.append(
        customer
    )

    save_data(
        CUSTOMERS_FILE,
        customers
    )

    print(
        f"{name} added successfully."
    )

def view_customers():

    customers = load_data(
        CUSTOMERS_FILE
    )

    bookings = load_data(
        BOOKINGS_FILE
    )

    if not customers:

        print(
            "No customers found."
        )

        return

    rows = []

    for customer in customers:

        booking_count = 0

        for booking in bookings:

            if (
                booking["cust_id"]
                ==
                customer["cust_id"]
            ):

                booking_count += 1

        rows.append(
            {
                "Customer ID":
                    customer["cust_id"],

                "Name":
                    customer["name"],

                "Phone":
                    customer["phone"],

                "Address":
                    customer["address"],

                "Total Bookings":
                    booking_count
            }
        )

    from excel_export import (
        export_to_excel
    )

    export_to_excel(
        "customers.xlsx",
        rows
    )

def customer_history():

    search = input(
        "Enter name or phone: "
    ).strip()

    matches = search_customers(
        search
    )

    if not matches:

        print("Customer not found.")
        return

    customer = choose_customer(
        matches
    )

    bookings = load_data(
        BOOKINGS_FILE
    )

    print(
        f"\nCustomer: "
        f"{customer['name']}"
    )

    print("\nBookings:\n")

    found = False

    for booking in bookings:

        if (
            booking["cust_id"]
            ==
            customer["cust_id"]
        ):

            print(
                f"{booking['booking_id']}"
            )

            print(
                f"Start: "
                f"{booking['start_date']}"
            )

            print()

            found = True

    if not found:

        print(
            "No bookings found."
        )

def get_or_create_customer():

    customers = load_data(
        CUSTOMERS_FILE
    )

    search = input(
        "Customer Name/Phone: "
    ).strip()

    matches = search_customers(
        search
    )

    if matches:

        print(
            "\nCustomer(s) Found:\n"
        )

        for index, customer in enumerate(
            matches,
            start=1
        ):

            print(
                f"{index}. {customer['name']}"
            )

            print(
                f"   Phone   : {customer['phone']}"
            )

            print(
                f"   Address : {customer['address']}"
            )

            print()

        customer = choose_customer(
            matches
        )

        confirm = input(
            f"Use {customer['name']}? (y/n): "
        ).strip().lower()

        if confirm == "y":

            return customer

        create_new = input(
            "Create a new customer instead? (y/n): "
        ).strip().lower()

        if create_new != "y":

            return None

    else:

        print(
            "\nCustomer not found."
        )

        create_new = input(
            "Create new customer? (y/n): "
        ).strip().lower()

        if create_new != "y":

            return None

    print("\nEnter New Customer Details\n")

    while True:

        name = input(
            "Customer Name: "
        ).strip()

        if name:
            break

        print(
            "Name cannot be empty."
        )

    while True:

        phone = get_valid_phone()

        if not phone:

            print(
                "Phone cannot be empty."
            )
            continue

        duplicate = False

        for customer in customers:

            if customer["phone"] == phone:

                duplicate = True
                break

        if duplicate:

            print(
                "Phone number already exists."
            )

            use_existing = input(
                "Use existing customer? (y/n): "
            ).strip().lower()

            if use_existing == "y":

                return customer

            continue

        break
    while True:
      address = input(
        "Address: "
    ).strip()
      if address:
          break
      print("Address cannot be empty")
      
    new_customer = {

        "cust_id":
            generate_customer_id(
                customers
            ),

        "name":
            name,

        "phone":
            phone,

        "address":
            address
    }

    customers.append(
        new_customer
    )

    save_data(
        CUSTOMERS_FILE,
        customers
    )

    print(
        f"{name} added successfully."
    )

    return new_customer