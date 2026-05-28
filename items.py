from storage import load_data, save_data


ITEMS_FILE = "data/items.json"


def normalize_text(text):

    return text.strip().lower()


def item_exists(items, item_name, exclude_item=None):

    normalized_name = normalize_text(item_name)

    for item in items:

        # Ignore current item during update
        if exclude_item == item:
            continue

        if normalize_text(item["name"]) == normalized_name:
            return True

    return False


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

    # Empty name check
    if normalized_name == "":
        print("Item name cannot be empty.")
        return

    # Duplicate check
    if item_exists(items, name):
        print("Item already exists.")
        return

    category = input(
        "Enter category (Chair/Table/etc): "
    ).strip()

    if category == "":
        print("Category cannot be empty.")
        return

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

    print(f"\nTotal Items Found: {len(items)}")

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
        ).strip()

        matches = []

        for item in items:

            if normalize_text(
                item["category"]
            ) == normalize_text(category):

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

    new_category = input(
        f"New category [{item['category']}]: "
    ).strip()

    new_quantity = input(
        f"New quantity [{item['total_quantity']}]: "
    ).strip()

    new_rate = input(
        f"New rate [{item['rate']}]: "
    ).strip()

    # Name update validation
    if new_name:

        normalized_name = normalize_text(new_name)

        if normalized_name == "":
            print("Item name cannot be empty.")

        elif item_exists(
            items,
            new_name,
            exclude_item=item
        ):
            print(
                "Another item with this name already exists."
            )

        else:
            item["name"] = new_name

    # Category update
    if new_category:
        item["category"] = new_category

    # Quantity update
    if new_quantity:

        if new_quantity.isdigit():

            quantity = int(new_quantity)

            if quantity >= 0:
                item["total_quantity"] = quantity

            else:
                print("Negative quantity not allowed.")

        else:
            print("Invalid quantity. Old value kept.")

    # Rate update
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

    print(f"{item['name']} updated successfully.")


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

        item_name = item["name"]

        items.remove(item)

        save_data(ITEMS_FILE, items)

        print(f"{item_name} deleted successfully.")

    else:
        print("Delete cancelled.")