from items import (
    add_item,
    list_items,
    search_item,
    update_item,
    delete_item
)


def main():

    while True:

        print("""
========== SHARMA TENT HOUSE ==========

1. Add Item
2. List Items
3. Search Item
4. Update Item
5. Delete Item
6. Exit

=======================================
""")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_item()

        elif choice == "2":
            list_items()

        elif choice == "3":
            search_item()

        elif choice == "4":
            update_item()

        elif choice == "5":
            delete_item()

        elif choice == "6":
            print("Program closed.")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()