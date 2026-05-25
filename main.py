from items import add_item, list_items


while True:

    print("""
====== SHARMA TENT HOUSE ======

1. Add Item
2. List Items
3. Exit
""")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_item()

    elif choice == "2":
        list_items()

    elif choice == "3":
        print("Program closed.")
        break

    else:
        print("Invalid choice.")