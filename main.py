from items import (
    add_item,
    view_items,
    update_item,
    delete_item
)

from customers import (
    add_customer,
    view_customers
)

from bookings import (
    check_availability,
    create_booking,
    list_bookings
)
from payments import (
    record_payment,
    booking_summary
)

from delivery import (
    mark_delivery,
    record_return,
    close_booking
)

from damage import (
    record_damage,
    damage_summary,
    settle_damage,
    view_damage_records
)

from maintenance import (
    send_to_maintenance,
    return_from_maintenance,
    view_maintenance_records,
    items_currently_out_report
)


def inventory_menu():

    while True:

        print("""
========== INVENTORY ==========

1. Add Item
2. View Items
3. Update Item
4. Delete Item
5. Back

==============================
""")

        choice = input(
            "Enter choice: "
        ).strip()

        if choice == "1":

            add_item()

        elif choice == "2":

            view_items()

        elif choice == "3":

            update_item()

        elif choice == "4":

            delete_item()

        elif choice == "5":

            break

        else:

            print("Invalid choice.")


def customer_menu():

    while True:

        print("""
========== CUSTOMERS ==========

1. Add Customer
2. View Customers
3. Back

==============================
""")

        choice = input(
            "Enter choice: "
        ).strip()

        if choice == "1":

            add_customer()

        elif choice == "2":

            view_customers()

        elif choice == "3":

            break

        else:

            print("Invalid choice.")


def booking_menu():

    while True:

        print("""
========== BOOKINGS ==========

1. Check Availability
2. Create Booking
3. List Bookings
4. Back

==============================
""")

        choice = input(
            "Enter choice: "
        ).strip()

        if choice == "1":

            check_availability()

        elif choice == "2":

            create_booking()

        elif choice == "3":

            list_bookings()

        elif choice == "4":

            break

        else:

            print("Invalid choice.")


def payment_menu():

    while True:

        print("""
========== PAYMENTS ==========

1. Record Payment
2. Booking Summary
3. Back

==============================
""")

        choice = input(
            "Enter choice: "
        ).strip()

        if choice == "1":

            record_payment()

        elif choice == "2":

            booking_summary()

        elif choice == "3":

            break

        else:

            print("Invalid choice.")


def delivery_menu():

    while True:

        print("""
====== DELIVERY & RETURNS ======

1. Mark Delivery
2. Record Return
3. Close Booking
4. Back

================================
""")

        choice = input(
            "Enter choice: "
        ).strip()

        if choice == "1":

            mark_delivery()

        elif choice == "2":

            record_return()

        elif choice == "3":

            close_booking()

        elif choice == "4":

            break

        else:

            print("Invalid choice.")


def damage_menu():

    while True:

        print("""
======= DAMAGE MANAGEMENT =======

1. Record Damage
2. Damage Summary
3. Settle Damage
4. View Damage Records
5. Back

=================================
""")

        choice = input(
            "Enter choice: "
        ).strip()

        if choice == "1":

            record_damage()

        elif choice == "2":

            damage_summary()

        elif choice == "3":

            settle_damage()

        elif choice == "4":

            view_damage_records()

        elif choice == "5":

            break

        else:

            print("Invalid choice.")


def maintenance_menu():

    while True:

        print("""
====== MAINTENANCE & REPORTS ======

1. Send Item To Maintenance
2. Return Item From Maintenance
3. View Maintenance Records
4. Items Currently Out Report
5. Back

===================================
""")

        choice = input(
            "Enter choice: "
        ).strip()

        if choice == "1":

            send_to_maintenance()

        elif choice == "2":

            return_from_maintenance()

        elif choice == "3":

            view_maintenance_records()

        elif choice == "4":

            items_currently_out_report()

        elif choice == "5":

            break

        else:

            print("Invalid choice.")


def main():

    while True:

        print("""
========== SHARMA TENT HOUSE ==========

1. Inventory
2. Customers
3. Bookings
4. Payments
5. Delivery & Returns
6. Damage Management
7. Maintenance & Reports
8. Exit

=======================================
""")

        choice = input(
            "Enter choice: "
        ).strip()

        if choice == "1":

            inventory_menu()

        elif choice == "2":

            customer_menu()

        elif choice == "3":

            booking_menu()

        elif choice == "4":

            payment_menu()

        elif choice == "5":

            delivery_menu()

        elif choice == "6":

            damage_menu()

        elif choice == "7":

            maintenance_menu()

        elif choice == "8":

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