from datetime import datetime
from decimal import Decimal

from storage import (
    load_data,
    save_data
)

DELIVERY_FILE = (
    "data/delivery_records.json"
)

RETURN_FILE = (
    "data/return_records.json"
)

BOOKINGS_FILE = (
    "data/bookings.json"
)

PAYMENTS_FILE = (
    "data/payments.json"
)


def generate_delivery_id(
    records
):

    highest = 0

    for record in records:

        try:

            number = int(
                record["delivery_id"]
                .split("_")[1]
            )

            highest = max(
                highest,
                number
            )

        except:
            pass

    return (
        f"DEL_{highest + 1:03d}"
    )


def generate_return_id(
    records
):

    highest = 0

    for record in records:

        try:

            number = int(
                record["return_id"]
                .split("_")[1]
            )

            highest = max(
                highest,
                number
            )

        except:
            pass

    return (
        f"RET_{highest + 1:03d}"
    )


def get_booking(
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


def get_balance_due(
    booking
):

    payments = load_data(
        PAYMENTS_FILE
    )

    total_paid = Decimal(
        "0.00"
    )

    for payment in payments:

        if (
            payment["booking_id"]
            ==
            booking["booking_id"]
        ):

            total_paid += Decimal(
                payment["amount"]
            )

    total_amount = Decimal(
        booking[
            "total_rental_amount"
        ]
    )

    advance = Decimal(
        booking["advance"]
    )

    return (
        total_amount
        -
        advance
        -
        total_paid
    )


def mark_delivery():

    bookings = load_data(
        BOOKINGS_FILE
    )

    delivery_records = load_data(
        DELIVERY_FILE
    )

    booking_id = input(
        "Booking ID: "
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

    if (
        booking["status"]
        ==
        "DELIVERED"
    ):

        print(
            "Already delivered."
        )

        return

    if (
        booking["status"]
        ==
        "CLOSED"
    ):

        print(
            "Booking already closed."
        )

        return

    notes = input(
        "Delivery Notes: "
    ).strip()

    delivery = {

        "delivery_id":
            generate_delivery_id(
                delivery_records
            ),

        "booking_id":
            booking_id,

        "delivery_date":
            datetime.now()
            .strftime(
                "%Y-%m-%d %H:%M"
            ),

        "notes":
            notes
    }

    delivery_records.append(
        delivery
    )

    booking["status"] = (
        "DELIVERED"
    )

    save_data(
        DELIVERY_FILE,
        delivery_records
    )

    save_data(
        BOOKINGS_FILE,
        bookings
    )

    print(
        "Delivery recorded."
    )


def record_return():

    bookings = load_data(
        BOOKINGS_FILE
    )

    return_records = load_data(
        RETURN_FILE
    )

    booking_id = input(
        "Booking ID: "
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

    if (
        booking["status"]
        ==
        "CLOSED"
    ):

        print(
            "Booking already closed."
        )

        return

    print("\nItems:\n")

    for index, item in enumerate(
        booking["items"],
        start=1
    ):

        pending = (
            item["quantity"]
            -
            item["returned_qty"]
        )

        print(
            f"{index}. "
            f"{item['item_id']} "
            f"(Pending {pending})"
        )

    choice = input(
        "Choose item: "
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
        f"Return Qty (Max {remaining}): "
    ).strip()

    if (
        not qty_text.isdigit()
    ):

        print(
            "Invalid quantity."
        )

        return

    qty = int(
        qty_text
    )

    if qty <= 0:

        print(
            "Quantity must be positive."
        )

        return

    if qty > remaining:

        print(
            "Return exceeds booked quantity."
        )

        return

    item["returned_qty"] += qty

    return_record = {

        "return_id":
            generate_return_id(
                return_records
            ),

        "booking_id":
            booking_id,

        "item_id":
            item["item_id"],

        "quantity":
            qty,

        "return_date":
            datetime.now()
            .strftime(
                "%Y-%m-%d %H:%M"
            )
    }

    return_records.append(
        return_record
    )

    fully_returned = True

    for booked_item in booking[
        "items"
    ]:

        if (
            booked_item[
                "returned_qty"
            ]
            <
            booked_item[
                "quantity"
            ]
        ):

            fully_returned = False
            break

    if fully_returned:

        booking["status"] = (
            "READY_TO_CLOSE"
        )

    else:

        booking["status"] = (
            "PARTIAL_RETURN"
        )

    save_data(
        BOOKINGS_FILE,
        bookings
    )

    save_data(
        RETURN_FILE,
        return_records
    )

    print(
        "Return recorded."
    )

def close_booking():

    bookings = load_data(
        BOOKINGS_FILE
    )

    booking_id = input(
        "Booking ID: "
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

    if (
        booking.get("status")
        ==
        "CLOSED"
    ):

        print(
            "Booking already closed."
        )

        return

    # Check pending returns

    for item in booking["items"]:

        pending = (
            item["quantity"]
            -
            item["returned_qty"]
        )

        if pending > 0:

            print(
                f"{item['item_id']} "
                f"still has "
                f"{pending} pending."
            )

            print(
                "Cannot close booking."
            )

            return

    # Check payment balance

    balance_due = (
        get_balance_due(
            booking
        )
    )

    if balance_due > 0:

        print(
            f"Balance Due: "
            f"₹{balance_due:.2f}"
        )

        print(
            "Cannot close booking."
        )

        return

    # Check damage settlement

    damage_amount = Decimal(
        booking.get(
            "damage_amount",
            "0.00"
        )
    )

    damage_settled = (
        booking.get(
            "damage_settled",
            False
        )
    )

    if (
        damage_amount > 0
        and
        not damage_settled
    ):

        print(
            "Damage settlement pending."
        )

        print(
            "Use 'Settle Damage' first."
        )

        return

    # Close booking

    booking["status"] = (
        "CLOSED"
    )

    save_data(
        BOOKINGS_FILE,
        bookings
    )

    print(
        "\nBooking closed successfully."
    )


def items_currently_out_report():

    bookings = load_data(
        BOOKINGS_FILE
    )

    found = False

    print(
        "\n===== ITEMS CURRENTLY OUT =====\n"
    )

    for booking in bookings:

        for item in booking[
            "items"
        ]:

            pending = (
                item["quantity"]
                -
                item["returned_qty"]
            )

            if pending > 0:

                found = True

                print(
                    f"Booking: "
                    f"{booking['booking_id']}"
                )

                print(
                    f"Item: "
                    f"{item['item_id']}"
                )

                print(
                    f"Pending: "
                    f"{pending}"
                )

                print(
                    "-"
                    * 30
                )

    if not found:

        print(
            "No items currently out."
        )