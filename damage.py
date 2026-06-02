from decimal import (
    Decimal,
    InvalidOperation
)

from storage import (
    load_data,
    save_data
)

DAMAGE_FILE = (
    "data/damage_records.json"
)

BOOKINGS_FILE = (
    "data/bookings.json"
)

ITEMS_FILE = (
    "data/items.json"
)


def generate_damage_id(
    records
):

    highest = 0

    for record in records:

        try:

            number = int(
                record["damage_id"]
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

    return (
        f"DAM_{highest + 1:03d}"
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


def get_item_name(
    item_id
):

    items = load_data(
        ITEMS_FILE
    )

    for item in items:

        if (
            item["item_id"]
            ==
            item_id
        ):

            return item["name"]

    return item_id


def get_money(
    prompt
):

    while True:

        value = input(
            prompt
        ).strip()

        try:

            amount = Decimal(
                value
            )

            if amount < 0:

                print(
                    "Amount cannot be negative."
                )

                continue

            return amount

        except (
            InvalidOperation
        ):

            print(
                "Invalid amount."
            )


def record_damage():

    bookings = load_data(
        BOOKINGS_FILE
    )

    damage_records = load_data(
        DAMAGE_FILE
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
        booking.get(
            "status"
        )
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

        item_name = get_item_name(
            item["item_id"]
        )

        print(
            f"{index}. "
            f"{item_name}"
        )

        print(
            f"   Booked   : "
            f"{item['quantity']}"
        )

        print(
            f"   Returned : "
            f"{item['returned_qty']}"
        )

        print()

    choice = input(
        "Choose item number: "
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

    max_qty = (
        item["returned_qty"]
    )

    qty_text = input(
        f"Damaged Quantity "
        f"(Max {max_qty}): "
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

    if qty > max_qty:

        print(
            "Damage quantity exceeds returned quantity."
        )

        return

    charge = get_money(
        "Damage Charge: "
    )

    notes = input(
        "Notes: "
    ).strip()

    damage_record = {

        "damage_id":
            generate_damage_id(
                damage_records
            ),

        "booking_id":
            booking_id,

        "item_id":
            item["item_id"],

        "quantity":
            qty,

        "damage_charge":
            f"{charge:.2f}",

        "notes":
            notes
    }

    damage_records.append(
        damage_record
    )

    current_damage = Decimal(
        booking.get(
            "damage_amount",
            "0.00"
        )
    )

    booking[
        "damage_amount"
    ] = (
        f"{current_damage + charge:.2f}"
    )

    booking["status"] = (
        "DAMAGE_PENDING"
    )

    save_data(
        DAMAGE_FILE,
        damage_records
    )

    save_data(
        BOOKINGS_FILE,
        bookings
    )

    print(
        "Damage recorded successfully."
    )


def damage_summary():

    booking_id = input(
        "Booking ID: "
    ).strip()

    booking = get_booking(
        booking_id
    )

    if not booking:

        print(
            "Booking not found."
        )

        return

    deposit = Decimal(
        booking.get(
            "deposit",
            "0.00"
        )
    )

    damage = Decimal(
        booking.get(
            "damage_amount",
            "0.00"
        )
    )

    print(
        "\n===== DAMAGE SUMMARY =====\n"
    )

    print(
        f"Booking ID    : "
        f"{booking_id}"
    )

    print(
        f"Deposit       : "
        f"₹{deposit:.2f}"
    )

    print(
        f"Damage Amount : "
        f"₹{damage:.2f}"
    )

    if damage <= deposit:

        refund = (
            deposit - damage
        )

        print(
            f"Refund Due    : "
            f"₹{refund:.2f}"
        )

    else:

        extra_due = (
            damage - deposit
        )

        print(
            f"Extra Due     : "
            f"₹{extra_due:.2f}"
        )


def settle_damage():

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

    deposit = Decimal(
        booking.get(
            "deposit",
            "0.00"
        )
    )

    damage = Decimal(
        booking.get(
            "damage_amount",
            "0.00"
        )
    )

    if damage == 0:

        print(
            "No damage recorded."
        )

        booking[
            "damage_settled"
        ] = True

    elif damage <= deposit:

        refund = (
            deposit - damage
        )

        print(
            f"Refund customer: "
            f"₹{refund:.2f}"
        )

        confirm = input(
            "Settlement completed? (y/n): "
        ).strip().lower()

        if confirm != "y":
            return

        booking[
            "damage_settled"
        ] = True

    else:

        extra_due = (
            damage - deposit
        )

        print(
            f"Collect extra: "
            f"₹{extra_due:.2f}"
        )

        confirm = input(
            "Amount collected? (y/n): "
        ).strip().lower()

        if confirm != "y":
            return

        booking[
            "damage_settled"
        ] = True

    save_data(
        BOOKINGS_FILE,
        bookings
    )

    print(
        "Damage settlement completed."
    )


def view_damage_records():

    records = load_data(
        DAMAGE_FILE
    )

    if not records:

        print(
            "No damage records."
        )

        return

    print(
        "\n===== DAMAGE RECORDS =====\n"
    )

    for record in records:

        print(
            f"Damage ID : "
            f"{record['damage_id']}"
        )

        print(
            f"Booking   : "
            f"{record['booking_id']}"
        )

        print(
            f"Item      : "
            f"{get_item_name(record['item_id'])}"
        )

        print(
            f"Qty       : "
            f"{record['quantity']}"
        )

        print(
            f"Charge    : ₹"
            f"{record['damage_charge']}"
        )

        print(
            f"Notes     : "
            f"{record['notes']}"
        )

        print(
            "-" * 40
        )