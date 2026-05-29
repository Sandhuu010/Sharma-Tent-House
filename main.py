from items import (
    add_item,
    view_items,
    update_item,
    delete_item
)


def main():

    while True:

        print("""
========== SHARMA TENT HOUSE ==========

1. Add Item
2. View Items
3. Update Item
4. Delete Item
5. Exit

=======================================
""")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_item()

        elif choice == "2":
            view_items()

        elif choice == "3":
            update_item()

        elif choice == "4":
            delete_item()

        elif choice == "5":
            print("Program closed.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()