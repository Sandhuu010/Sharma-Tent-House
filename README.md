# Sharma Tent House Management System

A Python-based inventory and booking management system developed for tent house businesses to manage items, customers, bookings, deliveries, returns, payments, damages, and maintenance records.

---

# Features

## Inventory Management

- Add Item
- View Items
- Search Item by Name
- Search Item by Category
- Update Item
- Delete Item
- Duplicate Item Prevention

---

## Customer Management

- Add Customer
- Search Customer by Name
- Search Customer by Phone Number
- Customer Booking History
- Duplicate Customer Detection

---

## Booking Management

- Check Availability
- Create Booking
- Multi-Item Booking
- Customer Linking
- Occasion Tracking
- Discount Support
- Advance Payment Tracking
- Security Deposit Tracking
- Booking Summary

---

## Delivery & Returns

- Mark Delivery
- Record Partial Return
- Record Full Return
- Track Pending Items
- Close Booking

---

## Payment Management

- Record Payment
- Advance Payments
- Balance Due Calculation
- Booking Financial Summary

---

## Damage Management

- Record Damage
- Damage Summary
- Damage Settlement
- View Damage Records

---

## Maintenance Management

- Send Item To Maintenance
- Return Item From Maintenance
- Maintenance Records
- Currently Out Items Report

---

## Excel Reports

System exports reports directly to Excel:

- Items Report
- Customer Report
- Booking Report
- Damage Report
- Maintenance Report
- Items Currently Out Report

---

# Project Structure

```
Sharma-Tent-House/
│
├── main.py
├── storage.py
├── items.py
├── customers.py
├── bookings.py
├── payments.py
├── delivery.py
├── damage.py
├── maintenance.py
├── export_utils.py
│
├── data/
│   ├── items.json
│   ├── customers.json
│   ├── bookings.json
│   ├── damages.json
│   └── maintenance.json
│
└── reports/
```

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

---

## Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install openpyxl
```

---

# Run Application

```bash
python main.py
```

---

# Booking Workflow

1. Create/Select Customer
2. Enter Booking Dates
3. Enter Occasion
4. Search Items
5. Add Quantities
6. Apply Discount
7. Receive Advance
8. Receive Deposit
9. Generate Booking

---

# Technologies Used

- Python
- JSON Storage
- OpenPyXL
- Decimal Module

---

# Future Improvements

- Invoice Generation
- PDF Receipts
- WhatsApp Integration
- SMS Notifications
- Cloud Database
- Multi-User Login
- Dashboard Analytics

---

# Developed For

Sharma Tent House

Inventory & Event Rental Management Solution