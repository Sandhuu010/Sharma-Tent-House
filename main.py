from items import (
    add_item,
    list_items,
    update_item,
    delete_item
)


def main():

    while True:

        print("""
========== SHARMA TENT HOUSE ==========

1. Add Item
2. List Items
3. Update Item
4. Delete Item
5. Exit

=======================================
""")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_item()

        elif choice == "2":
            list_items()

        elif choice == "3":
            update_item()

        elif choice == "4":
            delete_item()

        elif choice == "5":
            print("Program closed.")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()