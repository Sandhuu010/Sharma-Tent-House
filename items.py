from storage import load_data, save_data


ITEMS_FILE = "data/items.json"


def normalize_text(text):

    return text.strip().lower()


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

        rate = input("Enter rate: ").strip()

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

    search_text = normalize_text(search_text)

    for item in items:

        if search_text in normalize_text(item["name"]):
            matches.append(item)

    return matches


def choose_item(matches):

    if len(matches) == 1:
        return matches[0]

    print("\nMatching Items:\n")

    for index, item in enumerate(matches, start=1):

        print(
            f"{index}. {item['name']} "
            f"({item['category']})"
        )

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

    normalized_name = normalize_text(name)

    # Duplicate check
    for item in items:

        if normalize_text(item["name"]) == normalized_name:
            print("Item already exists.")
            return

    category = input(
        "Enter category (Chair/Table/etc): "
    ).strip()

    quantity = get_valid_quantity()

    rate = get_valid_rate()

    new_item = {
        "item_id": generate_item_id(items),
        "name": name,
        "category": category,
        "total_quantity": quantity,
        "rate": rate
    }

    items.append(new_item)

    save_data(ITEMS_FILE, items)

    print(f"{name} added successfully.")


def print_items(items):

    for item in items:

        print(f"""
Item ID   : {item['item_id']}
Name      : {item['name']}
Category  : {item['category']}
Quantity  : {item['total_quantity']}
Rate      : {item['rate']}
-----------------------------------
""")


def view_items():

    items = load_data(ITEMS_FILE)

    if not items:
        print("No items yet.")
        return

    print("""
1. View All Items
2. Search By Name
3. Search By Category
""")

    choice = input("Enter choice: ").strip()

    if choice == "1":

        print_items(items)

    elif choice == "2":

        search = input(
            "Enter item name: "
        ).strip()

        matches = search_items(items, search)

        if matches:
            print_items(matches)

        else:
            print("No matching items found.")

    elif choice == "3":

        category = input(
            "Enter category: "
        ).strip().lower()

        matches = []

        for item in items:

            if normalize_text(item["category"]) == category:
                matches.append(item)

        if matches:
            print_items(matches)

        else:
            print("No items found in this category.")

    else:
        print("Invalid choice.")


def update_item():

    items = load_data(ITEMS_FILE)

    search = input(
        "Enter item name to search: "
    ).strip()

    matches = search_items(items, search)

    if not matches:
        print("No matching items found.")
        return

    item = choose_item(matches)

    print("\nLeave blank to keep old value.\n")

    new_name = input(
        f"New name [{item['name']}]: "
    ).strip()

    new_category = input(
        f"New category [{item['category']}]: "
    ).strip()

    new_quantity = input(
        f"New quantity [{item['total_quantity']}]: "
    ).strip()

    new_rate = input(
        f"New rate [{item['rate']}]: "
    ).strip()

    if new_name:
        item["name"] = new_name

    if new_category:
        item["category"] = new_category

    if new_quantity.isdigit():
        item["total_quantity"] = int(new_quantity)

    if new_rate:

        try:
            item["rate"] = f"{float(new_rate):.2f}"

        except ValueError:
            print("Invalid rate. Old value kept.")

    save_data(ITEMS_FILE, items)

    print(f"{item['name']} updated successfully.")


def delete_item():

    items = load_data(ITEMS_FILE)

    search = input(
        "Enter item name to search: "
    ).strip()

    matches = search_items(items, search)

    if not matches:
        print("No matching items found.")
        return

    item = choose_item(matches)

    confirm = input(
        f"Delete {item['name']}? (yes/no): "
    ).strip().lower()

    if confirm == "yes":

        item_name = item["name"]

        items.remove(item)

        save_data(ITEMS_FILE, items)

        print(f"{item_name} deleted successfully.")

    else:
        print("Delete cancelled.")