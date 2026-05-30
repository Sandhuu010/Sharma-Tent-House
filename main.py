from items import (
    add_item,
    view_items,
    update_item,
    delete_item
)

from bookings import (
    create_booking,
    list_bookings,
    check_availability,
    record_return,
    customer_history,
    booking_summary
)


def main():

    while True:

        print("""
=========================================
         SHARMA TENT HOUSE
=========================================

INVENTORY

1. Add Item
2. View Items
3. Update Item
4. Delete Item

BOOKINGS

5. Check Availability
6. Create Booking
7. List Bookings
8. Record Return
9. Booking Summary
10. Customer History

11. Exit

=========================================
""")

        choice = input(
            "Enter choice: "
        ).strip()

        # Inventory

        if choice == "1":
            add_item()

        elif choice == "2":
            view_items()

        elif choice == "3":
            update_item()

        elif choice == "4":
            delete_item()

        # Bookings

        elif choice == "5":
            check_availability()

        elif choice == "6":
            create_booking()

        elif choice == "7":
            list_bookings()

        elif choice == "8":
            record_return()

        elif choice == "9":
            booking_summary()

        elif choice == "10":
            customer_history()

        # Exit

        elif choice == "11":

            print(
                "\nProgram closed."
            )

            break

        else:

            print(
                "\nInvalid choice."
            )


if __name__ == "__main__":
    main()