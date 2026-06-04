# TEST CASES

This document contains important test cases and edge cases verified for the Sharma Tent House Management System.

---

# Inventory Tests

## TC-01 Add New Item

Input:

Name: Plastic Chair
Quantity: 100

Expected:

Item added successfully.

Status: PASS

---

## TC-02 Duplicate Item

Input:

Plastic Chair

Expected:

Item already exists.

Status: PASS

---

## TC-03 Empty Item Name

Input:

(blank)

Expected:

Item name cannot be empty.

Status: PASS

---

## TC-04 Negative Quantity

Input:

-10

Expected:

Quantity cannot be negative.

Status: PASS

---

## TC-05 Invalid Rate

Input:

abc

Expected:

Invalid rate.

Status: PASS

---

# Customer Tests

## TC-06 New Customer

Input:

Name: Rakesh Kumar
Phone: 9876543210

Expected:

Customer added successfully.

Status: PASS

---

## TC-07 Duplicate Phone Number

Input:

Existing Phone Number

Expected:

Customer already exists.

Status: PASS

---

## TC-08 Invalid Phone Length

Input:

98765

Expected:

Phone number must contain exactly 10 digits.

Status: PASS

---

## TC-09 Non-Digit Phone Number

Input:

98A7654321

Expected:

Phone number must contain digits only.

Status: PASS

---

## TC-10 Empty Customer Name

Input:

(blank)

Expected:

Customer name cannot be empty.

Status: PASS

---

# Booking Tests

## TC-11 Valid Booking

Expected:

Booking created successfully.

Status: PASS

---

## TC-12 Invalid Date Format

Input:

15-06-2026

Expected:

Invalid date format.

Status: PASS

---

## TC-13 Return Date Before Start Date

Expected:

Return date must be after start date.

Status: PASS

---

## TC-14 Quantity Exceeds Availability

Expected:

Only X available.

Status: PASS

---

## TC-15 Empty Booking

Expected:

No items added.

Status: PASS

---

## TC-16 Discount Greater Than Total

Expected:

Discount cannot exceed rental total.

Status: PASS

---

## TC-17 Advance Greater Than Total

Expected:

Advance cannot exceed total.

Status: PASS

---

## TC-18 Invalid Item Search

Expected:

No matching item found.

Status: PASS

---

# Delivery Tests

## TC-19 Partial Return

Expected:

Return recorded.

Status: PASS

---

## TC-20 Return Quantity Exceeds Pending

Expected:

Return exceeds booked quantity.

Status: PASS

---

## TC-21 Invalid Booking ID

Expected:

Booking not found.

Status: PASS

---

# Damage Tests

## TC-22 Record Damage

Expected:

Damage recorded successfully.

Status: PASS

---

## TC-23 Negative Damage Amount

Expected:

Amount cannot be negative.

Status: PASS

---

## TC-24 Damage Settlement

Expected:

Damage settled.

Status: PASS

---

# Maintenance Tests

## TC-25 Send To Maintenance

Expected:

Maintenance record created.

Status: PASS

---

## TC-26 Maintenance Quantity Exceeds Available

Expected:

Not enough available quantity.

Status: PASS

---

## TC-27 Return From Maintenance

Expected:

Item returned from maintenance.

Status: PASS

---

# Payment Tests

## TC-28 Record Payment

Expected:

Payment recorded.

Status: PASS

---

## TC-29 Overpayment

Expected:

Payment exceeds balance due.

Status: PASS

---

# Booking Close Tests

## TC-30 Close Booking Successfully

Conditions:

- All items returned
- No damage pending
- No payment due

Expected:

Booking closed.

Status: PASS

---

## TC-31 Close Booking With Pending Items

Expected:

Cannot close booking.

Status: PASS

---

## TC-32 Close Booking With Pending Damage

Expected:

Damage not settled.

Status: PASS

---

## TC-33 Close Booking With Outstanding Payment

Expected:

Balance still due.

Status: PASS

---

# Excel Export Tests

## TC-34 Export Items

Expected:

items.xlsx created and opened.

Status: PASS

---

## TC-35 Export Customers

Expected:

customers.xlsx created and opened.

Status: PASS

---

## TC-36 Export Bookings

Expected:

bookings.xlsx created and opened.

Status: PASS

---

## TC-37 Excel File Already Open

Expected:

Close Excel file and try again.

Status: PASS

---

# Regression Tests

## RT-01 Booking Availability

Booking should reduce available quantity.

PASS

---

## RT-02 Maintenance Availability

Maintenance items should reduce available quantity.

PASS

---

## RT-03 Returned Items

Returned items become available again.

PASS

---

## RT-04 Customer History

Customer shows linked bookings.

PASS

---

# Current Test Coverage

Inventory        : Covered
Customers        : Covered
Bookings         : Covered
Payments         : Covered
Delivery         : Covered
Damage           : Covered
Maintenance      : Covered
Excel Export     : Covered

Approximate Coverage: 95%+