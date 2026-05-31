from storage import load_data, save_data

CUSTOMERS_FILE = "data/customers.json"
BOOKINGS_FILE = "data/bookings.json"


def generate_customer_id(customers):

    highest = 0

    for customer in customers:

        number = int(
            customer["cust_id"].split("_")[1]
        )

        highest = max(highest, number)

    return f"CUST_{highest + 1:03d}"


def search_customers(search_text):

    customers = load_data(
        CUSTOMERS_FILE
    )

    matches = []

    search_text = search_text.lower()

    for customer in customers:

        if (
            search_text in customer["name"].lower()
            or
            search_text in customer["phone"]
        ):
            matches.append(customer)

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

    name = input(
        "Customer Name: "
    ).strip()

    phone = input(
        "Phone Number: "
    ).strip()

    address = input(
        "Address: "
    ).strip()

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

    customers.append(customer)

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

        print("No customers yet.")
        return

    for customer in customers:

        print(
            f"\nCustomer ID : "
            f"{customer['cust_id']}"
        )

        print(
            f"Name        : "
            f"{customer['name']}"
        )

        print(
            f"Phone       : "
            f"{customer['phone']}"
        )

        print(
            f"Address     : "
            f"{customer['address']}"
        )

        print("\nBookings:")

        found = False

        for booking in bookings:

            if (
                booking["cust_id"]
                ==
                customer["cust_id"]
            ):

                print(
                    booking["booking_id"]
                )

                found = True

        if not found:
            print("No bookings.")

        print("-" * 40)


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

        phone = input(
            "Phone Number: "
        ).strip()

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

    address = input(
        "Address: "
    ).strip()

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