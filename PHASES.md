# Sharma Tent House - Detailed Phase Plans

---

# Sharma Tent House — Phase Plans (Brief)

---

## Phase 1 — Item Catalogue

**One sentence:** Add, list, update, and delete inventory items, and remember them after restart.

**What's in:** `items.json` only. Fields: item_id, name, total_quantity, rate_per_day, item_type.

**Menu:** Add item · List items · Update item · Delete item · Exit.

**Key rules:**
- Missing file → create empty `[]`, never crash.
- Money stored as string `"5.00"`, never float.
- Auto-generate IDs: ITEM_001, ITEM_002, …

**Prove it works:**
1. Fresh start → list shows "No items yet."
2. Add chair → exit → reopen → chair still there.
3. Update rate → exit → reopen → new rate persists.
4. Bad item_id on update → "Item not found", no crash.

---

## Phase 2 — Availability Engine

**One sentence:** Prove the program correctly answers "how many chairs are free between date X and date Y?"

**What's in:** Add `bookings.json` + `booked_items.json` (minimal — no money, no customers yet).

**The hard rule (overlap logic):**
```
booking overlaps query IF
  booking.delivery_date < query_end
  AND booking.return_datetime > query_start
```
This handles same-day morning-return / evening-booking correctly.

**Availability formula:**
```
available = total_qty − SUM(booked_qty − returned_qty for overlapping bookings)
```

**New menu:** Check availability · Create booking (checks stock first) · Mark items returned · List bookings.

**Prove it works:**
1. No bookings → full qty available.
2. Book 200 chairs → availability drops by 200 on those dates.
3. Non-overlapping booking → does NOT reduce availability.
4. B001 returns at 10:00 → items are available again for a query starting 18:00 same day.
5. Over-booking → rejected with "Only X available."
6. Persists across restart.

---

## Phase 3 — Full Business (5 sub-steps)

**One sentence:** Expand into everything Rakesh ji actually needs — in small steps, never breaking what works.

**3A — Customers:** Add `customers.json`. Link cust_id to bookings. Search by phone.

**3B — Money:** Add advance, deposit, total_rental_amount to bookings. Add `payments.json`. Compute balance_due on demand (never stored). All amounts as string decimals.

**3C — Deliver & Return cycle:** Add `delivery_records.json` + `return_records.json`. Support partial returns. Block booking close until: all items returned + balance_due = 0 + deposit settled.

**3D — Damage:** Add `damage_records.json`. Log damage at return time. Settle deposit against damage charges. Alert if damage exceeds deposit.

**3E — Maintenance + Reports:** Add `maintenance_records.json`. Maintenance subtracts from availability. Add: Items currently out (sorted by return time) · Day view (deliveries + returns on a date) · Customer history.

**After each sub-step:** still a working program you could hand to Rakesh ji.

---

## Phase 4 — Break It

**One sentence:** Find every failure the real wedding season would expose, decide what the program should do, and prove it.

**Availability failures:** 10 concurrent bookings; bad date order rejected at creation; maintenance overlapping a booking; zero stock.

**Money failures:** Payment on closed booking; advance > total (warn + confirm); deposit already fully returned; float slippage on 5 partial payments; late-return extra_charges stored as string decimal.

**Corrupt state:** Invalid JSON on startup → plain-English error, no traceback. Orphan foreign keys (booking references missing item or customer) → flagged, not crash.

**Business edge cases:** Cancellation policy (full / 50% / no refund by days-out); date change re-runs availability check; add items to existing booking (offer max available); delete item with active bookings refused; same customer books same item twice on overlapping dates caught by availability.

**Return failures:** Return qty > booked qty → rejected. Return on closed booking → rejected.

**For each failure:** write what happened → decide correct behaviour → implement → add named test.

---

## Phase 5 - Hand It Over

**One sentence:** Make the code and CLI clean enough that a stranger can read one and Rakesh ji can use the other without help.

**Code:** Split into modules (items.py, bookings.py, customers.py, payments.py, returns.py, delivery.py, reports.py, storage.py, validators.py). Audit every money value — `Decimal` everywhere, zero floats. Readable names, no magic numbers.

**CLI:** Numbered sub-menus (Inventory / Customers / Bookings / Payments / Delivery & Returns / Reports). Every prompt shows expected format: `Start date [YYYY-MM-DD]:`. Bad input re-prompts - never crashes. Currency always shows `₹6,500.00`. Confirm before every destructive action.

**Startup checks:** Create missing JSON files. Warn on duplicate IDs. Warn on orphan foreign keys. Never refuse to start.

**README:** Requirements → setup → first run → how to run tests → where data lives. A stranger reaches the menu in under 10 minutes.

**Final demo (handover test):** Rakesh ji completes - add 3 items · add customer · create booking · mark delivery · check availability · record return · record payment · close booking · view customer history · exit and reopen — without asking what to type. If he can, Phase 5 is done.