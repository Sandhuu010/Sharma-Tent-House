from datetime import datetime

from decimal import (
    Decimal,
    InvalidOperation
)

from excel_export import export_to_excel

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
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d"
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

def search_item_for_booking(
    items,
    query_start,
    query_end
):

    while True:

        search = input(
            "\nSearch Item: "
        ).strip().lower()

        if not search:

            print(
                "Search cannot be empty."
            )

            continue

        matches = []

        for item in items:

            if search in item["name"].lower():

                available = (
                    get_available_quantity(
                        item["item_id"],
                        query_start,
                        query_end
                    )
                )

                if available > 0:

                    matches.append(
                        (
                            item,
                            available
                        )
                    )

        if not matches:

            print(
                "No matching available item found."
            )

            continue

        print("\nMatching Items:\n")

        for index, (
            item,
            available
        ) in enumerate(
            matches,
            start=1
        ):

            print(
                f"{index}. "
                f"{item['name']}"
            )

            print(
                f"   Item ID       : "
                f"{item['item_id']}"
            )

            print(
                f"   Available Qty : "
                f"{available}"
            )

            print(
                f"   Rate          : "
                f"₹{item['rate']}"
            )

            print("-" * 40)

        choice = input(
            "\nSelect Item Number: "
        ).strip()

        if (
            choice.isdigit()
            and
            1 <= int(choice) <= len(matches)
        ):

            return matches[
                int(choice) - 1
            ][0]

        print(
            "Invalid choice."
        )

def show_booking_summary(
    booking,
    customer
):

    print("\n" + "=" * 50)

    print(
        "\nBOOKING CREATED SUCCESSFULLY\n"
    )

    print(
        f"Booking ID : "
        f"{booking['booking_id']}"
    )

    print(
        f"Customer   : "
        f"{customer['name']}"
    )

    print(
        f"Occasion   : "
        f"{booking['occasion']}"
    )

    print(
        f"Start      : "
        f"{booking['start_date']}"
    )

    print(
        f"Return     : "
        f"{booking['return_datetime']}"
    )

    print("\nItems:")

    for item in booking["items"]:

        print(
            f"{item['item_name']} "
            f"| Qty: {item['quantity']}"
        )

    print(
        f"\nRental Total : ₹"
        f"{booking['total_rental_amount']}"
    )

    print(
        f"Discount     : ₹"
        f"{booking['discount']}"
    )

    print(
        f"Final Amount : ₹"
        f"{booking['final_amount']}"
    )

    print(
        f"Advance      : ₹"
        f"{booking['advance']}"
    )

    print(
        f"Deposit      : ₹"
        f"{booking['deposit']}"
    )

    print(
        f"Balance      : ₹"
        f"{booking['balance_due']}"
    )

    print("\n" + "=" * 50)

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

    while True:

        print(
            "\nExample: 2026-06-15 10:00"
        )

        start_date = input(
            "Start Date [YYYY-MM-DD HH:MM]: "
        ).strip()

        return_date = input(
            "Return Date [YYYY-MM-DD HH:MM]: "
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

            print(
                "Invalid date format."
            )

            continue

        if query_end <= query_start:

            print(
                "Return date must be after start date."
            )

            continue

        break

    occasion = input(
        "Occasion: "
    ).strip()

    if not occasion:

        occasion = "General"

    booking_items = []

    while True:

        selected_item = (
            search_item_for_booking(
                items,
                query_start,
                query_end
            )
        )

        item_id = (
            selected_item["item_id"]
        )

        available = (
            get_available_quantity(
                item_id,
                query_start,
                query_end
            )
        )

        while True:

            qty_text = input(
                f"Quantity (Available {available}): "
            ).strip()

            if (
                not qty_text.isdigit()
                or
                int(qty_text) <= 0
            ):

                print(
                    "Invalid quantity."
                )

                continue

            quantity = int(
                qty_text
            )

            if quantity > available:

                print(
                    f"Only {available} available."
                )

                continue

            break

        found = False

        for booked_item in booking_items:

            if (
                booked_item["item_id"]
                ==
                item_id
            ):

                booked_item[
                    "quantity"
                ] += quantity

                found = True

                break

        if not found:

            booking_items.append(
                {
                    "item_id":
                        item_id,

                    "item_name":
                        selected_item["name"],

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
            "No items selected."
        )

        return

    rental_total = (
        calculate_rental_total(
            booking_items
        )
    )

    print(
        f"\nRental Total : "
        f"₹{rental_total:.2f}"
    )

    while True:

        discount = get_money(
            "Discount: "
        )

        if discount > rental_total:

            print(
                "Discount cannot exceed rental amount."
            )

            continue

        break

    final_total = (
        rental_total - discount
    )

    print(
        f"Final Total : "
        f"₹{final_total:.2f}"
    )

    while True:

        advance = get_money(
            "Advance Received: "
        )

        if advance > final_total:

            print(
                "Advance cannot exceed final amount."
            )

            continue

        break

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

        "occasion":
            occasion,

        "status":
            "OPEN",

        "start_date":
            start_date,

        "return_datetime":
            return_date,

        "discount":
            f"{discount:.2f}",

        "total_rental_amount":
            f"{final_total:.2f}",

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
        "\n========== BOOKING SUMMARY =========="
    )

    print(
        f"Booking ID : "
        f"{booking['booking_id']}"
    )

    print(
        f"Customer   : "
        f"{customer['name']}"
    )

    print(
        f"Phone      : "
        f"{customer['phone']}"
    )

    print(
        f"Occasion   : "
        f"{occasion}"
    )

    print(
        f"Start      : "
        f"{start_date}"
    )

    print(
        f"Return     : "
        f"{return_date}"
    )

    print("\nItems:")

    for item in booking_items:

        print(
            f"{item['item_name']} "
            f"| Qty: {item['quantity']}"
        )

    print(
        f"\nDiscount : ₹{discount:.2f}"
    )

    print(
        f"Final Total : ₹{final_total:.2f}"
    )

    print(
        f"Advance : ₹{advance:.2f}"
    )

    print(
        f"Deposit : ₹{deposit:.2f}"
    )

    print(
        "\nBooking created successfully."
    )

def check_availability():

    items = load_data(ITEMS_FILE)

    if not items:
        print("No items available.")
        return

    # STEP 1: SEARCH BY NAME (NEW UX)
    while True:

        search = input("\nSearch Item Name: ").strip().lower()

        matches = []

        for item in items:

            if search in item["name"].lower():
                matches.append(item)

        if not matches:
            print("No matching items found.")
            continue

        print("\nMatching Items:\n")

        for index, item in enumerate(matches, start=1):

            print(
                f"{index}. {item['name']} | "
                f"Qty: {item['total_quantity']} | "
                f"Rate: ₹{item['rate']}"
            )

        choice = input("\nSelect Item Number: ").strip()

        if (
            choice.isdigit()
            and 1 <= int(choice) <= len(matches)
        ):
            selected_item = matches[int(choice) - 1]
            break

        print("Invalid choice. Try again.")

    # STEP 2: DATE INPUT (same workflow as before)
    print("\nExample: 2026-06-15 10:00")

    start_date = input(
        "Start date [YYYY-MM-DD HH:MM]: "
    ).strip()

    return_date = input(
        "Return date [YYYY-MM-DD HH:MM]: "
    ).strip()

    query_start = get_datetime(start_date)
    query_end = get_datetime(return_date)

    if not query_start or not query_end:
        print("Invalid date.")
        return

    if query_end <= query_start:
        print("Return date must be after start date.")
        return

    # STEP 3: AVAILABILITY CHECK (unchanged logic)
    item_id = selected_item["item_id"]

    available = get_available_quantity(
        item_id,
        query_start,
        query_end
    )

    maintenance_qty = get_maintenance_quantity(item_id)

    print("\n========== AVAILABILITY ==========")
    print(f"Item        : {selected_item['name']}")
    print(f"Available   : {available}")
    print(f"Maintenance : {maintenance_qty}")
    print("=================================")

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

    bookings = load_data(BOOKINGS_FILE)
    customers = load_data(CUSTOMERS_FILE)

    if not bookings:
        print("No bookings found.")
        return

    rows = []

    for booking in bookings:

        customer_name = ""
        customer_phone = ""

        for customer in customers:

            if customer["cust_id"] == booking["cust_id"]:
                customer_name = customer["name"]
                customer_phone = customer["phone"]
                break

        rows.append({
            "Booking ID": booking["booking_id"],
            "Customer": customer_name,
            "Phone": customer_phone,
            "Occasion": booking.get("occasion", ""),
            "Status": booking.get("status", "OPEN"),
            "Amount": booking.get("total_rental_amount", "0.00"),
            "Start Date": booking["start_date"],
            "Return Date": booking["return_datetime"]
        })

    export_to_excel(
        "bookings.xlsx",
        rows
    )

    
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