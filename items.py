from storage import load_data, save_data


ITEMS_FILE = "data/items.json"


def generate_item_id(items):

    highest = 0

    for item in items:

        number = int(item["item_id"].split("_")[1])

        if number > highest:
            highest = number

    return f"ITEM_{highest + 1:03d}"


def get_valid_quantity():

    while True:

        quantity = input("Enter quantity: ").strip()

        if quantity == "":
            print("Quantity cannot be empty.")
            continue

        if not quantity.isdigit():
            print("Quantity must be a number.")
            continue

        quantity = int(quantity)

        if quantity < 0:
            print("Quantity cannot be negative.")
            continue

        return quantity


def get_valid_rate():

    while True:

        rate = input("Enter rate: ").strip()

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
            print("Invalid rate.")


def search_items(items, search_text):

    matches = []

    search_text = search_text.lower()

    for item in items:

        if search_text in item["name"].lower():
            matches.append(item)

    return matches


def choose_item(matches):

    if len(matches) == 1:
        return matches[0]

    print("\nMatching Items:\n")

    for index, item in enumerate(matches, start=1):

        print(f"{index}. {item['name']}")

    while True:

        choice = input(
            "Choose item number: "
        ).strip()

        if choice.isdigit():

            choice = int(choice)

            if 1 <= choice <= len(matches):
                return matches[choice - 1]

        print("Invalid choice.")


def add_item():

    items = load_data(ITEMS_FILE)

    name = input("Enter item name: ").strip()

    if name == "":
        print("Item name cannot be empty.")
        return

    quantity = get_valid_quantity()

    rate = get_valid_rate()

    new_item = {
        "item_id": generate_item_id(items),
        "name": name,
        "total_quantity": quantity,
        "rate": rate
    }

    items.append(new_item)

    save_data(ITEMS_FILE, items)

    print("Item added successfully.")


def list_items():

    items = load_data(ITEMS_FILE)

    if not items:
        print("No items yet.")
        return

    print("\n========== ITEMS ==========")

    for item in items:

        print(f"""
Item ID   : {item['item_id']}
Name      : {item['name']}
Quantity  : {item['total_quantity']}
Rate      : {item['rate']}
-----------------------------
""")


def search_item():

    items = load_data(ITEMS_FILE)

    if not items:
        print("No items yet.")
        return

    search = input(
        "Enter item name to search: "
    ).strip()

    matches = search_items(items, search)

    if not matches:

        print("\nNo matching items found.")

        print("\nAvailable items:")

        for item in items:
            print("-", item["name"])

        return

    print("\n========== SEARCH RESULTS ==========")

    for item in matches:

        print(f"""
Item ID   : {item['item_id']}
Name      : {item['name']}
Quantity  : {item['total_quantity']}
Rate      : {item['rate']}
-----------------------------
""")


def update_item():

    items = load_data(ITEMS_FILE)

    search = input(
        "Enter item name to search: "
    ).strip()

    matches = search_items(items, search)

    if not matches:

        print("\nNo matching items found.")

        print("\nAvailable items:")

        for item in items:
            print("-", item["name"])

        return

    item = choose_item(matches)

    print("\nLeave blank to keep old value.\n")

    new_name = input(
        f"New name [{item['name']}]: "
    ).strip()

    new_quantity = input(
        f"New quantity [{item['total_quantity']}]: "
    ).strip()

    new_rate = input(
        f"New rate [{item['rate']}]: "
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
                item["rate"] = f"{rate:.2f}"

            else:
                print("Negative rate not allowed.")

        except ValueError:
            print("Invalid rate. Old value kept.")

    save_data(ITEMS_FILE, items)

    print("Item updated successfully.")


def delete_item():

    items = load_data(ITEMS_FILE)

    search = input(
        "Enter item name to search: "
    ).strip()

    matches = search_items(items, search)

    if not matches:

        print("\nNo matching items found.")

        print("\nAvailable items:")

        for item in items:
            print("-", item["name"])

        return

    item = choose_item(matches)

    confirm = input(
        f"Delete {item['name']}? (yes/no): "
    ).strip().lower()

    if confirm == "yes":

        items.remove(item)

        save_data(ITEMS_FILE, items)

        print("Item deleted successfully.")

    else:
        print("Delete cancelled.")