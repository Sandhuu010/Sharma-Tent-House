from storage import load_items, save_items


def generate_item_id(items):

    if len(items) == 0:
        return "ITEM_001"

    last_id = items[-1]["item_id"]

    number = int(last_id.split("_")[1]) + 1

    return f"ITEM_{number:03}"


def add_item():

    items = load_items()

    name = input("Enter item name: ")
    quantity = int(input("Enter quantity: "))
    rate = input("Enter rate per day: ")
    item_type = input("Enter item type: ")

    item = {
        "item_id": generate_item_id(items),
        "name": name,
        "total_quantity": quantity,
        "rate_per_day": rate,
        "item_type": item_type
    }

    items.append(item)

    save_items(items)

    print("Item added successfully.")


def list_items():

    items = load_items()

    if len(items) == 0:
        print("No items yet.")
        return

    print("\n===== ITEMS =====")

    for item in items:

        print(f"""
ID: {item['item_id']}
Name: {item['name']}
Quantity: {item['total_quantity']}
Rate Per Day: {item['rate_per_day']}
Type: {item['item_type']}
------------------------
""")