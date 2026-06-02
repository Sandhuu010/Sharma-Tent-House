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


def main():

    while True:

        print("""
========== SHARMA TENT HOUSE ==========

INVENTORY

1. Add Item
2. View Items
3. Update Item
4. Delete Item

CUSTOMERS

5. Add Customer
6. View Customers

BOOKINGS

7. Check Availability
8. Create Booking
9. List Bookings

PAYMENTS

10. Record Payment
11. Booking Summary

DELIVERY & RETURNS

12. Mark Delivery
13. Record Return
14. Close Booking

DAMAGE MANAGEMENT

15. Record Damage
16. Damage Summary
17. Settle Damage
18. View Damage Records

MAINTENANCE & REPORTS

19. Send Item To Maintenance
20. Return Item From Maintenance
21. View Maintenance Records
22. Items Currently Out Report

23. Exit

=======================================
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

            add_customer()

        elif choice == "6":

            view_customers()

        elif choice == "7":

            check_availability()

        elif choice == "8":

            create_booking()

        elif choice == "9":

            list_bookings()

        elif choice == "10":

            record_payment()

        elif choice == "11":

            booking_summary()

        elif choice == "12":

            mark_delivery()

        elif choice == "13":

            record_return()

        elif choice == "14":

            close_booking()

        elif choice == "15":

            record_damage()

        elif choice == "16":

            damage_summary()

        elif choice == "17":

            settle_damage()

        elif choice == "18":

            view_damage_records()

        elif choice == "19":

            send_to_maintenance()

        elif choice == "20":

            return_from_maintenance()

        elif choice == "21":

            view_maintenance_records()

        elif choice == "22":

            items_currently_out_report()

        elif choice == "23":

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