from datetime import datetime

from decimal import (
    Decimal,
    InvalidOperation
)

from storage import load_data, save_data

from customers import (
    get_or_create_customer
)

from maintenance import (
    get_maintenance_quantity
)

ITEMS_FILE = "data/items.json"
BOOKINGS_FILE = "data/bookings.json"
CUSTOMERS_FILE = "data/customers.json"


def generate_booking_id(bookings):

    highest = 0

    for booking in bookings:

        try:

            number = int(
                booking["booking_id"]
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

    return f"BOOK_{highest + 1:03d}"


def get_datetime(text):

    formats = [
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M"
    ]

    for fmt in formats:

        try:

            return datetime.strptime(
                text,
                fmt
            )

        except ValueError:
            pass

    return None

def get_money(prompt):

    while True:

        value = input(prompt).strip()

        try:

            amount = Decimal(value)

            if amount < 0:

                print(
                    "Amount cannot be negative."
                )

                continue

            return amount

        except InvalidOperation:

            print(
                "Invalid amount."
            )

def booking_overlaps(
    booking_start,
    booking_return,
    query_start,
    query_end
):

    return (
        booking_start < query_end
        and
        booking_return > query_start
    )


def get_available_quantity(
    item_id,
    query_start,
    query_end
):

    items = load_data(
        ITEMS_FILE
    )

    bookings = load_data(
        BOOKINGS_FILE
    )

    total_qty = 0

    for item in items:

        if (
            item["item_id"]
            ==
            item_id
        ):

            total_qty = (
                item["total_quantity"]
            )

            break

    booked_qty = 0

    for booking in bookings:

        booking_start = get_datetime(
            booking["start_date"]
        )

        booking_return = get_datetime(
            booking["return_datetime"]
        )

        if not booking_overlaps(
            booking_start,
            booking_return,
            query_start,
            query_end
        ):

            continue

        for booked_item in booking[
            "items"
        ]:

            if (
                booked_item["item_id"]
                ==
                item_id
            ):

                booked_qty += (

                    booked_item[
                        "quantity"
                    ]

                    -

                    booked_item[
                        "returned_qty"
                    ]
                )

    maintenance_qty = (
        get_maintenance_quantity(
            item_id
        )
    )

    available = (

        total_qty

        -

        booked_qty

        -

        maintenance_qty
    )

    return max(
        0,
        available
    )

def calculate_rental_total(
    booking_items
):

    items = load_data(
        ITEMS_FILE
    )

    total = Decimal("0.00")

    for booked_item in booking_items:

        for item in items:

            if (
                item["item_id"]
                ==
                booked_item["item_id"]
            ):

                rate = Decimal(
                    item["rate"]
                )

                qty = Decimal(
                    str(
                        booked_item[
                            "quantity"
                        ]
                    )
                )

                total += (
                    rate * qty
                )

                break

    return total

def create_booking():

    customer = (
        get_or_create_customer()
    )

    if not customer:
        return

    items = load_data(
        ITEMS_FILE
    )

    bookings = load_data(
        BOOKINGS_FILE
    )

    if not items:

        print(
            "No items available."
        )

        return

    start_date = input(
        "Start date [YYYY-MM-DD]: "
    ).strip()

    return_date = input(
        "Return date [YYYY-MM-DD HH:MM]: "
    ).strip()

    query_start = get_datetime(
        start_date
    )

    query_end = get_datetime(
        return_date
    )

    if (
        not query_start
        or
        not query_end
    ):

        print("Invalid date.")
        return

    if query_end <= query_start:

        print(
            "Return date must be after start date."
        )

        return

    booking_items = []

    while True:

        print(
            "\nAvailable Items:\n"
        )

        for item in items:

         print(
        f"{item['item_id']} | "
        f"{item['name']} | "
        f"Qty: {item['total_quantity']} | "
        f"Rate: ₹{item['rate']}"
        )

        item_id = input(
            "\nEnter Item ID: "
        ).strip()

        selected_item = None

        for item in items:

            if (
                item["item_id"]
                ==
                item_id
            ):

                selected_item = item
                break

        if not selected_item:

            print(
                "Invalid Item ID."
            )

            continue

        quantity_text = input(
            "Quantity: "
        ).strip()

        if (
            not quantity_text.isdigit()
            or
            int(quantity_text) <= 0
        ):

            print(
                "Invalid quantity."
            )

            continue

        quantity = int(
            quantity_text
        )

        available = (
            get_available_quantity(
                item_id,
                query_start,
                query_end
            )
        )

        if quantity > available:

            print(
                f"Only {available} available."
            )

            continue

        duplicate = False

        for booked_item in booking_items:

            if (
                booked_item[
                    "item_id"
                ]
                ==
                item_id
            ):

                booked_item[
                    "quantity"
                ] += quantity

                duplicate = True

                break

        if not duplicate:

            booking_items.append(
                {
                    "item_id":
                        item_id,

                    "quantity":
                        quantity,

                    "returned_qty":
                        0
                }
            )

        choice = input(
            "Add another item? (y/n): "
        ).strip().lower()

        if choice != "y":
            break

    if not booking_items:

        print(
            "No items added."
        )

        return

    rental_total = (
        calculate_rental_total(
            booking_items
        )
    )

    print(
        f"\nRental Total = "
        f"₹{rental_total:.2f}"
    )

    advance = get_money(
        "Advance Received: "
    )

    if advance > rental_total:

        print(
            "Advance cannot exceed rental total."
        )

        return

    deposit = get_money(
        "Security Deposit: "
    )

    booking = {

    "booking_id":
        generate_booking_id(
            bookings
        ),

    "cust_id":
        customer["cust_id"],

    "status":
        "OPEN",

    "start_date":
        start_date,

    "return_datetime":
        return_date,

    "total_rental_amount":
        f"{rental_total:.2f}",

    "advance":
        f"{advance:.2f}",

    "deposit":
        f"{deposit:.2f}",

    "damage_amount":
        "0.00",

    "damage_settled":
        True,

    "items":
        booking_items
}

    bookings.append(
        booking
    )

    save_data(
        BOOKINGS_FILE,
        bookings
    )

    print(
        f"\n{booking['booking_id']} "
        f"created successfully."
    )

    print(
        f"Customer : "
        f"{customer['name']}"
    )

    print(
        f"Rental Total : "
        f"₹{rental_total:.2f}"
    )

    print(
        f"Advance : "
        f"₹{advance:.2f}"
    )

    print(
        f"Deposit : "
        f"₹{deposit:.2f}"
    )


def check_availability():

    item_id = input(
        "Enter Item ID: "
    ).strip()

    start_date = input(
        "Start date [YYYY-MM-DD]: "
    ).strip()

    return_date = input(
        "Return date [YYYY-MM-DD HH:MM]: "
    ).strip()

    query_start = get_datetime(
        start_date
    )

    query_end = get_datetime(
        return_date
    )

    if (
        not query_start
        or
        not query_end
    ):

        print("Invalid date.")
        return

    available = (
        get_available_quantity(
            item_id,
            query_start,
            query_end
        )
    )
    
    maintenance_qty = (
        get_maintenance_quantity(
        item_id
        )
)
    print(
        f"Available Quantity: "
        f"{available}"
    )
    
    print(
        f"Under Maintenance  : "
        f"{maintenance_qty}"
)

def mark_return():

    bookings = load_data(
        BOOKINGS_FILE
    )

    booking_id = input(
        "Enter Booking ID: "
    ).strip()

    booking = None

    for b in bookings:

        if (
            b["booking_id"]
            ==
            booking_id
        ):

            booking = b
            break

    if not booking:

        print(
            "Booking not found."
        )

        return

    print("\nItems:\n")

    for index, item in enumerate(
        booking["items"],
        start=1
    ):

        print(
            f"{index}. "
            f"{item['item_id']} "
            f"(Booked: {item['quantity']}, "
            f"Returned: {item['returned_qty']})"
        )

    choice = input(
        "\nChoose item number: "
    ).strip()

    if not choice.isdigit():

        print(
            "Invalid choice."
        )

        return

    choice = int(choice)

    if not (
        1 <= choice <= len(
            booking["items"]
        )
    ):

        print(
            "Invalid choice."
        )

        return

    item = booking[
        "items"
    ][choice - 1]

    remaining = (
        item["quantity"]
        -
        item["returned_qty"]
    )

    qty_text = input(
        f"Return Quantity (Max {remaining}): "
    ).strip()

    if (
        not qty_text.isdigit()
    ):

        print(
            "Invalid quantity."
        )

        return

    qty = int(qty_text)

    if qty > remaining:

        print(
            "Return exceeds booked quantity."
        )

        return

    item["returned_qty"] += qty

    save_data(
        BOOKINGS_FILE,
        bookings
    )

    print(
        "Return recorded."
    )


def list_bookings():

    bookings = load_data(
        BOOKINGS_FILE
    )

    customers = load_data(
        CUSTOMERS_FILE
    )

    if not bookings:

        print(
            "No bookings yet."
        )

        return

    for booking in bookings:

        customer_name = (
            "Unknown Customer"
        )

        customer_phone = ""

        if "cust_id" in booking:

            for customer in customers:

                if (
                    customer["cust_id"]
                    ==
                    booking["cust_id"]
                ):

                    customer_name = (
                        customer["name"]
                    )

                    customer_phone = (
                        customer["phone"]
                    )

                    break

        print(
            f"\nBooking ID : "
            f"{booking['booking_id']}"
        )

        print(
            f"Customer   : "
            f"{customer_name}"
        )

        print(
            f"Phone      : "
            f"{customer_phone}"
        )

        print(
            f"Status     : "
            f"{booking.get('status', 'OPEN')}"
        )
        
        print(
            f"Rental Amt  : ₹"
            f"{booking.get('total_rental_amount', '0.00')}"
        )

        print(
            f"Advance     : ₹"
            f"{booking.get('advance', '0.00')}"
        )

        print(
            f"Deposit     : ₹"
            f"{booking.get('deposit', '0.00')}"
        )

        print(
            f"Damage Amt  : ₹"
            f"{booking.get('damage_amount', '0.00')}"
        )

        print(
            f"Damage Done : "
            f"{booking.get('damage_settled', False)}"
        )
        print(
            f"Start Date : "
            f"{booking['start_date']}"
        )

        print(
            f"Return Date: "
            f"{booking['return_datetime']}"
        )

        print("\nItems:")

        for item in booking["items"]:

           pending = (
             item["quantity"]
             -
             item["returned_qty"]
           )

           print(
              f"{item['item_id']} "
              f"| Qty: {item['quantity']} "
              f"| Returned: {item['returned_qty']} "
              f"| Pending: {pending}"
           )

        print("-" * 40)

def get_booking_by_id(
    booking_id
):

    bookings = load_data(
        BOOKINGS_FILE
    )

    for booking in bookings:

        if (
            booking["booking_id"]
            ==
            booking_id
        ):

            return booking

    return None

def booking_fully_returned(
    booking
):

    for item in booking["items"]:

        if (
            item["returned_qty"]
            <
            item["quantity"]
        ):

            return False

    return True


def get_pending_items(
    booking
):

    pending = []

    for item in booking["items"]:

        remaining = (
            item["quantity"]
            -
            item["returned_qty"]
        )

        if remaining > 0:

            pending.append(
                {
                    "item_id":
                        item["item_id"],

                    "pending":
                        remaining
                }
            )

    return pending

def get_damage_amount(
    booking
):

    return Decimal(
        booking.get(
            "damage_amount",
            "0.00"
        )
    )