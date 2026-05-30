from datetime import datetime

from storage import (
    load_data,
    save_data
)

ITEMS_FILE = "data/items.json"
BOOKINGS_FILE = "data/bookings.json"


def generate_booking_id(bookings):

    highest = 0

    for booking in bookings:

        number = int(
            booking["booking_id"]
            .split("_")[1]
        )

        highest = max(
            highest,
            number
        )

    return f"BOOK_{highest + 1:03d}"


def parse_datetime(text):

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

    total_quantity = 0

    for item in items:

        if item["item_id"] == item_id:

            total_quantity = (
                item["total_quantity"]
            )

            break

    booked_quantity = 0

    for booking in bookings:

        booking_start = (
            parse_datetime(
                booking["start_date"]
            )
        )

        booking_return = (
            parse_datetime(
                booking[
                    "return_datetime"
                ]
            )
        )

        if not booking_overlaps(

            booking_start,

            booking_return,

            query_start,

            query_end

        ):

            continue

        for booked_item in booking["items"]:

            if (
                booked_item["item_id"]
                ==
                item_id
            ):

                active_qty = (

                    booked_item[
                        "quantity"
                    ]

                    -

                    booked_item[
                        "returned_qty"
                    ]

                )

                booked_quantity += (
                    active_qty
                )

    return (
        total_quantity
        -
        booked_quantity
    )

def check_availability():

    item_id = input(
        "Item ID: "
    ).strip()

    start = input(
        "Start Date [YYYY-MM-DD]: "
    ).strip()

    end = input(
        "Return Date [YYYY-MM-DD HH:MM]: "
    ).strip()

    query_start = (
        parse_datetime(start)
    )

    query_end = (
        parse_datetime(end)
    )

    if (
        not query_start
        or
        not query_end
    ):

        print(
            "Invalid date."
        )

        return

    available = (
        get_available_quantity(
            item_id,
            query_start,
            query_end
        )
    )

    print(
        f"\nAvailable: "
        f"{available}"
    )

def create_booking():

    bookings = load_data(
        BOOKINGS_FILE
    )

    customer_name = input(
        "Customer Name: "
    ).strip()

    phone = input(
        "Phone: "
    ).strip()

    address = input(
        "Address: "
    ).strip()

    start_date = input(
        "Start Date [YYYY-MM-DD]: "
    ).strip()

    return_datetime = input(
        "Return Date [YYYY-MM-DD HH:MM]: "
    ).strip()

    item_id = input(
        "Item ID: "
    ).strip()

    quantity = int(
        input(
            "Quantity: "
        )
    )

    advance = input(
        "Advance Amount: "
    ).strip()

    deposit = input(
        "Deposit Amount: "
    ).strip()

    total_amount = input(
        "Total Amount: "
    ).strip()

    query_start = (
        parse_datetime(
            start_date
        )
    )

    query_end = (
        parse_datetime(
            return_datetime
        )
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
            f"Only "
            f"{available} "
            f"available."
        )

        return

    booking = {

        "booking_id":
            generate_booking_id(
                bookings
            ),

        "customer_name":
            customer_name,

        "phone":
            phone,

        "address":
            address,

        "start_date":
            start_date,

        "return_datetime":
            return_datetime,

        "advance":
            advance,

        "deposit":
            deposit,

        "total_amount":
            total_amount,

        "items": [

            {

                "item_id":
                    item_id,

                "quantity":
                    quantity,

                "returned_qty":
                    0
            }

        ],

        "status":
            "ACTIVE"
    }

    bookings.append(
        booking
    )

    save_data(
        BOOKINGS_FILE,
        bookings
    )

    print(
        "\nBooking created."
    )

def list_bookings():

    bookings = load_data(
        BOOKINGS_FILE
    )

    if not bookings:

        print(
            "No bookings."
        )

        return

    for booking in bookings:

        print(f"""

Booking ID :
{booking['booking_id']}

Customer :
{booking['customer_name']}

Phone :
{booking['phone']}

Start :
{booking['start_date']}

Return :
{booking['return_datetime']}

Advance :
{booking['advance']}

Deposit :
{booking['deposit']}

Total :
{booking['total_amount']}

Status :
{booking['status']}

--------------------------------
""")
        
def record_return():

    bookings = load_data(
        BOOKINGS_FILE
    )

    booking_id = input(
        "Booking ID: "
    )

    for booking in bookings:

        if (
            booking["booking_id"]
            ==
            booking_id
        ):

            item = (
                booking["items"][0]
            )

            remaining = (

                item["quantity"]

                -

                item[
                    "returned_qty"
                ]
            )

            print(
                f"Remaining: "
                f"{remaining}"
            )

            qty = int(
                input(
                    "Return Qty: "
                )
            )

            if qty > remaining:

                print(
                    "Too many."
                )

                return

            item[
                "returned_qty"
            ] += qty

            save_data(
                BOOKINGS_FILE,
                bookings
            )

            print(
                "Return saved."
            )

            return

    print(
        "Booking not found."
    )

def customer_history():

    bookings = load_data(
        BOOKINGS_FILE
    )

    phone = input(
        "Phone: "
    )

    found = False

    for booking in bookings:

        if (
            booking["phone"]
            ==
            phone
        ):

            found = True

            print(f"""

Booking :
{booking['booking_id']}

Customer :
{booking['customer_name']}

Start :
{booking['start_date']}

Return :
{booking['return_datetime']}

Amount :
{booking['total_amount']}

-----------------------
""")

    if not found:

        print(
            "No history found."
        )

from decimal import Decimal


def booking_summary():

    bookings = load_data(
        BOOKINGS_FILE
    )

    booking_id = input(
        "Booking ID: "
    )

    for booking in bookings:

        if (
            booking["booking_id"]
            ==
            booking_id
        ):

            total = Decimal(
                booking[
                    "total_amount"
                ]
            )

            advance = Decimal(
                booking[
                    "advance"
                ]
            )

            balance = (
                total
                -
                advance
            )

            print(f"""

Customer :
{booking['customer_name']}

Total :
₹{total}

Advance :
₹{advance}

Balance :
₹{balance}

""")

            return

    print(
        "Booking not found."
    )

