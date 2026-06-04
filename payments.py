from decimal import (
    Decimal,
    InvalidOperation
)

from storage import (
    load_data,
    save_data
)

BOOKINGS_FILE = "data/bookings.json"
PAYMENTS_FILE = "data/payments.json"


def generate_payment_id(payments):

    highest = 0

    for payment in payments:

        try:

            number = int(
                payment["payment_id"]
                .split("_")[1]
            )

            highest = max(
                highest,
                number
            )

        except (
            KeyError,
            ValueError,
            IndexError
        ):
            pass

    return f"PAY_{highest + 1:03d}"


def get_money(prompt):

    while True:

        value = input(prompt).strip()

        try:

            amount = Decimal(value)

            if amount < 0:

                print(
                    "Amount cannot be negative."
                )

                continue

            return amount

        except InvalidOperation:

            print(
                "Invalid amount."
            )


def get_booking(booking_id):

    booking_id = booking_id.strip().upper()

    bookings = load_data(
        BOOKINGS_FILE
    )

    for booking in bookings:

        if (
            booking["booking_id"].upper()
            ==
            booking_id
        ):

            return booking

    return None

def get_total_payments(
    booking_id
):

    payments = load_data(
        PAYMENTS_FILE
    )

    total = Decimal("0.00")

    for payment in payments:

        if (
            payment["booking_id"]
            ==
            booking_id
        ):

            total += Decimal(
                payment["amount"]
            )

    return total

def get_balance_due(
    booking
):

    try:

        total_amount = Decimal(
            booking[
                "total_rental_amount"
            ]
        )

        advance = Decimal(
            booking["advance"]
        )

    except (
        InvalidOperation,
        KeyError
    ):

        return Decimal("0.00")

    total_paid = (
        get_total_payments(
            booking[
                "booking_id"
            ]
        )
    )

    balance = (
        total_amount
        -
        advance
        -
        total_paid
    )

    return max(
        Decimal("0.00"),
        balance
    )

def booking_summary():

    booking_id = input(
        "Booking ID: "
    ).strip()

    if booking_id == "":

        print(
            "Booking ID cannot be empty."
        )

        return

    booking = get_booking(
        booking_id
    )

    if not booking:

        print(
            "Booking not found."
        )

        return

    try:

        total_amount = Decimal(
            booking[
                "total_rental_amount"
            ]
        )

        advance = Decimal(
            booking["advance"]
        )

        deposit = Decimal(
            booking["deposit"]
        )

    except (
        InvalidOperation,
        KeyError
    ):

        print(
            "Booking contains invalid payment data."
        )

        return

    total_paid = (
        get_total_payments(
            booking[
                "booking_id"
            ]
        )
    )

    balance_due = (
        get_balance_due(
            booking
        )
    )

    print(
        "\n========== SUMMARY ==========\n"
    )

    print(
        f"Booking ID   : "
        f"{booking['booking_id']}"
    )

    print(
        f"Status       : "
        f"{booking.get('status', 'OPEN')}"
    )

    print(
        f"Rental Total : "
        f"₹{total_amount:.2f}"
    )

    print(
        f"Advance      : "
        f"₹{advance:.2f}"
    )

    print(
        f"Payments     : "
        f"₹{total_paid:.2f}"
    )

    print(
        f"Balance Due  : "
        f"₹{balance_due:.2f}"
    )

    print(
        f"Deposit      : "
        f"₹{deposit:.2f}"
    )

    
def record_payment():

    booking_id = input(
        "Booking ID: "
    ).strip()

    if booking_id == "":

        print(
            "Booking ID cannot be empty."
        )

        return

    booking = get_booking(
        booking_id
    )

    if not booking:

        print(
            "Booking not found."
        )

        return

    if (
        booking.get(
            "status",
            ""
        ).upper()
        ==
        "CLOSED"
    ):

        print(
            "Booking already closed."
        )

        return

    balance_due = (
        get_balance_due(
            booking
        )
    )

    print(
        f"\nBalance Due: "
        f"₹{balance_due:.2f}"
    )

    if balance_due <= 0:

        print(
            "No balance remaining."
        )

        return

    amount = get_money(
        "Payment Amount: "
    )

    if amount <= 0:

        print(
            "Payment must be greater than zero."
        )

        return

    if amount > balance_due:

        print(
            "Payment exceeds balance due."
        )

        return

    payments = load_data(
        PAYMENTS_FILE
    )

    payment = {

        "payment_id":
            generate_payment_id(
                payments
            ),

        "booking_id":
            booking[
                "booking_id"
            ],

        "amount":
            f"{amount:.2f}"
    }

    payments.append(
        payment
    )

    save_data(
        PAYMENTS_FILE,
        payments
    )

    remaining = (
        balance_due
        -
        amount
    )

    print(
        "\nPayment recorded successfully."
    )

    print(
        f"Remaining Balance: "
        f"₹{remaining:.2f}"
    )