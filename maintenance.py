from datetime import datetime

from storage import (
    load_data,
    save_data
)

ITEMS_FILE = "data/items.json"
BOOKINGS_FILE = "data/bookings.json"
CUSTOMERS_FILE = "data/customers.json"

MAINTENANCE_FILE = (
    "data/maintenance_records.json"
)


def generate_maintenance_id(
    records
):

    highest = 0

    for record in records:

        try:

            number = int(
                record["maintenance_id"]
                .split("_")[1]
            )

            highest = max(
                highest,
                number
            )

        except (
            ValueError,
            KeyError,
            IndexError
        ):
            pass

    return (
        f"MAIN_{highest + 1:03d}"
    )


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


def get_customer_name(
    cust_id
):

    customers = load_data(
        CUSTOMERS_FILE
    )

    for customer in customers:

        if (
            customer["cust_id"]
            ==
            cust_id
        ):

            return customer["name"]

    return "Unknown"


def get_maintenance_quantity(
    item_id
):

    records = load_data(
        MAINTENANCE_FILE
    )

    total = 0

    for record in records:

        if (
            record["item_id"]
            ==
            item_id
            and
            record["status"]
            ==
            "UNDER_MAINTENANCE"
        ):

            total += (
                record["quantity"]
            )

    return total


def send_to_maintenance():

    items = load_data(
        ITEMS_FILE
    )

    records = load_data(
        MAINTENANCE_FILE
    )

    if not items:

        print(
            "No items available."
        )

        return

    print("\nAvailable Items:\n")

    for item in items:

        print(
            f"{item['item_id']} "
            f"- "
            f"{item['name']}"
        )

    item_id = input(
        "\nItem ID: "
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
            "Item not found."
        )

        return

    qty_text = input(
        "Quantity: "
    ).strip()

    if not qty_text.isdigit():

        print(
            "Invalid quantity."
        )

        return

    quantity = int(
        qty_text
    )

    if quantity <= 0:

        print(
            "Quantity must be positive."
        )

        return

    reason = input(
        "Reason: "
    ).strip()

    record = {

        "maintenance_id":
            generate_maintenance_id(
                records
            ),

        "item_id":
            item_id,

        "quantity":
            quantity,

        "reason":
            reason,

        "sent_date":
            datetime.now()
            .strftime(
                "%Y-%m-%d"
            ),

        "status":
            "UNDER_MAINTENANCE"
    }

    records.append(
        record
    )

    save_data(
        MAINTENANCE_FILE,
        records
    )

    print(
        "\nItem sent to maintenance."
    )


def return_from_maintenance():

    records = load_data(
        MAINTENANCE_FILE
    )

    active = []

    for record in records:

        if (
            record["status"]
            ==
            "UNDER_MAINTENANCE"
        ):

            active.append(
                record
            )

    if not active:

        print(
            "No items in maintenance."
        )

        return

    print(
        "\nMaintenance Records:\n"
    )

    for index, record in enumerate(
        active,
        start=1
    ):

        print(
            f"{index}. "
            f"{record['maintenance_id']}"
        )

        print(
            f"   Item : "
            f"{get_item_name(record['item_id'])}"
        )

        print(
            f"   Qty  : "
            f"{record['quantity']}"
        )

        print(
            f"   Date : "
            f"{record['sent_date']}"
        )

        print()

    choice = input(
        "Choose record: "
    ).strip()

    if not choice.isdigit():

        print(
            "Invalid choice."
        )

        return

    choice = int(
        choice
    )

    if not (
        1 <= choice <= len(active)
    ):

        print(
            "Invalid choice."
        )

        return

    record = active[
        choice - 1
    ]

    record["status"] = (
        "RETURNED"
    )

    record[
        "returned_date"
    ] = datetime.now().strftime(
        "%Y-%m-%d"
    )

    save_data(
        MAINTENANCE_FILE,
        records
    )

    print(
        "Item returned from maintenance."
    )


def view_maintenance_records():

    records = load_data(
        MAINTENANCE_FILE
    )

    if not records:

        print(
            "No maintenance records."
        )

        return

    print(
        "\n===== MAINTENANCE RECORDS =====\n"
    )

    for record in records:

        print(
            f"Maintenance ID : "
            f"{record['maintenance_id']}"
        )

        print(
            f"Item           : "
            f"{get_item_name(record['item_id'])}"
        )

        print(
            f"Quantity       : "
            f"{record['quantity']}"
        )

        print(
            f"Reason         : "
            f"{record['reason']}"
        )

        print(
            f"Status         : "
            f"{record['status']}"
        )

        print(
            f"Sent Date      : "
            f"{record['sent_date']}"
        )

        if (
            "returned_date"
            in record
        ):

            print(
                f"Returned Date  : "
                f"{record['returned_date']}"
            )

        print(
            "-" * 40
        )


def items_currently_out_report():

    bookings = load_data(
        BOOKINGS_FILE
    )

    active = []

    for booking in bookings:

        if (
            booking.get("status")
            != "CLOSED"
        ):

            active.append(
                booking
            )

    active.sort(
        key=lambda booking:
        booking["return_datetime"]
    )

    if not active:

        print(
            "No active bookings."
        )

        return

    print(
        "\n===== ITEMS CURRENTLY OUT =====\n"
    )

    for booking in active:

        print(
            f"Booking : "
            f"{booking['booking_id']}"
        )

        print(
            f"Customer: "
            f"{get_customer_name(
                booking['cust_id']
            )}"
        )

        print(
            f"Return  : "
            f"{booking['return_datetime']}"
        )

        print(
            "\nItems:"
        )

        for item in booking["items"]:

            pending = (
                item["quantity"]
                -
                item["returned_qty"]
            )

            if pending > 0:

                print(
                    f"  {get_item_name(item['item_id'])}"
                    f" | Pending: "
                    f"{pending}"
                )

        print(
            "-" * 40
        )