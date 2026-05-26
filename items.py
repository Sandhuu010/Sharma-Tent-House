from storage import load_data, save_data


ITEMS_FILE = "data/items.json"


def generate_item_id(items):

    # Find highest existing number
    highest = 0

    for item in items:

        item_id = item["item_id"]

        number = int(item_id.split("_")[1])

        if number > highest:
            highest = number

    next_number = highest + 1

    return f"ITEM_{next_number:03}"


def get_valid_quantity():

    while True:

        quantity = input("Enter total quantity: ").strip()

        if quantity == "":
            print("Quantity cannot be empty.")
            continue

        if not quantity.isdigit():
            print("Quantity must be a positive number.")
            continue

        quantity = int(quantity)

        if quantity < 0:
            print("Quantity cannot be negative.")
            continue

        return quantity


def get_valid_rate():

    while True:

        rate = input(
            "Enter rate per day (example 5.00): "
        ).strip()

        if rate == "":
            print("Rate cannot be empty.")
            continue

        try:

            value = float(rate)

            if value < 0:
                print("Rate cannot be negative.")
                continue

            return f"{value:.2f}"

        except ValueError:
            print("Invalid rate. Enter valid number.")


def add_item():

    items = load_data(ITEMS_FILE)

    name = input("Enter item name: ").strip()

    if name == "":
        print("Item name cannot be empty.")
        return

    quantity = get_valid_quantity()

    rate = get_valid_rate()

    item_type = input("Enter item type:(Quantity/Limited/Unique) ").strip()

    new_item = {
        "item_id": generate_item_id(items),
        "name": name,
        "total_quantity": quantity,
        "rate_per_day": rate,
        "item_type": item_type
    }

    items.append(new_item)

    save_data(ITEMS_FILE, items)

    print("Item added successfully.")


def list_items():

    items = load_data(ITEMS_FILE)

    if not items:
        print("No items yet.")
        return

    print("\n========== ITEM LIST ==========")

    for item in items:

        print(f"""
Item ID       : {item['item_id']}
Name          : {item['name']}
Quantity      : {item['total_quantity']}
Rate Per Day  : {item['rate_per_day']}
Item Type     : {item['item_type']}
-----------------------------------
""")


def update_item():

    items = load_data(ITEMS_FILE)

    item_name = input(
        "Enter item name to update: "
    ).strip()

    for item in items:

        if item["name"].lower() == item_name.lower():

            print("\nLeave blank to keep old value.\n")

            new_name = input(
                f"New name [{item['name']}]: "
            ).strip()

            new_quantity = input(
                f"New quantity [{item['total_quantity']}]: "
            ).strip()

            new_rate = input(
                f"New rate [{item['rate_per_day']}]: "
            ).strip()

            new_type = input(
                f"New type [{item['item_type']}]: "
            ).strip()

            if new_name:
                item["name"] = new_name

            if new_quantity:

                if new_quantity.isdigit():

                    quantity = int(new_quantity)

                    if quantity >= 0:
                        item["total_quantity"] = quantity

                    else:
                        print("Negative quantity not allowed.")

                else:
                    print("Invalid quantity. Old value kept.")

            if new_rate:

                try:

                    rate = float(new_rate)

                    if rate >= 0:
                        item["rate_per_day"] = f"{rate:.2f}"

                    else:
                        print("Negative rate not allowed.")

                except ValueError:
                    print("Invalid rate. Old value kept.")

            if new_type:
                item["item_type"] = new_type

            save_data(ITEMS_FILE, items)

            print("Item updated successfully.")

            return

    print("Item not found.")


def delete_item():

    items = load_data(ITEMS_FILE)

    item_name = input(
        "Enter item name to delete: "
    ).strip()

    for item in items:

        if item["name"].lower() == item_name.lower():

            confirm = input(
                f"Delete {item['name']}? (yes/no): "
            ).strip().lower()

            if confirm == "yes":

                items.remove(item)

                save_data(ITEMS_FILE, items)

                print("Item deleted successfully.")

            else:
                print("Delete cancelled.")

            return

    print("Item not found.")