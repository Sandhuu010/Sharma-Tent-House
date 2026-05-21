# PLAN.md — Sharma Tent House CLI System
---

## 1. Three-Sentence Specification

1. What program does?
   Program Track items what they own, bookings (active), delivery, what customers owe, manage payments, items (damaged, under maintenance), delivered, available etc. all through CLI.

2. Who use it ? 
  Both Rakesh ji and Ankit use it - Rakesh ji makes decisions (pricing, discounts, refunds, cancellations) while Ankit handles day-to-day data entry (logging deliveries, recording returns, adding customers).

3. What done means ?
  Done means Rakesh ji can answer his 6 questions - availability check, what items are delivered and at which event, return dates, payment balances, monthly damaged items report, which items are idle, history of a particular event. Also the program will stop him from double booking and close booking only when all items are returned.

---
## 2. The Information Your Program Must Remember

### (1) Items (That Sharmaji Tent House owns & rents out)

| Field          | Type   | Required | Example                       |
|----------------|--------|----------|-------------------------------|
| item_id        | string | Yes      | ITEM_001                      |
| name           | string | Yes      | "Folding Chair", "Gas Burner" |
| total_quantity | int    | Yes      | Total owned                   |
| rate_per_day   | float  | Yes      | Price for one unit            |
| available_qty  | int    | Yes      | Available items               |
| item_type      | string | Yes      | Quantity / Unique / Limited   |

---

## (2) Customers

| Field           | Type   | Required |
|-----------------|--------|----------|
| cust_id         | string | Required |
| name            | string | Required |
| phone           | string | Required |
| address         | string | Required |
| alternate_phone | string | Optional |
| email           | string | Optional |

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
| delivery_date  | date   | Optional |

---

## (4) Booked Items

| Field        | Type   | Required |
|--------------|--------|----------|
| item_id      | string | Required |
| quantity     | int    | Required |
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

---

## (6) Payments

| Field        | Type   | Required |
|--------------|--------|----------|
| payment_id   | string | Required |
| booking_id   | string | Required |
| payment_date | date   | Required |
| total_amount | float  | Required |
| type         | string | Required |(deposit / balance / extra charges) |

---

## (7) Delivery Record

| Field           | Type   | Required |
|-----------------|--------|----------|
| Delivery_id     | string | Required |
| Booking_id      | string | Required |
| delivery_date   | date   | Required |
| delivery_status | string | Optional |

---

## (8) Damage

| Field        | Type   | Required |
|--------------|--------|----------|
| damage_id    | string | Required |
| booking_id   | string | Required |
| item_id      | string | Required |
| qty          | int    | Required |
| extra_charge | float  | Optional |

---

## (9) Maintenance Record

| Field     | Type   | Required |
|-----------|--------|----------|
| item_id   | string | Required |
| item_type | string | Required |
| name      | string | Required |
| qty       | int    | Required |
|  amount   | float  | Required |


---

## Relationships Summary

- **Booking <-> Customers:** One customer can have many bookings over the years. `cust_id` on the booking links back to the customer. When Rakesh ji looks up a customer by phone number, the program pulls all their bookings and shows a history - total spent, number of events, any remaining balance.
- **Items -> Booked Items:** Every booking carries a list of items with quantities. The availability check for any date works by scanning all active bookings, finding every booking whose date range overlaps the requested dates, summing up committed quantities per item, and subtracting from total stock. This is the central logic of the whole program.
- **Payments -> Booking:** For tracking payments (deposit / balance / extra charges) for all bookings.
- **Damage -> Booking:** How many damages to booking & there per booking & for that damage, how much we have to charge.
- **Return -> Booking:** When booked items of any booking are returned.
- **Delivery -> Booking:** For any particular booking, when delivery happens.

---
## (4) File Structure – JSON

### customers.json

```json
[
  {
    "cust_id": "C01",
    "Name": "Monu",
    "phone-no": "9142-...",
    "address": "Kathua, J&K",
    "Alt-ph": "9142 9-...",
    "E-mail": "monu@gmail.com"
  }
]
```
*(for all)*

---

### What breaks at 5,000 bookings a year?

Loading all of `bookings.json` into memory to check availability on a single date means reading thousands of records every time. Right now this is fine — Python can scan 2,000 bookings in milliseconds. But at 5,000+ bookings the file itself starts becoming large, reads slow down, and saving the whole file on every write becomes risky (if the program crashes mid-write, the file can corrupt). The right move at that scale is to shift to some DB.


## (5) Operations

1. **If Rakeshji checks availability of item** -> system checks at some date all bookings where delivery date & return date overlaps the days, sums up committed qty & subtracts from total qty - and shows available.

2. **If Rakeshji updates item details like price** -> system should update price & show updated details.

3. **If Rakeshji wants to close a booking** -> system checks whether all items are returned; if not, refuses ("can't close").

4. **Rakeshji wants to check total amount** -> system checks items booked, rate per day, multiplies & shows actual amount.

5. **If Rj wants to check booking** -> system loads booking + customer + payment history.

6. **If user adds more items to existing booking** -> system checks availability first, then adds; updates booking & rejects if not available.

7. **If Rakeshji wants to restock / check missing items** -> system should check total items delivered - returned items = missing items.

8. **If Rakeshji wants to check balance** -> system should show: total amount - deposit = balance.

9. **If Rj wants to refund to any customer** -> system checks item price & total items and shows refunded price.

10. **If Rj wants to check delivery date of items** -> system checks booking, delivery date & shows it to user.

11. **If user wants to add items into inventory** -> system should update it & show results.

12. **If Rj wants to check late return charges** -> system should check extra days from expected return date × extra charges = late return charges.

13. **If Rakeshji searches customer by phone number** -> system matches the details with customer details & shows result.

14. **If Rakeshji wants to add any customer** -> system should save details, generate new cust_id.

15. **If Rakeshji does a booking** -> system should check items before booking, check whether available or not, then generates booking_id.

16. **If Rakeshji records a partial return** -> system marks pending items -> shows remaining items.

17. **If Rakeshji views monthly damage report** -> system totals damage charges & displays losses.

18. **If Rj views customer history** -> system prompts for cust_no / ID -> shows all past bookings, total spent, days.

19. **View idle items** -> system compares total qty with any booking in last 30 days -> system shows items with low usage.

20. **If Rakeshji selects "Exit"** -> system saves all data to JSON -> exits.

---
## (6) Edge Cases (This Can Go Wrong!)

1. JSON file doesn't exist on first run.

2. If customer adds 850 / 600 chairs, maybe our system has 500/200 chairs, but program shows not available / rejects booking (loss).

3. If customer books an item on 19 Dec - at evening, but system says there are no available items (in a case if items are returned at 19-Dec at morning) - system doesn't show that items are available at evening; it simply rejects bookings. (Loss - for business.)

4. If Ankit / Rakeshji forgot to record missing items & made delivery as "returned" -> Business loss.

5. If multiple events ended same week & multiple items returned but some are broken - maybe Rakeshji forgets which event caused the damage. Business loss. -> Incorrect bill.

6. Customer cancels booking 3 days before event - Rakeshji already told his team to prepare delivery, & refused another booking for their chairs -> Lost revenue. Program should have a cancellation policy.

7. Rakeshji tries to close a booking but some items have not been returned. Program refuses: "Cannot close B_id - still remaining: 4× Gas Burner, 1× Imported Sofa." 

8. Customer wants to add 50 more chairs. Rakeshji edits the booking - program checks availability - only 25 more are available and others are committed. Can't add 50. Rj then decides to add 25 only. or rejects it.

9. Damage exceeds the deposit / program calculates this in the settlement 3 chances: Deposit = Rs 3000, damage = 5000 -> customer should pay 2000 extra - alert Rakeshji for this.

10. Rakeshji tries to delete an item that has active bookings. Program refuses - "Can't delete, close / cancel bookings first."

11. Customer returns half items before return date & half remain - but program just checks here returns; it can't show availability or partial returns -> Loss.

12. If a postponed event wants to change date of booking -> system should check re-availability.

---

## Open Questions / Unsolved Problems


- How to automatically update inventory quantities automatically after deliveries & returns, and changes without inconsistency?

- I am also unsure if storing all files in separate JSON files will remain efficient or not if the number of bookings increases during weekly periods.

- Unsure how to check availability when delivery date & return date overlaps between multiple bookings.

- If with customer Rakesh ji has to handles different prices -> how? I don't know yet.

- How to handle partial returns - (the program keeps booking open until all items are returned).

- Rakeshji - not a fast typist - how to make CLI easy? (menu system?) - Yes, what about sub-menus?

- Story says close at night, open in morning -> how to implement this? -> Date comparison logic needed - need experimentation.
