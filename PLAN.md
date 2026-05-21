# PLAN.md Sharma-Tent-House

## Three-Sentence Specification

1. What program does?
   Program will track what items they own, bookings(active and past), delivery status, what customers owe, manage Payments and items that are damanged, under-maintenance, delivered, available , missing etc. All through CLI.
2. Who uses it ?
   Both Rakesh ji and Ankit use same system . As Ankit will handle daily data entry like bookings, returns,damages. Rakesh ji will use it to check item available, customer history, find missing items, check broken / damaged items etc.
3. What done means ?
   Done means Rakesh ji can answer his 6 questions - Availablility check,what items are delivered at which event, return dates, payments (how much they deposit and remaining balance), Monthly damaged items report, items-idle, history of particular event.
   Also the program will stop him from double-booking and close booking only when all items are returned.

## The Information Program must Remember

## (1) Items (That Sharmaji Tent House owns & rents out)

|    Field      |  Type  | Required |          Example              |
|---------------|--------|----------|-------------------------------|
|   item_id     | string |    Yes   | ITEM_001                      |
|     name      | string |    Yes   | "Folding Chair", "Gas Burner" |
| total_quantity|  int   |    Yes   | Total owned                   |
| rent_per_day  |  float |    Yes   | Price for one unit            |
| available_qty |  int   |    Yes   | Available items               |
| item_type     | string |    Yes   | Quantity / Unique / Limited   |
| description   | string |    No    |                               |

---

## (2) Customers

| Field           | Type   | Required |
|-----------------|--------|----------|
| cust_id         | string | Yes      |
| name            | string | Yes      |
| phone           | string | Yes      |
| address         | string | Yes      |
| alternate_phone | string | No       |
| email           | string | No       |

---

## (3) Booking

| Field          | Type   | Required |
|----------------|--------|----------|
| booking_id     | string | Required |
| cust_id        | string | Required |
| items          | list   | Required |
| total_price    | float  | Required |
| event_name     | string | Required |
| start_date     | date   | Required |
| return_date    | date   | Required |
| deposit_paid   | bool   | Required |
| balance_amount | float  | Required |
| delivery_date  | date   | Required |

---

## (4) Booked Items

| Field        | Type   | Required |
|--------------|--------|----------|
| item_id      | string | Required |
| name         | string | Required |
| qty_booked   | int    | Required |
| rate_per_day | float  | Required |
| booking_id   | string | Required |

---

## (5) Return Record

| Field         | Type   | Required |
|---------------|--------|----------|
| return_id     | string | Required |
| booking_id    | string | Required |
| return_date   | date   | Required |
| extra_days    | int    | Required |
| extra_charges | float  | Required |
| damage_items  | list   | Optional |
| returned -qty | int    | Required |

---

## (6) Payments

| Field        | Type   | Required |
|--------------|--------|----------|
| payment_id   | string | Required |
| booking_id   | string | Required |
| payment_date | date   | Required |
| total_amount | float  | Required |
| type         | string | Required |(deposit / balance / extra charges)

---

## (7) Delivery Record

| Field           | Type   | Required |
|-----------------|--------|----------|
| delivery_id     | string | Required |
| booking_id      | string | Required |
| delivery_date   | date   | Required |
| delivery_status | string | Optional |

---

## (8) Damage

| Field        | Type   | Required |
|--------------|--------|----------|
| damage_id    | string | Required |
| booking_id   | string | Required |
| item_id      | string | Required |
| item_name    | string | Required |
| damage_qty   | int    | Required |
| extra_charge | float  | Required |
| event_name   |string  | Optional |

---

## (9) Maintenance Record

| Field         | Type   | Required |
|---------------|--------|----------|
| maintenance_id| string | Required |
| item_id       | string | Required |
| item_name     | string | Required |
| item_type     | string | Required |
| quantity      | int    | Required |
| cost          | float  | Required |
| date          | date   | Required |

---

## Relationships (Groupings connected to each other)

- **Booking <-> Customers:** One customer can have multiple bookings; there are many bookings from different customers. To track them, we have to use cust_id & booking_id.
- **Items -> Booked Items:** To track availability.
- **Payments -> Booking:** For tracking payments (deposit / balance / extra charges) for all bookings.
- **Damage -> Booking:** How many damages to booking & there per booking & for that damage, how much we have to charge.
- **Return -> Booking:** When booked items of any booking are returned.
- **Delivery -> Booking:** For any particular booking, when delivery happens.

---

## 3. How Your Groupings Connect to Each Other

**Customers -> Bookings:** One customer can have many bookings over the years. `cust_id` on the booking links back to the customer. When Rakesh ji looks up a customer by phone number, the program pulls all their bookings and shows a history - total spent, number of events, any outstanding balance.

**Items -> Booked Items:** Every booking carries a list of items with quantities. The availability check for any date works by scanning all active bookings, finding every booking whose date range overlaps the requested dates, summing up committed quantities per item, and subtracting from total stock. This is the central logic of the whole program.

**Items -> Maintenance Records:** Any item with an unresolved maintenance record has fewer units available. The availability calculation must subtract maintenance qty just like it subtracts booked qty.

**Bookings -> Payments:** A booking can have multiple payment records over its lifetime — deposit first, then balance, then possibly extra charges for damage or late return, and finally a refund if deposit exceeded charges. Summing all payments for a booking gives the net amount paid.

**Bookings -> Return Records:** As items come back from an event, return records are logged against the booking. The booking status updates from `delivered` ->  `closed` based on how many items are still outstanding. A booking cannot be closed until all `qty_returned` values match `qty_booked`.

**Return Records -> Damage Records:** When a return is logged, damaged items are recorded separately in damage records, linked to both the return and the booking. This is how Rakesh ji can later ask "how much did I lose to damages last month" and get a real number.

**Bookings -> Delivery:** Delivery date is stored on the booking itself (not a separate record) because Rakesh ji doesn't need delivery tracking beyond "when did it go out." If a more complex delivery log is needed later, it can be added.

---
### What breaks at 5,000 bookings a year?

Loading all of `bookings.json` into memory to check availability on a single date means reading thousands of records every time. Right now this is fine - Python can scan 2,000 bookings in milliseconds. But at 5,000+ bookings the file itself starts becoming large, reads slow down, and saving the whole file on every write becomes risky (if the program crashes mid-write, the file can corrupt). The right move at that scale is to shift to any database.

---

## 4. File Structure

---

### `items.json`
```json
[
  {
    "item_id": "ITEM_001",
    "name": "Folding Chair",
    "item_type": "bulk",
    "total_qty": 500,
    "rate_per_day": 15.0,
    "description": "Standard white folding chairs, stacked in warehouse block B"
  },
  {
    "item_id": "ITEM_002",
    "name": "Gas Burner (6-ring Commercial)",
    "item_type": "limited",
    "total_qty": 6,
    "rate_per_day": 250.0,
    "description": "High pressure commercial burners for halwai use"
  },
  {
    "item_id": "ITEM_003",
    "name": "LED Video Wall (Imported)",
    "item_type": "unique",
    "total_qty": 2,
    "rate_per_day": 3500.0,
    "description": "Bought in 2020, requires technician for setup - contact Suresh bhaiya"
  }
]
```

---

### `customers.json`
```json
[
  {
    "cust_id": "CUST_001",
    "name": "Ramesh Agarwal",
    "phone": "9414501234",
    "address": "Vigyan Nagar, Kota",
    "alt_phone": "9414509876",
    "email": ""
  },
]
```

---

### `bookings.json`
```json
[
  {
    "booking_id": "BK_001",
    "cust_id": "CUST_001",
    "event_name": "Agarwal Wedding",
    "event_address": "Plot 14, Indraprastha Colony, Kota",
    "start_date": "2024-12-18",
    "end_date": "2024-12-20",
    "delivery_date": "2024-12-17",
    "items": [
      {
        "item_id": "ITEM_001",
        "item_name": "Folding Chair",
        "qty_booked": 200,
        "qty_returned": 200,
        "rate_per_day": 13.0,
      },
      {
        "item_id": "ITEM_005",
        "item_name": "Antique Sofa Set (Stage)",
        "qty_booked": 1,
        "qty_returned": 1,
        "rate_per_day": 1200.0,
      }
    ],
    "total_price": 15000.0,
    "deposit_paid": 5000.0,
    "balance_due": 0.0,
  }
]
```

---

### `payments.json`
```json
[
  {
    "payment_id": "PAY_001",
    "booking_id": "BK_001",
    "date": "2024-11-30",
    "amount": 5000.0,
    "type": "deposit",
    "notes": "Cash received at shop"
  }
]
```

---

### `returns.json`
```json
[
  {
    "return_id": "RET_001",
    "booking_id": "BK_001",
    "return_date": "2024-12-21",
    "items_returned": [
      { "item_id": "ITEM_001", "qty_returned": 200 },
      { "item_id": "ITEM_003", "qty_returned": 3 },
      { "item_id": "ITEM_005", "qty_returned": 1 }
    ],
    "extra_days": 1,
    "late_charge": 250.0
  }
]
```

---

### `damages.json`
```json
[
  {
    "damage_id": "DAM_001",
    "booking_id": "BK_001",
    "item_id": "ITEM_003",
    "item_name": "Gas Burner (6-ring Commercial)",
    "qty_damaged": 1,
    "damage_type": "broken",
    "charge": 800.0
  }
]
```

---

### `maintenance.json`
```json
[
  {
    "maintenance_id": "MNT_001",
    "item_id": "ITEM_004",
    "item_name": "LED Video Wall (Imported)",
    "date": "2024-12-10",
    "qty": 1,
    "cost": 4500.0,
    "resolved": false
  }
]
```

---
## 5. Operations


1.   Rakesh ji Asks: "Are 250 chairs and 4 gas burners free on Dec 18–20?" System scans all bookings with status `active` / `delivered`  whose date range overlaps Dec 18–20. Sums committed qty per item. Subtracts from total stock. Also subtracts unresolved maintenance qty.System shows "Folding Chair: 500 total, 200 committed → **300 available. ✓**" / "Gas Burner: 6 total, 4 committed → **2 available. ✗ You need 4.**"

2.  Rakesh ji Creates a new booking. System prompts for customer (by phone or ID), event name, address, dates, then adds items one by one. Checks availability for each item as it's added. Calculates total price (qty × rate × days). Asks for deposit amount. Generates `booking_id`. Saves to `bookings.json`. System shows Summary of booking: all items, total price, deposit collected, balance due. 

3. If Rakesh ji Adds more items to an existing booking, System selects booking by ID. Adds new items. Checks availability for new items against the booking's dates. If available, appends to booking's item list and recalculates total. System shows Updated booking summary. If not available: "Only 1 Gas Burner free on those dates. Cannot add 2."

4. If Rakesh ji Records delivery of a booking, System selects booking. Marks `delivery_date` as today (or a specified date). Changes status from `active` -> `delivered`.System shows "Booking BK_001 marked as delivered on 17-Dec-2024." 

5. If Rakesh ji Records a return (full or partial) then System should prompts for booking ID, then for each item: how many came back today. Updates `qty_returned` on each Booking items in the booking. If all items fully returned, prompts for damage check before closing. If partial, sets status to `partially_returned`. List of what came back, what is still remaining: "Still pending: 1× Gas Burner." 

6. Closes a booking ,System should selects booking. System checks that all `qty_returned` == `qty_booked` for every boooked item. If yes, calculates final settlement: total paid - total charged - damage charges = refund or extra due. Marks status `closed`. System shows settlement summary: total billed, total paid, damage charges, late charges, final refund .

7. Cancels a booking System should selects booking. System checks status - if `delivered` , warns that items are already out. If `active`, marks as `cancelled`. Calculates refund based on deposit minus any cancellation charge. System shows "Booking cancelled. Refund due: ₹3,000 (deposit ₹5,000 minus cancellation fee ₹2,000)."

8. If Rakesh ji looks up a customer by phone , SYsrtem should Enters phone number. System searches `customers.json` for match. System shows Customer name, address, notes, and a summary: total bookings, total spent, any open balance. (All matching Results)

9. If Rakesh ji views full customer history System should first selects customer. System pulls all bookings for that customer. System shows table of all bookings: booking ID, event name, date, total price, amount paid.

10. If Rakesh ji checks late returns System should show All bookings where `end_date` has passed and status is not `closed` or `cancelled`. Shows how many days overdue and the late charges per day.

11.  If Rakesh ji records a payment(to check balance) System should first selects booking. Calculates `balance_due` on booking. System shows "Payment of ₹5,000 recorded. Balance due: ₹8,000."

12. If Rakesh ji want to adds a new customer System should Enters name, phone, address, and optional fields. System checks if phone already exists (duplicate guard). Generates `cust_id`. System shows "Customer CUST_003 - Monu Gupta - added."

13. If Rakesh ji wants to view idle items. System checks all items. For each, checks if it appears in any booking in the last 30 days. System shows items with zero or low bookings in the last month: "Antique Sofa Set - booked 1 time in last 30 days (3 days out of 30)." 

14. Views damage report for a month System prompts for enter month and year. System scans `damages.json` for that period. System shows total damages by item: item name, qty damaged, total charge. Grand total loss.

15. Adds new items to inventory System should prompt for enter item name, type, qty, rate, description. System generates `item_id`. Saves. And System shows "ITEM_006 - Pedestal Fan - added. Qty: 10." 

16. If Rakesh ji wants to check booking's full detail System prompts for Enter booking ID. ans System should show Everything: customer info, event details, all booked items with qty booked / returned, all payments, all damage records, current status, balance due. 

17. If Rakesh ji wants to check missing items from particular booking System should prompts for enter booking id and calculates delivered items - returned items and System should shows missing items.

18.  Updates an item's rate or details system should selects item by name or ID. Edits fields. And System should shows "Item updated. New rate: ₹18/day." (Should not effect active bookings).

19. If Rakesh ji wants to check total amount of any booking , System should ask first for `booking_id` and shows total amount by calculating total booked items * total days * rent per item.

20. If Rakesh ji selects "Exit" System should save all data to JSON. and make exit from program.

---

## 6. Things That Can Go Wrong

1. JSON files don't exist on first run. Program checks for each file at startup. If missing, creates it as an empty list `[]` and continues. No crash. First run is treated as a fresh shop setup.

2. Rakesh ji tries to book 250 chairs when only 220 are free on that date. Program rejects the booking and shows exactly what is available: "Only 220 Chairs free on Dec 18–20. Requested: 250. Booking not created."

3. Customer books an item for Dec 19, but another booking returns those items on Dec 19 at Morning. Program does not count same-day returns as available for same-day new bookings. The returning items are still committed until the return is physically logged. Simply prevents Rakesh ji from promising items that aren't confirmed back yet but it's a loss.

4. If Ankit / Rakeshji forgot to record missing items & made delivery as "returned" -> Business loss.

5. If multiple events ended same week & multiple items returned but some are broken - maybe Rakeshji forgets which event caused the damage. Business loss. -> Incorrect bill.

6. Customer cancels booking 3 days before event - Rakeshji already told his team to prepare delivery, & refused another booking for their chairs -> Lost revenue. Program should have a cancellation policy.

7. Rakeshji tries to close a booking but some items have not been returned. Program refuses: "Cannot close B_id - still remaining: 4× Gas Burner, 1× Imported Sofa." 

8. Customer wants to add 50 more chairs. Rakeshji edits the booking - program checks availability - only 25 more are available and others are committed. Can't add 50. Rakesh ji then decides to add 25 only or reject.

9. Damage exceeds the deposit / program calculates this in the settlement 3 chances: Deposit = Rs 3000, damage = 5000 -> customer should pay 2000 extra - alert Rakeshji for this.

10. Rakeshji tries to delete an item that has active bookings. Program refuses - "Can't delete, close / cancel bookings first."

11. Customer returns half items before return date & half remain - but program just checks here returns; it can't show availability or partial returns -> Loss.

12. A postponed event wants to shift its booking dates by two weeks. Program checks availability for the new dates for every item in the booking. If all are free, updates the dates. If any item is not free on the new dates, it tells Rakesh ji exactly which one is the conflict. Does not update unless all items clear.

---

## 7. One Thing I Don't Know Yet

There's actually not only one thing but here are few things that i don't know yet:

- How to handle partial returns - (the program keeps booking open until all items are returned).

- Rakeshji -> not a fast typist -> how to make CLI easy? (menu system?) -> Yes, what about sub-menus?

- Story says close at night, open in morning -> how to implement this? -> Date comparison logic needed - need experimentation.

- How to automatically update inventory quantities automatically after deliveries & returns, and changes without inconsistency?

- I am also unsure if storing all files in separate JSON files will remain efficient or not if the number of bookings increases during wedding periods.

- Unsure how to check availability when delivery date & return date overlaps between multiple bookings.
