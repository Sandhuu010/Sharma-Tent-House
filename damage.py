from decimal import (
    Decimal,
    InvalidOperation
)

from storage import (
    load_data,
    save_data
)

from excel_export import export_to_excel

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

def get_already_damaged_qty(
    booking_id,
    item_id
):

    damage_records = load_data(
        DAMAGE_FILE
    )

    total = 0

    for record in damage_records:

        if (
            record["booking_id"]
            == booking_id
            and
            record["item_id"]
            == item_id
        ):

            total += record["quantity"]

    return total

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

        if b["booking_id"] == booking_id:

            booking = b
            break

    if not booking:

        print("Booking not found.")
        return

    if booking.get("status") == "CLOSED":

        print("Booking already closed.")
        return

    if booking.get(
        "damage_settled",
        False
    ):

        print(
            "Damage already settled."
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

        already_damaged = (
            get_already_damaged_qty(
                booking_id,
                item["item_id"]
            )
        )

        available_damage = (
            item["returned_qty"]
            -
            already_damaged
        )

        print(
            f"{index}. {item_name}"
        )

        print(
            f"   Returned : {item['returned_qty']}"
        )

        print(
            f"   Already Damaged : {already_damaged}"
        )

        print(
            f"   Remaining Damage Qty : {available_damage}"
        )

        print()

    choice = input(
        "Choose item number: "
    ).strip()

    if not choice.isdigit():

        print("Invalid choice.")
        return

    choice = int(choice)

    if not (
        1 <= choice <= len(
            booking["items"]
        )
    ):

        print("Invalid choice.")
        return

    item = booking["items"][
        choice - 1
    ]

    already_damaged = (
        get_already_damaged_qty(
            booking_id,
            item["item_id"]
        )
    )

    max_qty = (
        item["returned_qty"]
        -
        already_damaged
    )

    if max_qty <= 0:

        print(
            "No quantity available for damage entry."
        )

        return

    qty_text = input(
        f"Damaged Quantity (Max {max_qty}): "
    ).strip()

    if not qty_text.isdigit():

        print("Invalid quantity.")
        return

    qty = int(qty_text)

    if qty <= 0:

        print(
            "Quantity must be positive."
        )

        return

    if qty > max_qty:

        print(
            "Damage quantity exceeds allowed limit."
        )

        return

    charge = get_money(
        "Damage Charge: "
    )

    if charge <= 0:

        print(
            "Damage charge must be greater than zero."
        )

        return

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

    booking[
        "damage_settled"
    ] = False

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

        if b["booking_id"] == booking_id:

            booking = b
            break

    if not booking:

        print("Booking not found.")
        return

    if booking.get(
        "damage_settled",
        False
    ):

        print(
            "Damage already settled."
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

        booking[
            "damage_settled"
        ] = True

    elif damage <= deposit:

        refund = (
            deposit - damage
        )

        print(
            f"Refund customer: ₹{refund:.2f}"
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
            f"Collect extra: ₹{extra_due:.2f}"
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

    damages = load_data(
        DAMAGE_FILE
    )

    if not damages:

        print(
            "No damage records."
        )

        return

    rows = []

    for damage in damages:

        rows.append([
            damage["damage_id"],
            damage["booking_id"],
            damage["item_id"],
            damage["quantity"],
            damage["damage_charge"],
            damage["notes"]
        ])

    export_to_excel(
        "damage_records.xlsx",
        [
            "Damage ID",
            "Booking ID",
            "Item ID",
            "Quantity",
            "Damage Charge",
            "Notes"
        ],
        rows
    )