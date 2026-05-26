from storage import load_items, save_items


def generate_item_id(items):
    if not items:
        return "ITEM_001"

    last_id = items[-1]["item_id"]
    number = int(last_id.split("_")[1]) + 1

    return f"ITEM_{number:03}"


def add_item():
    items = load_items()

    name = input("Enter item name: ")
    quantity = int(input("Enter total quantity: "))
    rate = input("Enter rate per day: ")
    item_type = input("Enter item type:(Quantity/Limited/Unique) ")

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

    if not items:
        print("No items yet.")
        return

    print("\n===== ITEMS =====")

    for item in items:
        print(f"""
ID: {item['item_id']}
Name: {item['name']}
Quantity: {item['total_quantity']}
Rate/Day: {item['rate_per_day']}
Type: {item['item_type']}
-------------------------
""")


def update_item():
    items = load_items()

    item_id = input("Enter item ID to update: ")

    for item in items:
        if item["item_id"] == item_id:

            print("Leave blank to keep old value.")

            new_name = input(f"New name ({item['name']}): ")
            new_quantity = input(f"New quantity ({item['total_quantity']}): ")
            new_rate = input(f"New rate ({item['rate_per_day']}): ")
            new_type = input(f"New type ({item['item_type']}): ")

            if new_name:
                item["name"] = new_name

            if new_quantity:
                item["total_quantity"] = int(new_quantity)

            if new_rate:
                item["rate_per_day"] = new_rate

            if new_type:
                item["item_type"] = new_type

            save_items(items)

            print("Item updated successfully.")
            return

    print("Item not found.")


def delete_item():
    items = load_items()

    item_id = input("Enter item ID to delete: ")

    for item in items:
        if item["item_id"] == item_id:
            items.remove(item)

            save_items(items)

            print("Item deleted successfully.")
            return

    print("Item not found.")