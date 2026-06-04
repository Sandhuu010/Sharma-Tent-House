from datetime import datetime

from storage import (
    load_data,
    save_data
)
from excel_export import export_to_excel

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
            record.get("item_id")
            ==
            item_id
            and
            record.get("status")
            ==
            "UNDER_MAINTENANCE"
        ):

            total += int(
                record.get(
                    "quantity",
                    0
                )
            )

    return total

def search_item_for_maintenance(items):

    while True:

        search = input(
            "\nSearch Item Name: "
        ).strip().lower()

        matches = []

        for item in items:

            if search in item["name"].lower():

                matches.append(item)

        if not matches:

            print(
                "No matching items found."
            )

            continue

        print("\nMatching Items:\n")

        for index, item in enumerate(
            matches,
            start=1
        ):

            print(
                f"{index}. {item['item_id']} | {item['name']}"
            )

        choice = input(
            "\nSelect Item Number: "
        ).strip()

        if (
            choice.isdigit()
            and 1 <= int(choice) <= len(matches)
        ):

            return matches[int(choice) - 1]

        print("Invalid choice.")


def send_to_maintenance():

    items = load_data(ITEMS_FILE)
    records = load_data(MAINTENANCE_FILE)
    bookings = load_data(BOOKINGS_FILE)

    if not items:

        print("No items available.")
        return

    # 🔥 NEW: SEARCH instead of listing all items
    selected_item = search_item_for_maintenance(items)

    item_id = selected_item["item_id"]

    qty_text = input(
        "Quantity: "
    ).strip()

    if (
        not qty_text.isdigit()
        or int(qty_text) <= 0
    ):

        print("Invalid quantity.")
        return

    quantity = int(qty_text)

    total_qty = selected_item["total_quantity"]

    booked_qty = 0

    for booking in bookings:

        for booked_item in booking["items"]:

            if booked_item["item_id"] == item_id:

                booked_qty += (
                    booked_item["quantity"]
                    - booked_item.get("returned_qty", 0)
                )

    already_under_maintenance = get_maintenance_quantity(item_id)

    available = (
        total_qty
        - booked_qty
        - already_under_maintenance
    )

    if quantity > available:

        print(
            f"Only {available} item(s) available to send for maintenance."
        )

        return

    reason = input("Reason: ").strip()

    if not reason:

        print("Reason cannot be empty.")
        return

    record = {

        "maintenance_id": generate_maintenance_id(records),

        "item_id": item_id,

        "quantity": quantity,

        "reason": reason,

        "sent_date": datetime.now().strftime("%Y-%m-%d"),

        "status": "UNDER_MAINTENANCE"
    }

    records.append(record)

    save_data(MAINTENANCE_FILE, records)

    print("\nItem sent to maintenance successfully.")

def return_from_maintenance():

    records = load_data(
        MAINTENANCE_FILE
    )

    active = []

    for record in records:

        if (
            record.get("status")
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

    if (
        record["status"]
        ==
        "RETURNED"
    ):

        print(
            "Already returned."
        )

        return

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

    rows = []

    for record in records:

        rows.append([
            record.get(
                "maintenance_id",
                ""
            ),
            get_item_name(
                record["item_id"]
            ),
            record["quantity"],
            record["reason"],
            record["status"],
            record.get(
                "sent_date",
                ""
            ),
            record.get(
                "returned_date",
                ""
            )
        ])

    export_to_excel(
        "maintenance.xlsx",
        [
            "Maintenance ID",
            "Item",
            "Quantity",
            "Reason",
            "Status",
            "Sent Date",
            "Returned Date"
        ],
        rows
    )

def items_currently_out_report():

    bookings = load_data(
        BOOKINGS_FILE
    )

    customers = load_data(
        CUSTOMERS_FILE
    )

    rows = []

    for booking in bookings:

        if (
            booking.get("status")
            ==
            "CLOSED"
        ):

            continue

        customer_name = ""

        for customer in customers:

            if (
                customer["cust_id"]
                ==
                booking["cust_id"]
            ):

                customer_name = (
                    customer["name"]
                )

                break

        for item in booking["items"]:

            pending = (
                item["quantity"]
                -
                item.get(
                    "returned_qty",
                    0
                )
            )

            if pending > 0:

                rows.append([
                    booking[
                        "booking_id"
                    ],
                    customer_name,
                    get_item_name(
                        item["item_id"]
                    ),
                    pending
                ])

    if not rows:

        print(
            "No items currently out."
        )

        return

    export_to_excel(
        "items_out_report.xlsx",
        [
            "Booking ID",
            "Customer",
            "Item",
            "Pending Qty"
        ],
        rows
    )