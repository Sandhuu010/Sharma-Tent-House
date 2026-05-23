# PLAN.md — Sharma Tent House CLI System
---

## 1. Three-Sentence Specification

Sharma Tent House rents out physical items - chairs, gas burners, sofas - and needs a CLI program to track what they own, what is committed to upcoming events, and what customers owe at any point in time. Rakesh ji makes all business decisions (pricing, discounts, cancellations, refunds) while Ankit handles day-to-day data entry (logging deliveries, recording returns, adding customers). The program is done when Rakesh ji can check item availability for any date range without double-booking, track every rupee across a booking's full money lifecycle, and close a booking only after all items are accounted for.

---
## 2. The Information Your Program Must Remember

### Section A - Items (That Sharmaji Tent House owns & rents out)

| Field          | Type   | Required | Example                       |
|----------------|--------|----------|-------------------------------|
| item_id        | string | Yes      | ITEM_001                      |
| name           | string | Yes      | "Folding Chair", "Gas Burner" |
| total_quantity | int    | Yes      | Total owned                   |
| rate_per_day   | decimal| Yes      | Price for one unit            |
| item_type      | string | Yes      | Quantity / Unique / Limited   |

**Availability query (derived, not stored):**
 ```
 available_qty(item, date_range) =
     total_qty
     - SUM( booked_qty - returned_qty  FOR EACH booking that overlaps date_range )
     - SUM( qty_under_repair           FOR EACH ongoing maintenance record for this item )
 ```
 --- 

### Section B - Customers

| Field           | Type   | Required |
|-----------------|--------|----------|
| cust_id         | string | Required |
| name            | string | Required |
| phone           | string | Required |
| address         | string | Required |
| alternate_phone | string | Optional |
| email           | string | Optional |

---

### Section C - Bookings

| Field              | Type   | Required | Notes                                                 |
|--------------------|--------|----------|-------------------------------------------------------|
| booking_id         | string | Required |                                                       |
| cust_id            | string | Required |                                                       |
| event_name         | string | Required |                                                       |
| start_date         | date   | Required |                                                       |
| return_datetime    |datetime| Required | Date + time; needed for same-day overlap resolutionn  |
| delivery_date      | date   | Optional |                                                       |
| total_rental_amount| float  | Required | Sum of all booked item charges                        |
| advance_paid       | float  | Required | Amount paid at booking time                           |
| deposit_amount     | float  | Required | Refundable security; held separately from advance     |
| deposit_returned   | float  | Required | How much of the deposit was actually returned         |
| status             | string | Required | active / delivered / closed / cancelled               |

> **`balance_due` is not stored.** Keeping a stored copy alongside a computed formula creates two sources of truth. Computing it on demand from the Payments table always reflects the real state.

---

### Section D - Booked Items

| Field        | Type   | Required |
|--------------|--------|----------|
| item_id      | string | Required |
| quantity     | int    | Required |
| rate_per_day | decimal| Required |
| booking_id   | string | Required |

 > **Why no `item_name` here?** .Name is looked up from the Items table at display time using `item_id`. Only the rate snapshot stays here.

---

### Section E - Return Records

| Field            | Type     | Required |      Notes                                         |
|------------------|----------|----------|----------------------------------------------------|
| return_id        | string   | Required |                                                    |
| booking_id       | string   | Required |                                                    |
| return_datetime  | datetime | Required | Date + time, not date only                         |
| items_returned   | list     | Required | List of {item_id, qty} actually returned this time |
| extra_days       | int      | Required | Days past expected return_datetime                 |
| extra_charges    | float    | Required | extra_days × per-day rate for each item            |

> A booking may have **multiple return records** (partial returns). The booking stays open until the sum of all `items_returned` across all return records equals the original booked quantities.
---

### Section F - Payments

| Field        | Type   | Required |
|--------------|--------|----------|
| payment_id   | string | Required |
| booking_id   | string | Required |
| payment_date | date   | Required |
| total_amount | float  | Required |
| type         | string | Required |advance / balance / extra_charges / damage / deposit_refund / deposit_extra |
| direction    | string | Required | in (customer pays us) / out (we refund customer)                           |

---

### Section G - Delivery Records

| Field           | Type   | Required |
|-----------------|--------|----------|
| Delivery_id     | string | Required |
| Booking_id      | string | Required |
| delivery_date   | date   | Required |
| delivery_status | string | Optional | pending / dispatched / delivered |

---

### Section H - Damage Records

| Field        | Type   | Required |
|--------------|--------|----------|
| damage_id    | string | Required |
| booking_id   | string | Required |
| return_id    | string | Required | Links to the return event where damage was found |
| item_id      | string | Required |
| qty          | int    | Required |
| damage_type  | string | Required | `broken` / `missing` / `unusable` |
| extra_charge | float  | Optional |

---

### Section I - Maintenance Records

One row represents **one maintenance event** for a specific item — when it started, its current status, and when it was resolved. 

| Field            | Type   | Required | Notes                                      |
|------------------|--------|----------|--------------------------------------------|
| maintenance_id   | string | Required | Unique per event                           |
| qty_under_repair | int    | Required | Units sent for this repair event           |
| start_date       | date   | Required | When item was sent for repair              |
| end_date         | date   | Optional | When item came back; null if still ongoing |
| status           | string | Required | ongoing / resolved                         |
| cost             | float  | Required | Repair cost for this event                 |

> Units under ongoing maintenance (`status = ongoing`) must be subtracted from `total_qty` when computing availability, alongside committed booking quantities.

---

## 3. Relationships Summary

- **Booking -> Customers:** One customer can have many bookings. `cust_id` on the booking links back. When Rakesh ji looks up a customer by phone, the program pulls all their bookings - total spent, number of events, remaining balance.
- **Booking -> Booked Items:** Section D is the only source of item-level detail per booking. Availability for a date range is computed by scanning Section D across all active bookings whose windows overlap.
- **Booking -> Payments (Section F):** Every money event in the full lifecycle - advance, balance, damage charges, deposit settlement - is a row here.
- **Booking -> Damage (Section H):** Damage facts live here only; Return Records do not duplicate them.
- **Booking -> Return Records (Section E):** Multiple partial-return records per booking are allowed. Booking closes only when all quantities are accounted for.
- **Booking -> Delivery (Section G):** One delivery record per booking.
- **Items -> Maintenance (Section I):** Ongoing maintenance reduces effective available quantity at query time.

---
## 4. File Structure – JSON

Each entity gets its own JSON file. All files are arrays of objects.

```
customers.json
items.json
bookings.json
booked_items.json
return_records.json
payments.json
delivery_records.json
damage_records.json
maintenance_records.json
```

### customers.json (example)

```json
[
  {
    "cust_id": "C001",
    "name": "Monu",
    "phone": "91420XXXXX",
    "address": "Kathua, J&K",
    "alternate_phone": "91429XXXXX",
    "email": "monu@gmail.com"
  }
]
```
### What breaks at 5,000 bookings a year?

>  JSON files loaded fully into memory are fine up to roughly 2,000–3,000 bookings. At 5,000+ bookings per year, full-file reads on every availability check slow down, and a crash mid-write can corrupt the file. The right move at that scale is SQLite or a similar embedded database — the schema above maps directly to relational tables.
---

## 5. Operations

1. **Availability check** -> scan Booked Items for all bookings whose `delivery_date`-`return_datetime` overlaps the requested range; also subtract units under ongoing maintenance; subtract from `total_qty`; show result.

2. **Update item price** -> update `rate_per_day` on Items; show updated record. Note: existing bookings retain the rate snapshot in Booked Items (Section D) - they are not changed.

3. **Close a booking** -> verify sum of returned quantities across all Return Records equals original booked quantities; if not, refuse: *"Cannot close B_001 - still out: 4× Gas Burner, 1× Imported Sofa."* Also verify balance_due = 0 and deposit is settled.

4. **Calculate total rental amount** -> sum across Booked Items: `quantity × rate_per_day × number_of_days`; store on Booking as `total_rental_amount`.

5. **View booking** -> load Booking + Customer + all Booked Items + Payment history; display full picture.

6. **Add items to existing booking** -> check availability for the booking's date range first; add only what is available; update Booked Items and recalculate `total_rental_amount`; reject or partially fulfil if stock is short.

7. **Check missing items** -> `total delivered - total returned` per item per booking; flag for this.

8. **Check balance due** -> `balance_due = total_rental_amount - SUM(payments where type IN (advance, balance))`. Deposit is tracked and settled separately - it is not subtracted from the rental bill.

9. **Process refund** -> calculate refund amount; create a Payment row with `direction = out`, `type = deposit_refund`; update `deposit_returned` on Booking.

10. **Check delivery date** -> read delivery_date from Delivery Records for the booking.

11. **Add item to inventory** -> create or update Items row; `total_qty` increases; show result.

12. **Late return charges** -> `extra_days = days past return_datetime × per-day rate per item`; create Payment row with `type = extra_charges`.

13. **Search customer by phone** -> match phone in Customers; show customer details and booking history.

14. **Add customer** -> save details; generate new `cust_id`; confirm.

15. **Create booking** -> check availability for requested date range (including maintenance units); if available, create Booking row + Booked Items rows + generate `booking_id`; reduce effective available stock in future queries automatically.

16. **Record partial return** -> create a Return Record with the items returned so far; show remaining unreturned items; keep booking open.

17. **Monthly damage report** -> sum `extra_charge` across Damage Records for the month; group by item; display losses.

18. **Customer history** -> look up by phone or cust_id; show all past bookings, total spent, total days, any open balance.

19. **View idle items** -> items with no active booking in the last 30 days; compare `total_qty` against committed quantities in that window.

20. **Exit** -> save all in-memory changes to JSON files; exit.

---

## 6. Edge Cases

1. **JSON file missing on first run** -> program creates empty files with valid `[]` structure; does not crash.

2. **Customer requests more than stock** -> availability check rejects or offers the maximum available: *"Only 200 chairs available on those dates; you requested 850."* Rakesh ji decides whether to proceed with 200 or decline.

3. **Morning return, evening booking on the same day** -> Return Records store `return_datetime` (date + time). Booking's `delivery_date` is a date; if needed, delivery time can be added as `delivery_datetime`. The overlap check compares datetimes, not dates. Items returned at 10 AM are available for a booking starting at 6 PM on the same day. This requires Ankit to record actual return time, not just date.

4. **Delivery marked as returned without recording missing items** -> programme shows discrepancy: `delivered qty - returned qty = missing qty` per item. Closing the booking is blocked until this is resolved.

5. **Multiple events ending the same week; damage attribution unclear** -> every Damage Record is linked to a `booking_id`. When Ankit logs damage at return time, the booking_id is already in context - he cannot log damage without it. This forces attribution at the moment of return.

6. **Cancellation policy** -> cancellation creates a Payment row (`direction = out, type = deposit_refund`) according to the policy (e.g., full refund if cancelled 7+ days out, 50% within 3–6 days, no refund within 2 days). Programme enforces the policy and shows the refund amount before confirming cancellation.

7. **Closing a booking with unreturned items** -> refused: *"Cannot close B_001 - still out: 4× Gas Burner."* Programme lists exactly what is missing.

8. **Customer wants to add 50 chairs; only 25 available** -> programme responds: *"Only 25 chairs available on those dates. Add 25 instead, or cancel the request."* Rakesh ji chooses.

9. **Damage charges exceed deposit** -> `deposit_amount − (damage + missing item charges) < 0` → alert: *"Deposit of ₹3,000 is short by ₹2,000. Customer owes an additional ₹2,000."* Create a Payment row with `type = deposit_extra, direction = in`.

10. **Deleting an item with active bookings** -> refused: *"Cannot delete ITEM_001 - active bookings exist. Close or cancel bookings first."*

11. **Partial returns** -> Return Records support multiple rows per booking (Section E). Programme sums returned quantities across all rows and shows remaining items. Availability for other bookings updates correctly because availability is always derived from Booked Items minus returned quantities.

12. **Postponed event / date change** -> programme re-runs availability check for the new date range before allowing the change. If a conflict exists, it reports which bookings clash.

---

## 7. Open Questions / Unsolved Problems


- How to automatically update inventory quantities automatically after deliveries & returns, and changes without inconsistency?

- I am also unsure if storing all files in separate JSON files will remain efficient or not if the number of bookings increases during weekly periods.

- Unsure how to check availability when delivery date & return date overlaps between multiple bookings.

- How to handle per-customer negotiated prices without corrupting the standard rate on the Items table?

- Rakeshji - not a fast typist - how to make CLI easy? (menu system?) - Yes, what about sub-menus?

- Story says close at night, open in morning -> how to implement this? -> Date comparison logic needed - need experimentation.

- How to handle a booking that spans two calendar months for monthly reporting purposes?
